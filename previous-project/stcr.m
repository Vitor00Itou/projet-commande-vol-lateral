%% Script Geração de Cenários ROUTE (Track Capture) - 10 CASOS
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
scenarios(idx).commande_route = 90;
scenarios(idx).W = 30 * KTS2MS;
scenarios(idx).psiW = 100 * DEG2RAD;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 4000; scenarios(idx).ya = 3500; scenarios(idx).rhoa = 120*DEG2RAD;

idx = idx + 1;
% CENÁRIO 2: Sem Vento (Track = Heading) (Ts = 0.6)
% Sem vento, a proa deve ser igual à rota comandada.
scenarios(idx).id = 2;
scenarios(idx).desc = 'Baseline_NoWind';
scenarios(idx).commande_route = 180;
scenarios(idx).W = 0;
scenarios(idx).psiW = 0;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 3: Drift Forte (Vento de Través 90 graus) (Ts = 0.6)
% Rota 90 (Leste), Vento do Norte (0). O avião tem que virar para a esquerda (Crab).
scenarios(idx).id = 3;
scenarios(idx).desc = 'Pure_Crosswind';
scenarios(idx).commande_route = 90;
scenarios(idx).W = 25 * KTS2MS;
scenarios(idx).psiW = 0 * DEG2RAD;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 4: Alta Velocidade (Tailwind) + Ts Lento (Ts = 1.0)
% Vento empurrando forte. O sistema fica mais instável com Ts alto.
scenarios(idx).id = 4;
scenarios(idx).desc = 'Tailwind_SlowTs';
scenarios(idx).commande_route = 90; % Voando Leste
scenarios(idx).W = 30 * KTS2MS;
scenarios(idx).psiW = 270 * DEG2RAD; % Vento vindo de Oeste (empurrando)
scenarios(idx).Ts = 1.0; % <--- Ts LENTO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 5: Baixa Velocidade (Headwind) + Ts Rápido (Ts = 0.4)
% Vento de cara. O avião fica "lento" em relação ao solo.
scenarios(idx).id = 5;
scenarios(idx).desc = 'Headwind_FastTs';
scenarios(idx).commande_route = 270; % Voando Oeste
scenarios(idx).W = 40 * KTS2MS;
scenarios(idx).psiW = 270 * DEG2RAD; % Vento vindo de Oeste (de cara)
scenarios(idx).Ts = 0.4; % <--- Ts RÁPIDO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 6: Correção Extrema (Vento Quase Máximo) (Ts = 0.6)
% 50 nós de vento lateral. Verifica se o ângulo de crab satura ou funciona.
scenarios(idx).id = 6;
scenarios(idx).desc = 'Extreme_Drift_Correction';
scenarios(idx).commande_route = 0; % Voando Norte
scenarios(idx).W = 50 * KTS2MS; 
scenarios(idx).psiW = 90 * DEG2RAD; % Vento de Leste
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 7: Cruzamento do Norte (Wrapping) (Ts = 0.8)
% Rota 350. Vento oblíquo.
scenarios(idx).id = 7;
scenarios(idx).desc = 'North_Crossing';
scenarios(idx).commande_route = 350;
scenarios(idx).W = 20 * KTS2MS;
scenarios(idx).psiW = 45 * DEG2RAD;
scenarios(idx).Ts = 0.8;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 8: Pequena Correção (Ts = 0.6)
% Rota 10 graus. Vento fraco.
scenarios(idx).id = 8;
scenarios(idx).desc = 'Small_Angle';
scenarios(idx).commande_route = 10;
scenarios(idx).W = 5 * KTS2MS;
scenarios(idx).psiW = 180 * DEG2RAD;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 9: Latência Crítica (Ts = 1.2)
% Teste de stress do integrador da malha de rota.
scenarios(idx).id = 9;
scenarios(idx).desc = 'Critical_Latency_Stress';
scenarios(idx).commande_route = 135;
scenarios(idx).W = 15 * KTS2MS;
scenarios(idx).psiW = 0;
scenarios(idx).Ts = 1.2; % <--- Ts MUITO LENTO
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

idx = idx + 1;
% CENÁRIO 10: Vento Variável (Simulado como oblíquo forte) (Ts = 0.6)
scenarios(idx).id = 10;
scenarios(idx).desc = 'Oblique_Strong_Wind';
scenarios(idx).commande_route = 45;
scenarios(idx).W = 35 * KTS2MS;
scenarios(idx).psiW = 300 * DEG2RAD;
scenarios(idx).Ts = 0.6;
scenarios(idx).xa = 0; scenarios(idx).ya = 0; scenarios(idx).rhoa = 0;

% ---------------------------------------------------------
% 3. LOOP DE SIMULAÇÃO
% ---------------------------------------------------------
fprintf('Gerando arquivos em: %s\n', output_dir);

for k = 1:length(scenarios)
    s = scenarios(k);
    fprintf('Processando ts_route%d.xlsx [%s] (Ts=%.1f)... ', s.id, s.desc, s.Ts);
    
    % --- INJETAR VARIÁVEIS NO WORKSPACE ---
    assignin('base', 'W', s.W);
    assignin('base', 'psiW', s.psiW);
    assignin('base', 'commande_route', s.commande_route);
    assignin('base', 'Ts', s.Ts); % <--- Ts DINÂMICO
    
    % Dummies
    assignin('base', 'xa', s.xa);
    assignin('base', 'ya', s.ya);
    assignin('base', 'rhoa', s.rhoa);
    
    % --- RODAR SIMULAÇÃO ---
    try
        sim('CaptRouteModeleAvionNonLineaireDiscret');
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
        
        try 
            gamma_data = evalin('base', 'sim_gamma.Data'); 
        catch
            gamma_data = zeros(n,1);
        end
        
    catch ME
        fprintf('Erro ao extrair dados: %s\n', ME.message);
        continue;
    end

    % --- CRIAR VETORES ---
    wind_spd_vec = s.W * ones(n, 1);
    wind_dir_vec = s.psiW * ones(n, 1);
    c_route_vec  = s.commande_route * ones(n, 1);
    Ts_vec       = s.Ts * ones(n, 1); % <--- VETOR Ts DINÂMICO

    % --- MONTAR TABELA ---
    T = table(t_vec, v_data, psi_data, phi_data, x_data, y_data, gamma_data, rr_data, ...
              c_route_vec, wind_spd_vec, wind_dir_vec, Ts_vec, ...
              'VariableNames', ...
              {'Time', 'TAS', 'Psi', 'Phi', 'X', 'Y', 'Gamma', 'Roll_rate', ...
               'Input_route', 'Input_W', 'Input_PsiW', 'Input_Ts'});
           
    % --- SALVAR ---
    filename = sprintf('ts_route%d.xlsx', s.id);
    full_path = fullfile(output_dir, filename);
    
    writetable(T, full_path);
    fprintf('OK\n');
end

disp('--- CONCLUÍDO ---');