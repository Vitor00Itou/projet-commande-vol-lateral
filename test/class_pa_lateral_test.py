import pandas as pd
import pytest
import os
import sys
import numpy as np

# --- 1. CONFIGURAÇÃO DE CAMINHOS ---
# Garante que o python encontre a pasta 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.class_pa_lateral import PA_Lateral

# --- 2. CONFIGURAÇÕES GERAIS ---
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'output')
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data')

# Cria a pasta de output se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- 3. HELPER FUNCTION (O Motor dos Testes) ---
def run_simulation_and_save(pa, input_filename, output_filename):
    """
    1. Lê o Excel de referência.
    2. Roda a simulação Python linha a linha.
    3. Compara resultados (Roll Rate e Ey).
    4. Guarda um novo Excel para inspeção visual.
    """
    input_path = os.path.join(DATA_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    assert os.path.exists(input_path), f"Ficheiro não encontrado: {input_path}"
    
    df = pd.read_excel(input_path)
    
    # Listas para armazenar o resultado do Python
    py_roll_rates = []
    py_ey_values = [] # <--- NOVA LISTA PARA O Ey
    
    # --- LOOP DE SIMULAÇÃO ---
    for _, row in df.iterrows():
        # 1. Ler Inputs do Avião (Estado)
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row.get('X', 0)) 
        Y = float(row.get('Y', 0))
        gamma = float(row.get('Gamma', 0))
        
        # 2. Ler Inputs de Cenário/Controle
        W = float(row.get('Input_W', 0))
        PsiW = float(row.get('Input_PsiW', 0))
        Ts_val = float(row.get('Input_Ts', 1.0))
        
        # Inputs de Axis
        Xa = float(row.get('Input_Xa', 0))
        Ya = float(row.get('Input_Ya', 0))
        Ra = float(row.get('Input_Rhoa', 0))

        # Inputs de FCU (Heading/Track)
        if 'Input_route' in row and not pd.isna(row['Input_route']):
            pa.update_fcu_track_command(float(row['Input_route']))
            
        if 'Input_cap' in row and not pd.isna(row['Input_cap']):
            pa.update_fcu_heading_command(float(row['Input_cap']))

        # 3. Atualizar PA
        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        
        # 4. Calcular (Executar a lógica)
        roll_rate_py = pa.calculate_roll_rate(X, Y, Vp, gamma=gamma, psi=Psi, phi=Phi)
        
        # 5. Guardar resultados
        py_roll_rates.append(roll_rate_py)
        
        # --- CAPTURA DO Ey ---
        # Verifica se o PA calculou e guardou o Ey no stats
        if pa.stats and 'Ey' in pa.stats and len(pa.stats['Ey']) > 0:
            py_ey_values.append(pa.stats['Ey'][-1])
        else:
            # Se não houver Ey (ex: modo Heading), guarda 0 ou NaN
            py_ey_values.append(0.0)

    # --- PÓS-PROCESSAMENTO ---
    
    # Adiciona os resultados do Python ao DataFrame original
    df['Py_RollRate'] = py_roll_rates
    df['Py_Ey'] = py_ey_values # <--- NOVA COLUNA NO EXCEL
    
    # Renomeia colunas de referência do Matlab para clareza
    if 'Roll_rate' in df.columns:
        df.rename(columns={'Roll_rate': 'Ref_RollRate'}, inplace=True)
    
    # Calcula diferenças (Erros)
    if 'Ref_RollRate' in df.columns:
        df['Diff_RollRate'] = df['Py_RollRate'] - df['Ref_RollRate']
        
    # Comparação do Ey (Se existir Ey no ficheiro original)
    if 'Ey' in df.columns:
        df.rename(columns={'Ey': 'Ref_Ey'}, inplace=True)
        df['Diff_Ey'] = df['Py_Ey'] - df['Ref_Ey'] # <--- DIFERENÇA DO ERRO LATERAL

    # Guarda o Excel final
    df.to_excel(output_path, index=False)
    print(f"\n[INFO] Resultados guardados em: {output_path}")
    
    return df

# --- 4. FIXTURE ---
@pytest.fixture
def pa():
    return PA_Lateral()

# --- 5. TESTES ---

def test_axis_capture(pa):
    print("\n--- Rodando Teste: Axis Capture ---")
    pa.define_flight_mode(managed_mode=True, cmd_type=None)
    
    df = run_simulation_and_save(pa, "ts_axis1.xlsx", "result_axis.xlsx")
    
    # Validação do Roll Rate
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error_roll = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error_roll:.5f}")
        assert max_error_roll < 0.05, f"RollRate diverge! Erro: {max_error_roll}"

    # Validação do Ey (Erro Lateral) - CRUCIAL PARA AXIS CAPTURE
    if 'Ref_Ey' in df.columns:
        valid_rows_ey = df.dropna(subset=['Ref_Ey'])
        max_error_ey = valid_rows_ey['Diff_Ey'].abs().max()
        print(f"Erro Máx Ey: {max_error_ey:.5f}")
        
        # Tolerância maior para posição (ex: 1 metro), pois erros acumulam
        assert max_error_ey < 1.0, f"Ey diverge! O Python está a {max_error_ey}m do Matlab"


def test_track_capture(pa):
    print("\n--- Rodando Teste: Track Capture ---")
    pa.define_flight_mode(managed_mode=False, cmd_type="Track")
    
    df = run_simulation_and_save(pa, "ts_route1.xlsx", "result_track.xlsx")
    
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error:.5f}")
        assert max_error < 0.05


def test_heading_capture(pa):
    print("\n--- Rodando Teste: Heading Capture ---")
    pa.define_flight_mode(managed_mode=False, cmd_type="Heading")
    
    df = run_simulation_and_save(pa, "ts_cap1.xlsx", "result_heading.xlsx")
    
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error:.5f}")
        assert max_error < 0.05