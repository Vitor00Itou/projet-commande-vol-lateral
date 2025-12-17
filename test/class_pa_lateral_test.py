import pandas as pd
import pytest
import os
import sys
import numpy as np

# Guarantee that the src folder is in the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.class_pa_lateral import PA_Lateral

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'data', 'output') # Output data directory
DATA_DIR = os.path.join(os.path.dirname(__file__), '..', 'data') # Input data directory

# Creates output directory if it doesn't exist
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- AUXILIARY FUNCTION (Tests Engine) ---
def run_simulation_and_save(pa, input_filename, output_filename):
    """
    1. Reads the reference Excel.
    2. Runs the Python simulation line by line.
    3. Compares results (Roll Rate and Ey).
    4. Saves a new Excel for visual inspection.
    """
    input_path = os.path.join(DATA_DIR, input_filename)
    output_path = os.path.join(OUTPUT_DIR, output_filename)

    assert os.path.exists(input_path), f"File not found: {input_path}"
    
    df = pd.read_excel(input_path)
    
    # List for storing Python results
    py_roll_rates = []
    py_ey_values = [] # <--- NEW LIST FOR Ey
    
    # --- SIMULATION LOOP ---
    for _, row in df.iterrows():
        # Read inputs from the Excel row
        Vp = float(row['TAS'])
        Psi = float(row['Psi'])
        Phi = float(row['Phi'])
        X = float(row.get('X', 0)) 
        Y = float(row.get('Y', 0))
        gamma = float(row.get('Gamma', 0))
        
        # Read scenario/control inputs
        W = float(row.get('Input_W', 0))
        PsiW = float(row.get('Input_PsiW', 0))
        Ts_val = float(row.get('Time', 1.0))
        
        # Inputs related to Axis Capture
        Xa = float(row.get('Input_Xa', 0))
        Ya = float(row.get('Input_Ya', 0))
        Ra = float(row.get('Input_Rhoa', 0))

        # Inputs related to FCU (Heading/Track)
        if 'Input_route' in row and not pd.isna(row['Input_route']):
            pa.update_fcu_track_command(float(row['Input_route']))
            
        if 'Input_cap' in row and not pd.isna(row['Input_cap']):
            pa.update_fcu_heading_command(float(row['Input_cap']))

        # Update the AP
        pa.update_timestamp(Ts_val)
        pa.update_wind_conditions(W, PsiW)
        pa.update_fgs_axis_command((Xa, Ya, Ra))
        
        # Calculate roll rate
        roll_rate_py = pa.calculate_roll_rate(X, Y, Vp, gamma=gamma, psi=Psi, phi=Phi)
        
        # Save results
        py_roll_rates.append(roll_rate_py)
        
        # Ey capture
        # Verifies if we are in managed mode to get Ey in the stats
        if pa.stats and 'Ey' in pa.stats and len(pa.stats['Ey']) > 0:
            py_ey_values.append(pa.stats['Ey'][-1])
        else:
            # If there is no Ey (e.g., Heading mode), store 0 or NaN
            py_ey_values.append(0.0)

    # --- POST-PROCESSING ---
    
    # Adds Python results to the DataFrame
    df['Py_RollRate'] = py_roll_rates
    df['Py_Ey'] = py_ey_values # <--- NOVA COLUNA NO EXCEL

    # Renames MATLAB columns for clarity
    if 'Roll_rate' in df.columns:
        df.rename(columns={'Roll_rate': 'Ref_RollRate'}, inplace=True)
    
    # Calculates differences (Errors)
    if 'Ref_RollRate' in df.columns:
        df['Diff_RollRate'] = df['Py_RollRate'] - df['Ref_RollRate']
        
    # Ey comparison (if Ey exists in the original file)
    if 'Ey' in df.columns:
        df.rename(columns={'Ey': 'Ref_Ey'}, inplace=True)
        df['Diff_Ey'] = df['Py_Ey'] - df['Ref_Ey'] # <--- DIFERENÇA DO ERRO LATERAL

    # Stores the final Excel
    df.to_excel(output_path, index=False)
    print(f"\n[INFO] Resultados guardados em: {output_path}")
    
    return df

# --- FIXTURE ---
@pytest.fixture
def pa():
    return PA_Lateral()

# --- ACTUAL TESTS ---

def test_axis_capture(pa):
    print("\n--- Running test: Axis Capture ---")
    pa.define_flight_mode(managed_mode=True, cmd_type=None)
    
    df = run_simulation_and_save(pa, "ts_axis1.xlsx", "result_axis.xlsx")
    
    # Roll Rate Validation
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error_roll = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error_roll:.5f}")
        assert max_error_roll < 0.05, f"RollRate diverge! Erro: {max_error_roll}"

    # Ey Validation (Lateral Error Validation - CRUCIAL FOR AXIS CAPTURE)
    if 'Ref_Ey' in df.columns:
        valid_rows_ey = df.dropna(subset=['Ref_Ey'])
        max_error_ey = valid_rows_ey['Diff_Ey'].abs().max()
        print(f"Erro Máx Ey: {max_error_ey:.5f}")
        
        assert max_error_ey < 1.0, f"Ey diverge! O Python está a {max_error_ey} m do Matlab"


def test_track_capture(pa):
    print("\n--- Running test: Track Capture ---")
    pa.define_flight_mode(managed_mode=False, cmd_type="Track")
    
    df = run_simulation_and_save(pa, "ts_route1.xlsx", "result_track.xlsx")
    
    # Roll Rate Validation
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error:.5f}")
        assert max_error < 0.05


def test_heading_capture(pa):
    print("\n--- Running test: Heading Capture ---")
    pa.define_flight_mode(managed_mode=False, cmd_type="Heading")
    
    df = run_simulation_and_save(pa, "ts_cap1.xlsx", "result_heading.xlsx")
    
    # Roll Rate Validation
    if 'Ref_RollRate' in df.columns:
        valid_rows = df.dropna(subset=['Ref_RollRate'])
        max_error = valid_rows['Diff_RollRate'].abs().max()
        print(f"Erro Máx RollRate: {max_error:.5f}")
        assert max_error < 0.05