import pandas as pd
import matplotlib.pyplot as plt
import os

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'output')
PLOT_DIR = os.path.join(BASE_DIR, 'data', 'plots')

# Ensure plot directory exists
os.makedirs(PLOT_DIR, exist_ok=True)

# Set visual style (optional, falls back to default if unavailable)
try:
    plt.style.use('seaborn-v0_8-darkgrid')
except:
    plt.grid(True, linestyle='--', alpha=0.6)

def generate_comparative_plots(df, mode_name, metric_key, unit_label):
    """
    Generates 2 images for a given metric:
    1. Overlaid (Reference vs Python on the same axes)
    2. Separated (Reference on top, Python on bottom)
    """
    
    # Column Names
    ref_col = f"Ref_{metric_key}"
    py_col = f"Py_{metric_key}"
    
    # Check if columns exist
    if ref_col not in df.columns or py_col not in df.columns:
        print(f"[WARN] Skipping {metric_key} for {mode_name}: Columns not found.")
        return

    time = df['Time']
    
    # --- 1. OVERLAID PLOT ---
    plt.figure(figsize=(10, 6))
    plt.plot(time, df[ref_col], 'k--', label='Matlab (Reference)', linewidth=2, alpha=0.7)
    plt.plot(time, df[py_col], 'r-', label='Python (Implementation)', linewidth=1.5)
    
    plt.title(f"{mode_name}: {metric_key} Comparison (Overlay)", fontsize=14)
    plt.xlabel("Time (s)", fontsize=12)
    plt.ylabel(f"{metric_key} ({unit_label})", fontsize=12)
    plt.legend(fontsize=11)
    plt.grid(True, which='both', linestyle='--', alpha=0.7)
    
    filename_overlay = f"{mode_name.lower()}_{metric_key.lower()}_overlay.png"
    save_path = os.path.join(PLOT_DIR, filename_overlay)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[OK] Saved: {filename_overlay}")

    # --- 2. SEPARATED PLOT (Subplots) ---
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
    
    plt.suptitle(f"{mode_name}: {metric_key} Analysis (Separated Planes)", fontsize=14)
    
    filename_sep = f"{mode_name.lower()}_{metric_key.lower()}_separated.png"
    save_path = os.path.join(PLOT_DIR, filename_sep)
    plt.savefig(save_path, dpi=150)
    plt.close()
    print(f"[OK] Saved: {filename_sep}")

def main():
    print("--- Starting Plot Generation (English Version) ---\n")

    # 1. AXIS CAPTURE (Expects RollRate AND Ey)
    path_axis = os.path.join(DATA_DIR, 'result_axis.xlsx')
    if os.path.exists(path_axis):
        df = pd.read_excel(path_axis)
        # Plot 1 & 2: Roll Rate
        generate_comparative_plots(df, "Axis_Capture", "RollRate", "rad/s")
        # Plot 3 & 4: Ey (Cross Track Error)
        generate_comparative_plots(df, "Axis_Capture", "Ey", "meters")
    else:
        print("[ERR] result_axis.xlsx not found.")

    # 2. TRACK CAPTURE (RollRate Only)
    path_track = os.path.join(DATA_DIR, 'result_track.xlsx')
    if os.path.exists(path_track):
        df = pd.read_excel(path_track)
        # Plot 5 & 6
        generate_comparative_plots(df, "Track_Capture", "RollRate", "rad/s")
    else:
        print("[ERR] result_track.xlsx not found.")

    # 3. HEADING CAPTURE (RollRate Only)
    # Check for both possible filenames just in case
    path_heading = os.path.join(DATA_DIR, 'result_heading.xlsx')
    if not os.path.exists(path_heading):
        path_heading = os.path.join(DATA_DIR, 'result_cap.xlsx')

    if os.path.exists(path_heading):
        df = pd.read_excel(path_heading)
        # Plot 7 & 8
        generate_comparative_plots(df, "Heading_Capture", "RollRate", "rad/s")
    else:
        print("[ERR] result_heading.xlsx not found.")

    print("\n--- All plots generated in /data/plots/ ---")

if __name__ == "__main__":
    main()