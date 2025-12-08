from constants import TAU_EY, X_EQUI, Y_EQUI
from numpy import sin, cos, asin, sqrt

"""
This function has been named 'captureEcartLateral' in MATLAB, and the last argument as 'rhoa'.
"""
def axis_lateral_distance(x, xa, y, ya, axis_track):
    return -(x - xa) * sin(axis_track) + (y - ya) * cos(axis_track)

def get_track_command(x_dot, y_dot, lateral_distance, time_constant, axis_track):
	ground_speed = sqrt(x_dot**2 + y_dot**2)
	arg = -lateral_distance / (time_constant * ground_speed)
	arg = max(-1, min(1, arg)) # -1 <= arg <= 1
	return asin(arg) + axis_track

# Discrete integration related variables
dt = 1 # integration step time
x_acc = X_EQUI # initial x position
y_acc = Y_EQUI # initial y position

"""
There are more parameters than MATLAB here because we need to receive the axis coordinates
from the FGS, instead of getting these parameters from the 'constants.py' module, for example.
"""
def axis_capture(x_dot, y_dot, axis_x, axis_y, axis_track):
    # Discrete integration of x speed and y speed
    global x_acc, y_acc
    x_acc += x_dot * dt
    y_acc += y_dot * dt
    
    lat_dist = axis_lateral_distance(x_acc, axis_x, y_acc, axis_y, axis_track)
    return get_track_command(x_dot, y_dot, lat_dist, TAU_EY, axis_track)
