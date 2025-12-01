import numpy as np

"""
Modelling and control of point mass aircraft model

clear
%close all
%bdclose all
warning('off')

%% The system.

%Constantes
"""

pi = np.pi
g = 9.80665 # m/s2
DEG2RAD = pi / 180
NM2M = 1852
KTS2MS = NM2M / 3600
FT2M = 0.3048
FL2M = 100 * FT2M
FPM2MS = FT2M / 60

k = KTS2MS / (2*FL2M)

# Vent
psiW = 100*DEG2RAD # direction d'ou vient le vent, rad
W = 30*KTS2MS # vitesse du vent, m/s

# Conditions initiales dans les integrateurs de modeleAvion
Vie = 130*KTS2MS # vitesse indiqu�e initiale
gammae = 0*DEG2RAD # rad
psie = 0*DEG2RAD # rad
phie = 0*5*DEG2RAD # rad

# Conditions initiales dans les integrateurs de cinematiqueDuVol
xe = 0*NM2M # m
ye = 0*NM2M # m
ze = 0*100*FL2M # m

# Linearisation
Ve = Vie + k*ze
xe = [Ve, gammae, psie, phie]
nxe = np.sin(gammae)
nze = np.cos(gammae)
pe = 0
ue = [nxe, nze, pe]
# [A,B,C,D] = linmod('modeleAvion', xe, ue)

# Contrôle lateral
k11 = 0.1
k22 = 1

tauGamma = Ve / (g*k22)
tauh = 5*tauGamma # tauh >> tauGamma

#  Contrôle longitudinal
m = 0.9 # coeff amortisement
w0 = 0.1 # pulsation naturelle
k1 = w0**2 * Ve / g
k2 = 2*m*w0

# Contrôle lateral 2
tau_phi = 0.4
tau_psi = 10*tau_phi # tau_psi >> tau_phi

# Capture d'axe
tau_ey = 5*tau_psi
xa = 1000
ya = 2500
rhoa = 180*DEG2RAD

# Periode echantillonnage
Ts = 1 # sec

#writematrix([TAS_m_s.time, TAS_m_s.signals.values], 'Scenario1.xls')
