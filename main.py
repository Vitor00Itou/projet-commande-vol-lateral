import pandas as pd
from ivy.std_api import *
from src.class_pa_lateral import PA_Lateral

pa = PA_Lateral()

def on_state_vector(agent, *larg):
    """
    Handles the state vector message from the simulator, computes the roll rate command,
    and sends it back via Ivy.
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The state vector components as strings.
            Expected order: x, y, z, Vp, gamma (fpa), psi, phi
    """
    X = float(larg[0])
    Y = float(larg[1])
    Vp = float(larg[3])
    gamma = float(larg[4]) # 'fpa'
    psi = float(larg[5])
    phi = float(larg[6])
    
    roll_rate = pa.calculate_roll_rate(X, Y, Vp, gamma, psi, phi)
    
    roll_rate_msg = f'PALat {roll_rate}'
    IvySendMsg(roll_rate_msg)

def on_FCU_lateral_selected(agent, *larg):
    """
    Handles the FCU lateral selected mode message, updating the PA_Lateral instance
    with the new mode and command values.  
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The command type and value as strings.
            Expected order: cmd_type, value
    """
    
    cmd_type = larg[0]
    val = float(larg[1])
    
    if cmd_type == "Heading":
        pa.define_flight_mode(managed_mode=False, cmd_type=cmd_type, fcu_heading_command=val)
    else:
        pa.define_flight_mode(managed_mode=False, cmd_type=cmd_type, fcu_track_command=val)

def on_FCU_lateral_managed_trigger(agent, *larg):
    """
    Handles the FCU lateral managed mode trigger message, updating the PA_Lateral instance
    to managed mode.
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The managed mode value as a string (not used here).    
    """
    pa.define_flight_mode(managed_mode=True, cmd_type=pa.command_type)

def on_FGS_axis_capture_command(agent, *larg):
    """
    Handles the FGS lateral axis command message, updating the PA_Lateral instance
    with the new axis commands.
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The axis commands as strings.
            Expected order: xa, ya, axis_track 
    """
    xa = float(larg[0])
    ya = float(larg[1])
    axis_track = float(larg[2])
    
    pa.update_fgs_axis_command((xa, ya, axis_track))
    
def on_wind_component(agent, *larg):
    """
    Handles the wind component message, updating the PA_Lateral instance
    with the new wind speed and direction.
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The wind speed and direction as strings.
            Expected order: wind_speed, wind_dir
    """
    wind_speed = float(larg[0])
    wind_dir = float(larg[1])
    pa.update_wind_conditions(wind_speed, wind_dir)
    
def on_timestamp(agent, *larg):
    """
    Handles the timestamp message, updating the PA_Lateral instance
    with the new timestamp.
    
    Parameters:
        agent: The Ivy agent (not used here).
        *larg: The timestamp as a string.
    """
    t = float(larg[0])
    pa.update_timestamp(t)


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

# Receives the current state vector of the plane
# Indices no capture: x=0, y=1, z=2, Vp=3, fpa=4, psi=5, phi=6
STATE_VECTOR_TOPIC = r'^StateVector x=(\S+) y=(\S+) z=(\S+) Vp=(\S+) fpa=(\S+) psi=(\S+) phi=(\S+)'
IvyBindMsg(on_state_vector, STATE_VECTOR_TOPIC)

# Receives "lateral selected mode" trigger, type and value
FCU_LATERAL_SELECTED_TOPIC = r'^FCULateral Mode=Selected(\S+) Val=(\S+)'
IvyBindMsg(on_FCU_lateral_selected, FCU_LATERAL_SELECTED_TOPIC)

# Receives "lateral managed mode" trigger
FCU_LATERAL_MANAGED_TRIGGER_TOPIC = r'^FCULateral Mode=Managed Val=(\S+)'
IvyBindMsg(on_FCU_lateral_managed_trigger, FCU_LATERAL_MANAGED_TRIGGER_TOPIC)

# Receives FGS lateral command
FGS_LATERAL_COMMAND_TOPIC = r'^FGSLateral Mode=Axe Xa=(\S+) Ya=(\S+) Ra=(\S+)'
IvyBindMsg(on_FGS_axis_capture_command, FGS_LATERAL_COMMAND_TOPIC)

# Receives wind parameters
WIND_COMPONENT_TOPIC = r'WindComponent VWind=(\S+) dirWind=(\S+)'
IvyBindMsg(on_wind_component, WIND_COMPONENT_TOPIC)

# Receives timestamps
TIMESTAMP_TOPIC = r'Time t=(\S+)'
IvyBindMsg(on_timestamp, TIMESTAMP_TOPIC)

IvyMainLoop()
