import numpy as np
from constants import g, Vie, gammae, psie, phie

def vdot(nx, gamma) -> float:
    """
    Calcula a derivada da velocidade (vdot) do avião com base nos estados e entradas de controle.
    
    Parâmetros:
        nx (float): Componente norte da direção do vetor de velocidade normalizado.
        gamma (float): Ângulo de voo (flight path angle) em radianos.
    
    Retorna:
        float: Derivada da velocidade (vdot)
    """
    # Eq: g * (u(1) - sin(u(2)))
    return g * (nx - np.sin(gamma))


def gamma_dot(nz, gamma, v, phi) -> float:
    """
    Calcula a derivada do ângulo de voo (gamma_dot) do avião com base
    nos estados e entradas de controle.
    
    Parâmetros:
        nz (float): Componente vertical da direção do vetor de velocidade normalizado.
        gamma (float): Ângulo de voo (flight path angle) em radianos.
        v (float): Velocidade do avião em m/s.
        phi (float): Ângulo de inclinação (bank angle) em radianos.
    
    Retorna:
        float: Derivada do ângulo de voo (gamma_dot)
    """
    # Eq: g/u(3) * (u(1)*cos(u(2)) - cos(u(4)))
    v_safe = max(v, 0.1) 
    return (g / v_safe) * (nz * np.cos(gamma) - np.cos(phi))


def psi_dot(nz, phi, v, gamma) -> float:
    """
    Calcula a derivada do ângulo de guinada (psi_dot) do avião com base
    nos estados e entradas de controle.
    
    Parâmetros:
        nz (float): Componente vertical da direção do vetor de velocidade normalizado.
        phi (float): Ângulo de inclinação (bank angle) em radianos.
        v (float): Velocidade do avião em m/s.
        gamma (float): Ângulo de voo (flight path angle) em radianos.
        
    Retorna:
        float: Derivada do ângulo de guinada (psi_dot)
    """
    # Eq: g * sin(u(2)) * u(1) / (u(3) * cos(u(4)))
    v_safe = max(v, 0.1)
    denominador = v_safe * np.cos(gamma)
    if abs(denominador) < 1e-6: denominador = 1e-6 # Proteção
    return (g * np.sin(phi) * nz) / denominador


def phi_dot(p) -> float:
    return p


def simulate_avion(t_inicial, t_final):
    """
    Simula a dinâmica do avião ao longo do tempo usando integração numérica simples (Euler).
    
    Parâmetros:
        t_inicial (float): Tempo inicial da simulação em segundos.
        t_final (float): Tempo final da simulação em segundos.
    
    Retorna:
        tuple: Arrays de tempo e estados (v, gamma, psi, phi) ao longo da simulação.
    """
    
    # Configuração de Tempo
    dt = 0.01  # Passo de integração (Ts)
    t = np.arange(t_inicial, t_final, dt)
    n_steps = len(t)

    # Inicialização dos Arrays de Estado
    v_arr = np.zeros(n_steps)
    gamma_arr = np.zeros(n_steps)
    psi_arr = np.zeros(n_steps)
    phi_arr = np.zeros(n_steps)

    # APLICAÇÃO DAS CONDIÇÕES INICIAIS (t=0)
    v_arr[0] = Vie
    gamma_arr[0] = gammae
    psi_arr[0] = psie
    phi_arr[0] = phie

    # Definição dos Inputs de Controle (u)
    nx_input = np.zeros(n_steps)      # nx = 0 (equilíbrio)
    nz_input = np.ones(n_steps)       # nz = 1 (voo sustentado)
    p_input = np.zeros(n_steps)       # p = 0 (manter bank angle constante)

    # Loop de Integração (Euler)
    for k in range(n_steps - 1):
        # 1. Ler estados atuais
        v_k = v_arr[k]
        gam_k = gamma_arr[k]
        psi_k = psi_arr[k]
        phi_k = phi_arr[k]

        # 2. Ler inputs
        nx = nx_input[k]
        nz = nz_input[k]
        p = p_input[k]

        # 3. Calcular Derivadas
        dv = vdot(nx, gam_k)
        dg = gamma_dot(nz, gam_k, v_k, phi_k)
        dpsi = psi_dot(nz, phi_k, v_k, gam_k)
        dphi = phi_dot(p)

        # 4. Integrar (Passo Euler)
        v_arr[k+1] = v_k + dv * dt
        gamma_arr[k+1] = gam_k + dg * dt
        psi_arr[k+1] = psi_k + dpsi * dt
        phi_arr[k+1] = phi_k + dphi * dt

    return {
        "time": t,
        "v": v_arr,
        "gamma": gamma_arr,
        "psi": psi_arr,
        "phi": phi_arr
    }