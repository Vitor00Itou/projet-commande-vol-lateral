import pandas as pd
import matplotlib.pyplot as plt
from src.class_pa_lateral import PA_Lateral
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

df_ref = pd.read_excel("data/ts_axis1.xlsx")

time_ref = df_ref["Time"].values
roll_ref = df_ref["Roll_rate"].values

# Inicializa o objeto PA_Lateral
pa = PA_Lateral()
pa.define_flight_mode(managed_mode=True, cmd_type=None)

pa.stats = {
    "Time": [],
    "Roll_rate": [],
    "RollRate": [],   # usado internamente
    "TAS": [],
    "Psi": [],
    "Phi": [],
    "X": [],
    "Y": [],
    "Gamma": [],
    "Ey": [],
    "Input_W": [],
    "Input_PsiW": [],
    "Input_Xa": [],
    "Input_Ya": [],
    "Input_Rhoa": [],
    "Input_Ts": []
}

for _, row in df_ref.iterrows():
    Vp = float(row["TAS"])
    Psi = float(row["Psi"])
    Phi = float(row["Phi"])
    X = float(row["X"])
    Y = float(row["Y"])
    gamma = float(row["Gamma"])

    W = float(row["Input_W"])
    PsiW = float(row["Input_PsiW"])
    Xa = float(row["Input_Xa"])
    Ya = float(row["Input_Ya"])
    Ra = float(row["Input_Rhoa"])
    Ts_val = float(row["Input_Ts"])

    pa.update_timestamp(Ts_val)
    pa.update_wind_conditions(W, PsiW)
    pa.update_fgs_axis_command((Xa, Ya, Ra))
    pa.calculate_roll_rate(X, Y, Vp, gamma=gamma, psi=Psi, phi=Phi)

# Coleta os dados processados pelo PA_Lateral
time_py = pa.stats["Time"]
roll_py = pa.stats["RollRate"] 
print(len(pa.stats["Time"]))
print(len(pa.stats["RollRate"]))  # ou 'Roll_rate'

print(pa.stats.keys())

plt.figure()
plt.plot(time_ref, roll_ref, label="Matlab")
plt.plot(time_py, roll_py, linestyle="--", label="Python")
plt.xlabel("Time [s]")
plt.ylabel("Roll rate [rad/s]")
plt.title("Axis Capture – Roll Rate Comparison")
plt.legend()
plt.grid(True)
plt.show()

