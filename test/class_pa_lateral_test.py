from src.class_pa_lateral import PA_Lateral

pa = PA_Lateral()

def test_axis_capture():
    """
    - definir o modo de captura de eixo:
        - setar flag "managed_mode" pra True
    - receber/ler inputs de W, psiW, xa, ya e Ra
    - atualizar (enviar) o objeto PA_Lateral com os dados de vento (W e psiW)
    - atualizar (enviar) o objeto PA_Lateral com o comando de xa, ya e Ra
    - para cada timestamp t no arquivo MATLAB:
        - ler Vp, Psi, Phi, X, Y, W, PsiW, Xa, Ya, Ra, Ts (inputs do PA)
        - atualizar PA_Lateral com esses inputs (update_timestamp, update_wind, update_fgs_axis)
        - chamar calculate_roll_rate(Vp, gamma, psi, phi)
        - (calculate_roll_rate já loga tudo em stats automaticamente)
    - extrair "stats" do objeto de PA_Lateral com os dados gerados da simulação
    - retornar pro pytest o "stats" (para fazer comparações automaticamente, gerar de gráficos, etc)
    """
    pass
