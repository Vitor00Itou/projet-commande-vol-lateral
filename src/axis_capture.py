from src.constants import TAU_EY, X_EQUI, Y_EQUI
from numpy import sin, cos, asin, sqrt

"""
This function has been named 'captureEcartLateral' in MATLAB, and the last argument as 'rhoa'.
"""
def axis_lateral_distance(x, xa, y, ya, axis_track):
    return -(x - xa) * sin(axis_track) + (y - ya) * cos(axis_track)

"""
Calculates the track correction command needed to reduce lateral distance to zero.
"""
def get_track_command(x_dot, y_dot, lateral_distance, time_constant, axis_track):
	ground_speed = sqrt(x_dot**2 + y_dot**2)
	arg = -lateral_distance / (time_constant * ground_speed)
	arg = max(-1, min(1, arg)) # -1 <= arg <= 1
	return asin(arg) + axis_track

"""
There are more parameters than MATLAB here because we need to receive the axis coordinates
from the FGS, instead of getting these parameters from the 'constants.py' module, for example.
"""
def axis_capture(X, Y, x_dot, y_dot, axis_x, axis_y, axis_track):
    global x_acc, y_acc
    
    lat_dist = axis_lateral_distance(X, axis_x, Y, axis_y, axis_track)
    return lat_dist, get_track_command(x_dot, y_dot, lat_dist, TAU_EY, axis_track)
