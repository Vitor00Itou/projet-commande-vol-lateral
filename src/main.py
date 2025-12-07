from ivy.std_api import *

managed_mode_on = True

# ===== Handlers =====
def on_state_vector(agent, *larg):
    pass

def on_FCU_lateral_selected(agent, *larg):
    pass

def on_FCU_lateral_managed_trigger(agent, *larg):
    pass

def on_FGS_axis_capture_command(agent, *larg):
    pass

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
# State vector
STATE_VECTOR_TOPIC = r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+)fpa=(\S+) psi=(\S+) phi=(\S+)'
IvyBindMsg(on_state_vector, STATE_VECTOR_TOPIC)

"""
Waits for the lateral selected mode trigger, type of command (Heading or Track) and command value from the FCU
"""
FCU_LATERAL_SELECTED_TOPIC = r'^FCULateral Mode=Selected(\S+) Val=(\S+)'
IvyBindMsg(on_FCU_lateral_selected, FCU_LATERAL_SELECTED_TOPIC)

# Lateral managed mode trigger from the FCU
FCU_LATERAL_MANAGED_TRIGGER_TOPIC = r'^FCULateral Mode=Managed Val=(\S+)'
IvyBindMsg(on_FCU_lateral_managed_trigger, FCU_LATERAL_MANAGED_TRIGGER_TOPIC)

# FGS lateral command for axis capture
FGS_LATERAL_COMMAND_TOPIC = r'^FGSLateral Mode=Axe Xa=(\S+) Ya=(\S+) Ra=(\S+)'
IvyBindMsg(on_FGS_axis_capture_command, FGS_LATERAL_COMMAND_TOPIC)

# Start module
IvyMainLoop()
