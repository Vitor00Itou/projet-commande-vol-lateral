import pandas as pd
import pytest
import os
import sys
import numpy as np
import glob  # <--- Biblioteca para achar os arquivos

# Guarantee that the src folder is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.class_pa_lateral import PA_Lateral

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
OUTPUT_DIR = os.path.join(BASE_DIR, '..', 'data', 'output')

# Creates output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- HELPER: ENCONTRAR ARQUIVOS ---
def get_test_files(pattern):
    """
    Busca na pasta DATA_DIR todos os arquivos que batem com o padrão (ex: 'ts_axis*.xlsx').
    Retorna uma lista ordenada com os nomes dos arquivos.
    """
    search_path = os.path.join(DATA_DIR, pattern)
    files = glob.glob(search_path)
    # Retorna apenas o nome do arquivo (basename) e ordenado para garantir consistência
    return sorted([os.path.basename(f) for f in files])

# --- AUXILIARY FUNCTION (Tests Engine) ---
def run_simulation_and_save(pa, input_filename, output_filename):
    """
    Roda a simulação para um arquivo e salva o resultado.
    """
    input_path = os.path.join(DATA_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    assert os.path.exists(input_path), f"File not found: {input_path}"
    
    df = pd.read_excel(input_path)
    
    py_roll_rates = []
    py_ey_values = []
    
    # --- SIMULATION LOOP ---
    for _, row in df.iterrows():
        # Inputs Básicos
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row.get('X', 0)) 
        Y = float(row.get('Y', 0))
        gamma = float(row.get('Gamma', 0))
        
        # Inputs Cenário
        W = float(row.get('Input_W', 0))
        PsiW = float(row.get('Input_PsiW', 0))
        Ts_val = float(row.get('Time', 1.0)) # Atenção: Verifique se sua coluna chama 'Time' ou 'Input_Ts'
        
        # Inputs Axis
        Xa = float(row.get('Input_Xa', 0))
        Ya = float(row.get('Input_Ya', 0))
        Ra = float(row.get('Input_Rhoa', 0))

        # Inputs FCU
        if 'Input_route' in row and not pd.isna(row['Input_route']):
            pa.update_fcu_track_command(float(row['Input_route']))
        if 'Input_cap' in row and not pd.isna(row['Input_cap']):
            pa.update_fcu_heading_command(float(row['Input_cap']))

        # Update AP
        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        
        # Calculate
        roll_rate_py = pa.calculate_roll_rate(X, Y, Vp, gamma=gamma, psi=Psi, phi=Phi)
        
        py_roll_rates.append(roll_rate_py)
        
        # Capture Ey
        if pa.stats and 'Ey' in pa.stats and len(pa.stats['Ey']) > 0:
            py_ey_values.append(pa.stats['Ey'][-1])
        else:
            py_ey_values.append(0.0)

    # --- SAVE RESULTS ---
    df['Py_RollRate'] = py_roll_rates
    df['Py_Ey'] = py_ey_values

    if 'Roll_rate' in df.columns:
        df.rename(columns={'Roll_rate': 'Ref_RollRate'}, inplace=True)
    
    if 'Ref_RollRate' in df.columns:
        df['Diff_RollRate'] = df['Py_RollRate'] - df['Ref_RollRate']
        
    if 'Ey' in df.columns:
        df.rename(columns={'Ey': 'Ref_Ey'}, inplace=True)
        df['Diff_Ey'] = df['Py_Ey'] - df['Ref_Ey']

    df.to_excel(output_path, index=False)
    print(f"[INFO] Processado: {input_filename} -> {output_filename}")
    
    return df

# --- FIXTURE ---
@pytest.fixture
def pa():
    """Garante um PA novo e limpo para cada arquivo de teste"""
    return PA_Lateral()

# --- ACTUAL TESTS (DYNAMIC) ---

# Procura qualquer arquivo que comece com 'ts_axis' e termine com .xlsx
@pytest.mark.parametrize("filename", get_test_files("ts_axis*.xlsx"))
def test_axis_capture(pa, filename):
    print(f"\n--- Running Axis Test for: {filename} ---")
    
    # Gera nome de saída: ts_axis1.xlsx -> result_axis1.xlsx
    output_filename = filename.replace("ts_", "result_")
    
    pa.define_flight_mode(managed_mode=True, cmd_type=None)
    
    df = run_simulation_and_save(pa, filename, output_filename)
    
    # Validações
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        if not valid_rows.empty:
            max_error_roll = valid_rows['Diff_RollRate'].abs().max()
            assert max_error_roll < 0.05, f"RollRate falhou em {filename}"

    if 'Ref_Ey' in df.columns:
        valid_rows_ey = df.dropna(subset=['Ref_Ey'])
        if not valid_rows_ey.empty:
            max_error_ey = valid_rows_ey['Diff_Ey'].abs().max()
            assert max_error_ey < 1.0, f"Ey falhou em {filename}"


@pytest.mark.parametrize("filename", get_test_files("ts_route*.xlsx"))
def test_track_capture(pa, filename):
    print(f"\n--- Running Track Test for: {filename} ---")
    
    output_filename = filename.replace("ts_", "result_")
    
    pa.define_flight_mode(managed_mode=False, cmd_type="Track")
    
    df = run_simulation_and_save(pa, filename, output_filename)
    
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        if not valid_rows.empty:
            max_error = valid_rows['Diff_RollRate'].abs().max()
            assert max_error < 0.05, f"RollRate falhou em {filename}"


@pytest.mark.parametrize("filename", get_test_files("ts_cap*.xlsx"))
def test_heading_capture(pa, filename):
    print(f"\n--- Running Heading Test for: {filename} ---")
    
    output_filename = filename.replace("ts_", "result_")
    
    pa.define_flight_mode(managed_mode=False, cmd_type="Heading")
    
    df = run_simulation_and_save(pa, filename, output_filename)
    
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        if not valid_rows.empty:
            max_error = valid_rows['Diff_RollRate'].abs().max()
            assert max_error < 0.05, f"RollRate falhou em {filename}"