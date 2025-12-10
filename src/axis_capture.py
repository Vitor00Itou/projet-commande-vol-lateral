from src.constants import TAU_EY, X_EQUI, Y_EQUI
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
last_timestamp = 0 # for measuring the current time step
x_acc = X_EQUI # initial x position
y_acc = Y_EQUI # initial y position

"""
There are more parameters than MATLAB here because we need to receive the axis coordinates
from the FGS, instead of getting these parameters from the 'constants.py' module, for example.
"""
def axis_capture(x_dot, y_dot, axis_x, axis_y, axis_track, timestamp):
    global x_acc, y_acc, last_timestamp
    
    # First call: initialize timestamp
    if last_timestamp is None:
        last_timestamp = timestamp
        return axis_track  # no correction yet

    dt = timestamp - last_timestamp
    last_timestamp = timestamp

    # Avoid bad dt (should be > 0)
    if dt < 0:
        # ignore backward time jumps
        dt = 0
    elif dt > 1:  
        # probably lost messages (safety clamp)
        dt = 1

    # integrate
    x_acc += x_dot * dt
    y_acc += y_dot * dt
    
    lat_dist = axis_lateral_distance(x_acc, axis_x, y_acc, axis_y, axis_track)
    return get_track_command(x_dot, y_dot, lat_dist, TAU_EY, axis_track)
