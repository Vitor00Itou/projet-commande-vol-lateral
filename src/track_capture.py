from constants import WIND_SPEED, PSI_WIND
from numpy import atan2, cos, asin, sin, pi

def get_x_dot(V, gamma, psi, wind, psi_wind):
    return V * cos(gamma) * cos(psi) + wind * cos(psi_wind + pi);

def get_y_dot(V, gamma, psi, wind, psi_wind):
    return V * cos(gamma) * sin(psi) + wind * sin(psi_wind + pi);

def get_drift(V, gamma, wind, psi_wind, track):
    arg = wind / (V*cos(gamma)) * sin(pi + psi_wind - track);
    arg = max(-1, min(1, arg)) # -1 <= arg <= 1
    return asin(arg)

# Named as 'capture_de_route' in MATLAB
def track_capture(V, gamma, psi):
    x_dot = get_x_dot(V, gamma, psi, WIND_SPEED, PSI_WIND)
    y_dot = get_y_dot(V, gamma, psi, WIND_SPEED, PSI_WIND)
    
    track = atan2(y_dot, x_dot)
    drift = get_drift(V, gamma, WIND_SPEED, PSI_WIND, track)
    return x_dot, y_dot, drift
