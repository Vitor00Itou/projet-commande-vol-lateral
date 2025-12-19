%% Script Geração de Cenários CAPTURE CAP (Heading) - 10 CASOS
clear; clc; warning('off');

% ---------------------------------------------------------
% 1. CONFIGURAÇÃO INTELIGENTE (SALVA EM ../data)
% ---------------------------------------------------------
[pasta_do_script, ~, ~] = fileparts(mfilename('fullpath'));
output_dir = fullfile(pasta_do_script, '..', 'data');

if ~exist(output_dir, 'dir')
    mkdir(output_dir);
end

fprintf('------------------------------------------------\n');
fprintf('SALVANDO EM: %s\n', output_dir);
fprintf('------------------------------------------------\n');

% Carrega constantes
if exist('startCADV.m', 'file')
    run("startCADV.m");
else
    assignin('base', 'DEG2RAD', pi/180);
    assignin('base', 'KTS2MS', 0.514444);
    assignin('base', 'NM2M', 1852);
end

DEG2RAD = pi/180;
if exist('NM2M', 'var'), KTS2MS = NM2M / 3600; else, KTS2MS = 0.514444; end

% ---------------------------------------------------------
% 2. DEFINIÇÃO DOS CENÁRIOS (COM VARIAÇÃO DE Ts)
% ---------------------------------------------------------
idx = 1;

% CENÁRIO 1: O Pedido Original (Ts = 0.6)
scenarios(idx).id = 1;
scenarios(idx).desc = 'Original_Request';
scenarios(idx).W = 30 * KTS2MS;
scenarios(idx).psiW = 100 * DEG2RAD;
scenarios(idx).commande_cap = 90;
scenarios(idx).Ts = 0.6;
% Dummies para evitar erro no simulink
scenarios(idx).xa = 1000; scenarios(idx).ya = 2000; scenarios(idx).rhoa = 120*DEG2RAD;

idx = idx + 1;
% CENÁRIO 2: Básico - Sem Vento, Cap Sul (Ts = 0.6)
scenarios(idx).id = 2;
scenarios(idx).desc = 'Baseline_NoWind';
scenarios(idx).W = 0;
scenarios(idx).psiW = 0;
scenarios(idx).commande_cap = 180;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 3: Vento de Través (Crosswind) (Ts = 0.6)
scenarios(idx).id = 3;
scenarios(idx).desc = 'Crosswind_West';
scenarios(idx).W = 20 * KTS2MS;
scenarios(idx).psiW = 0; % Vento do Norte
scenarios(idx).commande_cap = 270; % Voando para Oeste
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 4: Ajuste Fino (Pequena variação) (Ts = 0.6)
% Teste para ver se não há oscilação em comandos pequenos (10 graus)
scenarios(idx).id = 4;
scenarios(idx).desc = 'Small_Adjustment';
scenarios(idx).W = 0;
scenarios(idx).psiW = 0;
scenarios(idx).commande_cap = 10; % Apenas 10 graus
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 5: Cruzamento do Norte (Wrapping) (Ts = 0.6)
% Comandar 350 -> 0 -> 10 graus. Teste de lógica trigonométrica.
scenarios(idx).id = 5;
scenarios(idx).desc = 'North_Wrapping';
scenarios(idx).W = 15 * KTS2MS;
scenarios(idx).psiW = 90 * DEG2RAD;
scenarios(idx).commande_cap = 355; % Quase norte
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 6: Alta Velocidade + Ts Lento (Ts = 1.0)
% Vento de cauda aumenta a Ground Speed. Ts lento diminui a margem de fase.
% Teste de estabilidade.
scenarios(idx).id = 6;
scenarios(idx).desc = 'HighSpeed_SlowTs';
scenarios(idx).W = 30 * KTS2MS;
scenarios(idx).psiW = 0; % Vento de Norte
scenarios(idx).commande_cap = 0; % Voando para Norte (Vento de cauda se inicial for 0)
% Nota: Se o avião inicia em psi=0 e vento vem de 0, é Headwind. 
% Vamos por vento vindo de 180 (Sul) para ser Tailwind voando para Norte (0).
scenarios(idx).psiW = 180 * DEG2RAD; 
scenarios(idx).Ts = 1.0; % <--- Ts LENTO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 7: Baixa Velocidade + Ts Rápido (Ts = 0.4)
% Vento de proa forte reduz GS. Ts rápido.
scenarios(idx).id = 7;
scenarios(idx).desc = 'LowSpeed_FastTs';
scenarios(idx).W = 40 * KTS2MS; % Vento forte
scenarios(idx).psiW = 0; % Vento de Norte
scenarios(idx).commande_cap = 0; % Voando contra o vento
scenarios(idx).Ts = 0.4; % <--- Ts RÁPIDO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 8: A Curva de 180 Graus (U-Turn) (Ts = 0.8)
% Erro máximo possível.
scenarios(idx).id = 8;
scenarios(idx).desc = 'U_Turn_180';
scenarios(idx).W = 10 * KTS2MS;
scenarios(idx).psiW = 90 * DEG2RAD;
scenarios(idx).commande_cap = 179; % Quase 180 graus de giro
scenarios(idx).Ts = 0.8; % Ts intermediário
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 9: Tempestade (Vento Extremo) (Ts = 0.6)
scenarios(idx).id = 9;
scenarios(idx).desc = 'Storm_Conditions';
scenarios(idx).W = 50 * KTS2MS; % 50 Nós!
scenarios(idx).psiW = 45 * DEG2RAD;
scenarios(idx).commande_cap = 135;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 10: Latência Crítica (Ts = 1.2)
% Teste de robustez com amostragem muito lenta.
scenarios(idx).id = 10;
scenarios(idx).desc = 'Critical_Latency';
scenarios(idx).W = 10 * KTS2MS;
scenarios(idx).psiW = 270 * DEG2RAD;
scenarios(idx).commande_cap = 90;
scenarios(idx).Ts = 1.2; % <--- Ts MUITO LENTO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

% ---------------------------------------------------------
% 3. LOOP DE SIMULAÇÃO
% ---------------------------------------------------------
fprintf('Gerando arquivos em: %s\n', output_dir);

for k = 1:length(scenarios)
    s = scenarios(k);
    fprintf('Processando ts_cap%d.xlsx [%s] (Ts=%.1f)... ', s.id, s.desc, s.Ts);
    
    % --- INJETAR VARIÁVEIS NO WORKSPACE ---
    assignin('base', 'W', s.W);
    assignin('base', 'psiW', s.psiW);
    assignin('base', 'commande_cap', s.commande_cap);
    assignin('base', 'Ts', s.Ts); % <--- Ts DINÂMICO
    
    % Dummies
    assignin('base', 'xa', s.xa);
    assignin('base', 'ya', s.ya);
    assignin('base', 'rhoa', s.rhoa);
    
    % --- RODAR SIMULAÇÃO ---
    try
        sim('CaptCapModeleAvionNonLineaireDiscret');
    catch ME
        fprintf('\nERRO NO SIMULINK: %s\n', ME.message);
        continue; 
    end
    
    % --- EXTRAIR DADOS ---
    try
        t_vec = evalin('base', 'sim_psi.Time');
        n = length(t_vec);
        
        v_data   = evalin('base', 'TAS_m_s.Data');
        psi_data = evalin('base', 'sim_psi.Data');
        phi_data = evalin('base', 'sim_phi.Data');
        x_data   = evalin('base', 'sim_x.Data');
        y_data   = evalin('base', 'sim_y.Data');
        rr_data  = evalin('base', 'sim_roll_rate.Data');
        
        try, gamma_data = evalin('base', 'sim_gamma.Data'); catch, gamma_data = zeros(n,1); end
        
    catch ME
        fprintf('Erro ao extrair dados: %s\n', ME.message);
        continue;
    end

    % --- CRIAR VETORES ---
    wind_spd_vec = s.W * ones(n, 1);
    wind_dir_vec = s.psiW * ones(n, 1);
    c_cap_vec    = s.commande_cap * ones(n, 1);
    Ts_vec       = s.Ts * ones(n, 1); % <--- VETOR Ts DINÂMICO

    % --- MONTAR TABELA ---
    T = table(t_vec, v_data, psi_data, phi_data, x_data, y_data, gamma_data, rr_data, ...
              c_cap_vec, wind_spd_vec, wind_dir_vec, Ts_vec, ...
              'VariableNames', ...
              {'Time', 'TAS', 'Psi', 'Phi', 'X', 'Y', 'Gamma', 'Roll_rate', ...
               'Input_cap', 'Input_W', 'Input_PsiW', 'Input_Ts'});
           
    % --- SALVAR ---
    filename = sprintf('ts_cap%d.xlsx', s.id);
    full_path = fullfile(output_dir, filename);
    
    writetable(T, full_path);
    fprintf('OK\n');
end

disp('--- CONCLUÍDO ---');