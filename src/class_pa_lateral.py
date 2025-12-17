from numpy import pi
from src.axis_capture import axis_capture
from src.track_capture import track_capture
from src.constants import PSI_EQUI, TAU_PHI, DEG2RAD, V_EQUI, GRAVITY, TAU_PSI, WIND_SPEED, PSI_WIND

"""
Class implementing the lateral autopilot (PA_Lateral) business logic.
"""
class PA_Lateral:
    
    """ Constructor (initializes default values) """
    def __init__(self):
        self.managed_mode_on = True
        self.command_type = "Heading" 
        self.fcu_heading_command = PSI_EQUI 
        self.fcu_track_command = PSI_EQUI
        self.fgs_axis_command = (0, 0, 0)
        self.wind = WIND_SPEED
        self.psi_wind = PSI_WIND  
        self.timestamp = 0
        
        self.stats = {
            'Time': [],
            'TAS': [],
            'X': [],
            'Y': [],
            'Ey': [],
            'Psi': [],
            'Phi': [],
            'RollRate': []
        }
        
    """ Computes the roll rate command based on the current state and mode """
    def phi_command(self, heading_error):
        phi_command = heading_error * (V_EQUI / (GRAVITY * TAU_PSI))
        phi_command = max(-15 * DEG2RAD, min(phi_command, 15 * DEG2RAD))
        return phi_command
    
    """ Normalizes an angle to the range [-pi, pi] """
    def modulo360(self, heading_input):
        optimized_heading = heading_input
        while (optimized_heading > pi):
            optimized_heading = optimized_heading - 2*pi
        while (optimized_heading < -pi):
            optimized_heading = optimized_heading + 2*pi
        return optimized_heading
    
    """ Calculates the roll rate command based on current state and mode """
    def calculate_roll_rate(self, X, Y, Vp, gamma, psi, phi):
        psi_command = 0
        x_dot, y_dot, drift = track_capture(Vp, gamma, psi, self.wind, self.psi_wind)
        
        ey = 0 # calculate Ey only in managed mode
        if self.managed_mode_on:
            """
            Managed (Axis Capture) Mode
            Uses FGS axis command to compute lateral deviation and track command
            """
            axis_x = self.fgs_axis_command[0]
            axis_y = self.fgs_axis_command[1]
            axis_track = self.fgs_axis_command[2]
            
            ey, fgs_track_command = axis_capture(X, Y, x_dot, y_dot, axis_x, axis_y, axis_track)
            psi_command = fgs_track_command - drift
        else:
            """
            Selected Mode
            Uses FCU commands directly
            """
            if self.command_type == "Heading":
                psi_command = self.fcu_heading_command
            elif self.command_type == "Track":
                psi_command = self.fcu_track_command - drift

        # Compute errors and roll rate command based on MATLAB logic
        psi_error = psi_command - psi
        psi_error = self.modulo360(psi_error)
        
        phi_error = self.phi_command(psi_error) - phi
        
        roll_rate = phi_error / TAU_PHI
        
        # --- STATS LOGGING ---
        self.stats['Time'].append(self.timestamp)
        self.stats['TAS'].append(Vp)
        self.stats['X'].append(X)
        self.stats['Y'].append(Y)
        self.stats['Ey'].append(ey)
        self.stats['Psi'].append(psi)
        self.stats['Phi'].append(phi)
        self.stats['RollRate'].append(roll_rate)
        
        return roll_rate
    
    def define_flight_mode(self, managed_mode: bool, cmd_type: str, 
                           fcu_heading_command:float=None,
                           fcu_track_command:float=None):
        """
        Defines the flight mode (managed or selected) and updates command values.
        
        Parameters:
            managed_mode: True for managed mode, False for selected mode.
            cmd_type: "Heading" or "Track" for selected mode.
            fcu_heading_command: Heading command in radians (if applicable).
            fcu_track_command: Track command in radians (if applicable).
        """
        self.managed_mode_on = managed_mode
        self.command_type = cmd_type
        
        if fcu_heading_command is not None:
            self.fcu_heading_command = fcu_heading_command
        if fcu_track_command is not None:
            self.fcu_track_command = fcu_track_command
            
    def update_fgs_axis_command(self, axis_command: tuple[float, float, float]):
        """
        Updates the FGS axis command.
        Parameters:
            axis_command: Tuple containing (xa, ya, axis_track) in meters and radians.
        """
        self.fgs_axis_command = axis_command
    
    def update_fcu_heading_command(self, heading_command: float):
        """
        Updates the FCU heading command.
        Parameters:
            heading_command: Heading command in radians.
        """
        self.fcu_heading_command = heading_command
    
    def update_fcu_track_command(self, track_command: float):
        """
        Updates the FCU track command.
        Parameters:
            track_command: Track command in radians.
        """
        self.fcu_track_command = track_command
        
    def update_wind_conditions(self, wind_speed: float, psi_wind: float):
        """
        Updates the wind conditions.
        Parameters:
            wind_speed: Wind speed in knots.
            psi_wind: Direction from which comes the wind in radians.
        """
        self.wind = wind_speed
        self.psi_wind = psi_wind
        
    def update_timestamp(self, timestamp: float):
        """
        Updates the current timestamp.
        Parameters:
            timestamp: Current time in seconds."""
        self.timestamp = timestamp    
    