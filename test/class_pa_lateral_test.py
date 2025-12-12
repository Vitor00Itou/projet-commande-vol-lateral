import pandas as pd
from src.class_pa_lateral import PA_Lateral
import pytest

pa = PA_Lateral()

def test_axis_capture():

    pa.define_flight_mode(managed_mode=True, cmd_type=None)
    df = pd.read_excel("data/Ts_axis1.xlsx")

    for _, row in df.iterrows():
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row['X'])
        Y = float(row['Y'])
        W = float(row['Input_W'])
        PsiW = float(row['Input_PsiW'])
        Xa = float(row['Input_Xa'])
        Ya = float(row['Input_Ya'])
        Ra = float(row['Input_Rhoa'])
        Ts_val = float(row['Input_Ts'])

        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        pa.calculate_roll_rate(X, Y, Vp, gamma=0, psi=Psi, phi=Phi)  

    stats = pa.stats

    assert len(stats['Time']) == len(df), "Número de registros em stats diferente do arquivo de referência"
    assert all(isinstance(v, float) for v in stats['RollRate']), "RollRate deve conter apenas floats"

    assert pa.stats is not None

def test_track_capture():

    pa.define_flight_mode(managed_mode=False, cmd_type="Track")
    df = pd.read_excel("data/TS_route1.xlsx")

    for _, row in df.iterrows():
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row['X'])
        Y = float(row['Y'])
        W = float(row['Input_W'])
        PsiW = float(row['Input_PsiW'])
        Xa = float(row['Input_Xa'])
        Ya = float(row['Input_Ya'])
        Ra = float(row['Input_Rhoa'])
        Ts_val = float(row['Input_Ts'])

        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        pa.calculate_roll_rate(X, Y, Vp, gamma=0, psi=Psi, phi=Phi)  

    stats = pa.stats

    assert len(stats['Time']) == len(df), "Número de registros em stats diferente do arquivo de referência"
    assert all(isinstance(v, float) for v in stats['RollRate']), "RollRate deve conter apenas floats"

    assert pa.stats is not None

def test_heading_capture():

    pa.define_flight_mode(managed_mode=False, cmd_type="Heading")
    df = pd.read_excel("data/Ts_axis1.xlsx")

    for _, row in df.iterrows():
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row['X'])
        Y = float(row['Y'])
        W = float(row['Input_W'])
        PsiW = float(row['Input_PsiW'])
        Xa = float(row['Input_Xa'])
        Ya = float(row['Input_Ya'])
        Ra = float(row['Input_Rhoa'])
        Ts_val = float(row['Input_Ts'])

        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        pa.calculate_roll_rate(X, Y, Vp, gamma=0, psi=Psi, phi=Phi)  

    stats = pa.stats

    assert len(stats['Time']) == len(df), "Número de registros em stats diferente do arquivo de referência"
    assert all(isinstance(v, float) for v in stats['RollRate']), "RollRate deve conter apenas floats"

    assert pa.stats is not None

    """
    - definir o modo de captura de eixo:
        - setar flag "managed_mode" pra True
    - receber/ler inputs de W, psiW, xa, ya e Ra
    - atualizar (enviar) o objeto PA_Lateral com os dados de vento (W e psiW)
    - atualizar (enviar) o objeto PA_Lateral com o comando de xa, ya e Ra
    - para cada timestamp t no arquivo MATLAB:
        - ler Vp, Psi, Phi, X, Y, W, PsiW, Xa, Ya, Ra, Ts (inputs do PA)
        - atualizar PA_Lateral com esses inputs (update_timestamp, update_wind, update_fgs_axis)
        - chamar calculate_roll_rate(Vp, gamma, psi, phi)
        - (calculate_roll_rate já loga tudo em stats automaticamente)
    - extrair "stats" do objeto de PA_Lateral com os dados gerados da simulação
    - retornar pro pytest o "stats" (para fazer comparações automaticamente, gerar de gráficos, etc)
    """