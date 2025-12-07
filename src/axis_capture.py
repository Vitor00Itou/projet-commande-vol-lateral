from numpy import sin, cos, asin, sqrt

"""
This function has been named 'captureEcartLateral' in MATLAB, and the last argument as 'rhoa'.
"""
def lateral_axis_distance(x, xa, y, ya, axis_track):
    return -(x - xa) * sin(axis_track) + (y - ya) * cos(axis_track)

def get_track_command(xdot, ydot, ey, tau_ey, rhoa):
	ground_speed = sqrt(xdot**2 + ydot**2)
	arg = -ey / (tau_ey * ground_speed)
	arg = max(-1, min(1, arg)) # -1 <= arg <= 1
	return asin(arg) + rhoa

"""
There are more parameters than MATLAB here because we need to receive the axis coordinates
from the FGS, instead of getting these parameters from the 'constants.py' module, for example.
"""
def axis_capture(x_dot, y_dot, axis_x, axis_y, axis_track):
    pass