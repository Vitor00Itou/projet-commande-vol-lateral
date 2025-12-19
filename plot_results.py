import pandas as pd
import matplotlib.pyplot as plt
import os
import glob
import re

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Ajuste se seus resultados estiverem em 'data/output' ou apenas 'data'
# O script assume que os .xlsx começam com "result_"
DATA_DIR = os.path.join(BASE_DIR, 'data', 'output') 
PLOT_DIR = os.path.join(BASE_DIR, 'data', 'plots')

# Ensure plot directory exists
os.makedirs(PLOT_DIR, exist_ok=True)

# Set visual style
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.grid(True, linestyle='--', alpha=0.6)

def generate_comparative_plots(df, mode_label, metric_key, unit_label, test_id, file_tag):
    """
    Generates plots identifying the specific test ID.
    file_tag: e.g., 'axis', 'cap', 'route' used for filename generation.
    """
    
    # Column Names
    ref_col = f"Ref_{metric_key}"
    py_col = f"Py_{metric_key}"
    
    # Check if columns exist
    if ref_col not in df.columns or py_col not in df.columns:
        # Tenta fallback para nomes antigos se necessário, ou apenas avisa
        print(f"   [WARN] Skipping {metric_key}: Columns not found in result_{file_tag}{test_id}.")
        return

    time = df['Time']
    
    # --- 1. OVERLAID PLOT ---
    plt.figure(figsize=(10, 6))
    plt.plot(time, df[ref_col], 'k--', label='Matlab (Reference)', linewidth=2, alpha=0.7)
    plt.plot(time, df[py_col], 'r-', label='Python (Implementation)', linewidth=1.5)
    
    plt.title(f"{mode_label} (ID: {test_id}): {metric_key} Comparison", fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel(f"{metric_key} ({unit_label})", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    # Filename ex: axis_id1_rollrate_overlay.png
    filename_overlay = f"{file_tag}_id{test_id}_{metric_key.lower()}_overlay.png"
    save_path = os.path.join(PLOT_DIR, filename_overlay)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()

    # --- 2. SEPARATED PLOT ---
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8), sharex=True)
    
    # Top: Reference
    ax1.plot(time, df[ref_col], 'k-', linewidth=1.5)
    ax1.set_title(f"Reference (Matlab): {metric_key}", fontsize=12)
    ax1.set_ylabel(unit_label)
    ax1.grid(True, linestyle='--', alpha=0.6)
    
    # Bottom: Python
    ax2.plot(time, df[py_col], 'r-', linewidth=1.5)
    ax2.set_title(f"Implementation (Python): {metric_key}", fontsize=12)
    ax2.set_ylabel(unit_label)
    ax2.set_xlabel("Time (s)", fontsize=12)
    ax2.grid(True, linestyle='--', alpha=0.6)
    
    plt.suptitle(f"{mode_label} (ID: {test_id}): {metric_key} Analysis", fontsize=14)
    
    filename_sep = f"{file_tag}_id{test_id}_{metric_key.lower()}_separated.png"
    save_path = os.path.join(PLOT_DIR, filename_sep)
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"   [OK] Generated plots for {metric_key} -> {filename_overlay}")

def main():
    print(f"--- Starting Bulk Plot Generation in {DATA_DIR} ---\n")

    # Find all files matching result_*.xlsx
    search_pattern = os.path.join(DATA_DIR, 'result_*.xlsx')
    files = glob.glob(search_pattern)
    files.sort() # Sort alphabetically

    if not files:
        print("[ERR] No 'result_*.xlsx' files found! Run the tests first.")
        return

    count = 0
    for file_path in files:
        filename = os.path.basename(file_path)
        
        # Regex to extract type and ID. 
        # Matches: result_axis1.xlsx, result_cap10.xlsx, result_route2.xlsx
        match = re.search(r'result_([a-zA-Z]+)(\d+)\.xlsx', filename)
        
        if match:
            mode_tag = match.group(1).lower() # axis, cap, route
            test_id = match.group(2)          # 1, 2, 10...
            
            print(f"Processing: {filename} (Mode: {mode_tag}, ID: {test_id})...")
            
            try:
                df = pd.read_excel(file_path)
                
                # Logic map based on file type
                if mode_tag == 'axis':
                    # Axis Capture: Plots RollRate AND Ey
                    generate_comparative_plots(df, "Axis Capture", "RollRate", "rad/s", test_id, mode_tag)
                    generate_comparative_plots(df, "Axis Capture", "Ey", "m", test_id, mode_tag)
                    
                elif mode_tag == 'route':
                    # Track Capture: Plots RollRate
                    generate_comparative_plots(df, "Track Capture", "RollRate", "rad/s", test_id, mode_tag)
                    
                elif mode_tag == 'cap' or mode_tag == 'heading':
                    # Heading Capture: Plots RollRate
                    generate_comparative_plots(df, "Heading Capture", "RollRate", "rad/s", test_id, mode_tag)
                
                else:
                    print(f"   [SKIP] Unknown mode tag: {mode_tag}")

                count += 1

            except Exception as e:
                print(f"   [ERR] Failed to process {filename}: {e}")
        else:
            print(f"[SKIP] Filename {filename} does not match pattern 'result_NAME#.xlsx'")

    print(f"\n--- Processing Complete. {count} files processed. Check /data/plots/ ---")

if __name__ == "__main__":
    main()