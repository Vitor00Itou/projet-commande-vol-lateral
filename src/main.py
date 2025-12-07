from ivy.std_api import *
from constants import psie

managed_mode_on = True

DEFAULT_AXIS = (0, 0, 0) # (m, m, rad) - Position and angle of the axis
command_type = "Heading" # default
heading_command = psie # rads
track_command = psie # rads
axis_command = DEFAULT_AXIS

# ===== Handlers =====
def on_state_vector(agent, *larg):
    # Extract state variables from the vector
    x = larg[0]
    y = larg[1]
    z = larg[2]
    Vp = larg[3]
    gamma = larg[4] # named as 'fpa' in the Ivy message
    psi = larg[5]
    phi = larg[6]

# Updates the command global variables according to the received commands
def on_FCU_lateral_selected(agent, *larg):
    # Trigger the selected mode
    global managed_mode_on
    managed_mode_on = False
    
    global command_type
    command_type = larg[0]
    if command_type == "Heading":
        global heading_command
        heading_command = larg[1]
    else:
        global track_command
        track_command = larg[1]

def on_FCU_lateral_managed_trigger(agent, *larg):
    global managed_mode_on
    managed_mode_on = True

def on_FGS_axis_capture_command(agent, *larg):
    global axis_command
    xa = larg[0]
    ya = larg[1]
    axis_track = larg[2] # this has also been named as 'Ra' in lectures
    axis_command = (xa, ya, axis_track)

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

# ===== Start module =====
IvyMainLoop()
