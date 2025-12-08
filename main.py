from ivy.std_api import *
from constants import psie, TAU_PHI, DEG2RAD, V_EQUI, GRAVITY, TAU_PSI, WIND_SPEED, PSI_WIND
from numpy import pi
from track_capture import track_capture
from axis_capture import axis_capture

managed_mode_on = True

# Lateral control constants
DEFAULT_AXIS = (0, 0, 0) # (m, m, rad) - Position and angle of the axis
MAX_BANK_ANGLE = 15 * DEG2RAD
MIN_BANK_ANGLE = -15 * DEG2RAD

# Global control variables
command_type = "Heading" # default
fcu_heading_command = psie # rads
fcu_track_command = psie # rads
fgs_axis_command = DEFAULT_AXIS
wind = WIND_SPEED
psi_wind = PSI_WIND
timestamp = 0

# ===== Helpers =====
# Bank angle control law 2 (first order)
def phi_command(heading_error):
    phi_command = heading_error * (V_EQUI / (GRAVITY * TAU_PSI))
    phi_command = max(MIN_BANK_ANGLE, max(phi_command, MAX_BANK_ANGLE))

# Make the best choice for heading command
def modulo360(heading_input):
	optimized_heading = heading_input
	while (optimized_heading > pi):
		optimized_heading = optimized_heading - 2*pi
	while (optimized_heading < -pi):
		optimized_heading = optimized_heading + 2*pi

# ===== Handlers =====
def on_state_vector(agent, *larg):
    # Extract state variables from the vector
    Vp = larg[3]
    gamma = larg[4] # named as 'fpa' in the Ivy message
    psi = larg[5]
    phi = larg[6]
    
    psi_command = 0
    x_dot, y_dot, drift = track_capture(Vp, gamma, psi, wind, psi_wind)
    if managed_mode_on:
        # Extract axis coordinates
        global fgs_axis_command
        axis_x = fgs_axis_command[0]
        axis_y = fgs_axis_command[1]
        axis_track = fgs_axis_command[2]
        
        fgs_track_command = axis_capture(x_dot, y_dot, axis_x, axis_y, axis_track)    
        psi_command = fgs_track_command - drift
    else:
        if command_type == "Heading":
            psi_command = fcu_heading_command
        elif command_type == "Track":
            psi_command = fcu_track_command - drift

    psi_error = psi_command - psi
    psi_error = modulo360(psi_error)
    
    phi_error = phi_command(psi_error) - phi
    
    roll_rate = phi_error / TAU_PHI
    
    roll_rate_msg = f'PALat {roll_rate}'
    IvySendMsg(roll_rate_msg)

# Updates the command global variables according to the received commands
def on_FCU_lateral_selected(agent, *larg):
    # Trigger the selected mode
    global managed_mode_on
    managed_mode_on = False
    
    global command_type
    command_type = larg[0]
    if command_type == "Heading":
        global fcu_heading_command
        fcu_heading_command = larg[1]
    else:
        global fcu_track_command
        fcu_track_command = larg[1]

def on_FCU_lateral_managed_trigger(agent, *larg):
    global managed_mode_on
    managed_mode_on = True

def on_FGS_axis_capture_command(agent, *larg):
    global fgs_axis_command
    xa = larg[0]
    ya = larg[1]
    axis_track = larg[2] # this has also been named as 'Ra' in lectures
    fgs_axis_command = (xa, ya, axis_track)
    
def on_wind_component(agent, *larg):
    global wind
    global psi_wind
    wind = larg[0]
    psi_wind = larg[1]
    
def on_timestamp(agent, *larg):
    global timestamp
    timestamp = larg[0]

# ===== Initializing =====
null_callback = lambda *a: None
module_name = "PALateral"
bus_address = "127.255.255.255:2010"
ready_msg = "Ready"
IvyInit(
	module_name,
	ready_msg,
	0,
	null_callback,
	null_callback
)
IvyStart(bus_address)

# ===== Bindings (subscriptions) =====
"""
Receives the current state vector of the plane
"""
STATE_VECTOR_TOPIC = r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'
IvyBindMsg(on_state_vector, STATE_VECTOR_TOPIC)

"""
Receives the "lateral selected mode" trigger, type of command (Heading or Track) and command value from the FCU
"""
FCU_LATERAL_SELECTED_TOPIC = r'^FCULateral Mode=Selected(\S+) Val=(\S+)'
IvyBindMsg(on_FCU_lateral_selected, FCU_LATERAL_SELECTED_TOPIC)

"""
Receives the "lateral managed mode" trigger from the FCU
"""
FCU_LATERAL_MANAGED_TRIGGER_TOPIC = r'^FCULateral Mode=Managed Val=(\S+)'
IvyBindMsg(on_FCU_lateral_managed_trigger, FCU_LATERAL_MANAGED_TRIGGER_TOPIC)

"""
Receives the FGS lateral command for axis capture
"""
FGS_LATERAL_COMMAND_TOPIC = r'^FGSLateral Mode=Axe Xa=(\S+) Ya=(\S+) Ra=(\S+)'
IvyBindMsg(on_FGS_axis_capture_command, FGS_LATERAL_COMMAND_TOPIC)

"""
Receives wind parameters
"""
WIND_COMPONENT_TOPIC = r'WindComponent VWind=(\S+) dirWind=(\S+)'
IvyBindMsg(on_wind_component, WIND_COMPONENT_TOPIC)

"""
Receives timestamps
"""
TIMESTAMP_TOPIC = r'Time t=(\S+)'
IvyBindMsg(on_timestamp, TIMESTAMP_TOPIC)

# ===== Start module =====
IvyMainLoop()
