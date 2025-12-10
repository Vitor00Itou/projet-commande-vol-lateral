from numpy import pi
from src.axis_capture import axis_capture
from src.track_capture import track_capture
from src.constants import psie, TAU_PHI, DEG2RAD, V_EQUI, GRAVITY, TAU_PSI, WIND_SPEED, PSI_WIND

class PA_Lateral:
    def __init__(self):
        self.managed_mode_on = True
        self.command_type = "Heading" 
        self.fcu_heading_command = psie 
        self.fcu_track_command = psie 
        self.fgs_axis_command = (0, 0, 0)
        self.wind = WIND_SPEED
        self.psi_wind = PSI_WIND  
        self.timestamp = 0
        
    def phi_command(self, heading_error):
        phi_command = heading_error * (V_EQUI / (GRAVITY * TAU_PSI))
        phi_command = max(-15 * DEG2RAD, min(phi_command, 15 * DEG2RAD))
        return phi_command
    
    def modulo360(self, heading_input):
        optimized_heading = heading_input
        while (optimized_heading > pi):
            optimized_heading = optimized_heading - 2*pi
        while (optimized_heading < -pi):
            optimized_heading = optimized_heading + 2*pi
        return optimized_heading
    
    def calculate_roll_rate(self, Vp, gamma, psi, phi): 
        psi_command = 0
        x_dot, y_dot, drift = track_capture(Vp, gamma, psi, self.wind, self.psi_wind)
        
        if self.managed_mode_on:
            axis_x = self.fgs_axis_command[0]
            axis_y = self.fgs_axis_command[1]
            axis_track = self.fgs_axis_command[2]
            
            ey, fgs_track_command = axis_capture(x_dot, y_dot, axis_x, axis_y, axis_track)    
            psi_command = fgs_track_command - drift
        else:
            if self.command_type == "Heading":
                psi_command = self.fcu_heading_command
            elif self.command_type == "Track":
                psi_command = self.fcu_track_command - drift

        psi_error = psi_command - psi
        psi_error = self.modulo360(psi_error)
        
        phi_error = self.phi_command(psi_error) - phi
        
        roll_rate = phi_error / TAU_PHI
        
        return ey, roll_rate
    
    def define_flight_mode(self, managed_mode: bool, cmd_type: str, 
                           fcu_heading_command:float=None,
                           fcu_track_command:float=None):
        self.managed_mode_on = managed_mode
        self.command_type = cmd_type
        
        if fcu_heading_command is not None:
            self.fcu_heading_command = fcu_heading_command
        if fcu_track_command is not None:
            self.fcu_track_command = fcu_track_command
            
    def update_fgs_axis_command(self, axis_command: tuple[float, float, float]):
        self.fgs_axis_command = axis_command
    
    def update_fcu_heading_command(self, heading_command: float):
        self.fcu_heading_command = heading_command
    
    def update_fcu_track_command(self, track_command: float):
        self.fcu_track_command = track_command
        
    def update_wind_conditions(self, wind_speed: float, psi_wind: float):
        self.wind = wind_speed
        self.psi_wind = psi_wind
        
    def update_timestamp(self, timestamp: float):
        self.timestamp = timestamp    
    