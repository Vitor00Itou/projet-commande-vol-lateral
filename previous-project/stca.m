%% Script Geração de Cenários AXIS (EXPANDIDO COM VARIAÇÃO DE Ts)
clear; clc; warning('off');

% ---------------------------------------------------------
% 1. CONFIGURAÇÃO INTELIGENTE
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

% Constantes Locais
DEG2RAD = pi/180;
if exist('NM2M', 'var')
    KTS2MS = NM2M / 3600;
else
    KTS2MS = 0.514444;
end

% ---------------------------------------------------------
% 2. DEFINIÇÃO DOS CENÁRIOS
% ---------------------------------------------------------
% NOTA: Agora 'Ts' faz parte da struct para poder variar!

idx = 1;
% CENÁRIO 1: O Original (Ts = 0.6)
scenarios(idx).id = 1;
scenarios(idx).desc = 'Original_Request';
scenarios(idx).W = 30*KTS2MS;
scenarios(idx).psiW = 100*DEG2RAD;
scenarios(idx).xa = 4000;
scenarios(idx).ya = 3500;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 0.6;

idx = idx + 1;
% CENÁRIO 2: Baseline Padrão (Sem vento, Ts = 0.6)
scenarios(idx).id = 2;
scenarios(idx).desc = 'Baseline_NoWind';
scenarios(idx).W = 0;
scenarios(idx).psiW = 0;
scenarios(idx).xa = 4000;
scenarios(idx).ya = 3500;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 0.6;

idx = idx + 1;
% CENÁRIO 3: Crosswind Forte (Ts = 0.6)
scenarios(idx).id = 3;
scenarios(idx).desc = 'Strong_Crosswind';
scenarios(idx).W = 30 * KTS2MS;
scenarios(idx).psiW = 90 * DEG2RAD;
scenarios(idx).xa = 4000;
scenarios(idx).ya = 3500;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 0.6;

idx = idx + 1;
% CENÁRIO 4: Geometria Deslocada (Ts = 0.6)
scenarios(idx).id = 4;
scenarios(idx).desc = 'Offset_Geometry';
scenarios(idx).W = 10 * KTS2MS;
scenarios(idx).psiW = 180 * DEG2RAD;
scenarios(idx).xa = 1000;
scenarios(idx).ya = 2000;
scenarios(idx).rhoa = 90 * DEG2RAD;
scenarios(idx).Ts = 0.6;

idx = idx + 1;
% CENÁRIO 5: Slow Refresh Rate (Ts = 1.0) - Teste de Estabilidade
% Sem vento, mas com amostragem lenta.
scenarios(idx).id = 5;
scenarios(idx).desc = 'Slow_Refresh_Ts1.0';
scenarios(idx).W = 0;
scenarios(idx).psiW = 0;
scenarios(idx).xa = 7000;
scenarios(idx).ya = 3200;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 1.0; % <--- VARIAÇÃO AQUI

idx = idx + 1;
% CENÁRIO 6: Vento de Cauda (Tailwind) + Ts = 0.8
% Vento vindo de 300 graus (quase alinhado com a pista 120, empurrando)
scenarios(idx).id = 6;
scenarios(idx).desc = 'Tailwind_Ts0.8';
scenarios(idx).W = 20 * KTS2MS;
scenarios(idx).psiW = 300 * DEG2RAD; 
scenarios(idx).xa = 4000;
scenarios(idx).ya = 3500;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 0.8; % <--- VARIAÇÃO AQUI

idx = idx + 1;
% CENÁRIO 7: "A Tempestade Lenta" (Vento Forte + Ts Lento)
% Caso crítico: O controlador consegue manter com update lento e muito vento?
scenarios(idx).id = 7;
scenarios(idx).desc = 'Storm_Slow_Update';
scenarios(idx).W = 35 * KTS2MS; % Vento muito forte
scenarios(idx).psiW = 150 * DEG2RAD; % Vento oblíquo
scenarios(idx).xa = 4000;
scenarios(idx).ya = 3500;
scenarios(idx).rhoa = 120 * DEG2RAD;
scenarios(idx).Ts = 1.0; % <--- Pior caso de tempo
idx = idx + 1;

% CENÁRIO 8: Geometria Negativa/Invertida (Quadrante III)
% A pista começa em coordenadas negativas e aponta para Sudoeste (225 graus)
% O avião (0,0) está "na frente" e à direita da cabeceira.
scenarios(idx).id = 8;
scenarios(idx).desc = 'Negative_Coords_SW';
scenarios(idx).W = 15 * KTS2MS;
scenarios(idx).psiW = 180 * DEG2RAD; % Vento vindo do Sul
scenarios(idx).xa = -2000;
scenarios(idx).ya = -2000;
scenarios(idx).rhoa = 225 * DEG2RAD; % Pista aponta para SW
scenarios(idx).Ts = 0.6;

idx = idx + 1;
% CENÁRIO 9: "O Furacão" (Vento Extremo + Ts Lento)
% 45 Nós de vento cruzado com atualização de 0.9s.
% Teste de robustez máxima. Se oscilar muito, o ganho estático está alto.
scenarios(idx).id = 9;
scenarios(idx).desc = 'Hurricane_45kts_Ts0.9';
scenarios(idx).W = 45 * KTS2MS; 
scenarios(idx).psiW = 0 * DEG2RAD; % Vento vindo do Norte
scenarios(idx).xa = 4000;
scenarios(idx).ya = 1000;
scenarios(idx).rhoa = 90 * DEG2RAD; % Pista Leste (Vento bate de lado 90 graus)
scenarios(idx).Ts = 0.9;

idx = idx + 1;
% CENÁRIO 10: O Problema do Norte (355 graus)
% Teste de singularidade trigonométrica perto de 360/0 graus.
% Pista longe em Y, exigindo interceptação longa.
scenarios(idx).id = 10;
scenarios(idx).desc = 'North_Wrapping_Test';
scenarios(idx).W = 10 * KTS2MS;
scenarios(idx).psiW = 90 * DEG2RAD; % Vento de Leste
scenarios(idx).xa = 3000;
scenarios(idx).ya = -5000; % Muito deslocado para a direita
scenarios(idx).rhoa = 355 * DEG2RAD; % Quase Norte (355 graus)
scenarios(idx).Ts = 0.6;

% ---------------------------------------------------------
% 3. LOOP DE SIMULAÇÃO
% ---------------------------------------------------------
fprintf('Gerando arquivos em: %s\n', output_dir);

for k = 1:length(scenarios)
    s = scenarios(k);
    fprintf('Processando ts_axis%d.xlsx [%s] (Ts=%.1fs)... ', s.id, s.desc, s.Ts);
    
    % --- ASSIGNIN DINÂMICO ---
    assignin('base', 'W', s.W);
    assignin('base', 'psiW', s.psiW);
    assignin('base', 'xa', s.xa);
    assignin('base', 'ya', s.ya);
    assignin('base', 'rhoa', s.rhoa);
    assignin('base', 'Ts', s.Ts); % <--- Ts AGORA É DINÂMICO
    
    % --- RODAR SIMULAÇÃO ---
    try
        sim('CaptAxeModeleAvionNonLineaireDiscret');
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
            ey_data = evalin('base', 'sim_ey.Data');
        catch
            dx = x_data - s.xa;
            dy = y_data - s.ya;
            ey_data = -(dy).*cos(s.rhoa) + (dx).*sin(s.rhoa);
        end
        
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
    xa_vec       = s.xa * ones(n, 1);
    ya_vec       = s.ya * ones(n, 1);
    rhoa_vec     = s.rhoa * ones(n, 1);
    Ts_vec       = s.Ts * ones(n, 1); % <--- VETOR COM O Ts CORRETO

    % --- MONTAR TABELA ---
    T = table(t_vec, v_data, psi_data, phi_data, x_data, y_data, ey_data, gamma_data, rr_data, ...
              wind_spd_vec, wind_dir_vec, xa_vec, ya_vec, rhoa_vec, Ts_vec, ...
              'VariableNames', ...
              {'Time', 'TAS', 'Psi', 'Phi', 'X', 'Y', 'Ey', 'Gamma', 'Roll_rate', ...
               'Input_W', 'Input_PsiW', 'Input_Xa', 'Input_Ya', 'Input_Rhoa', 'Input_Ts'});
           
    % --- SALVAR ---
    filename = sprintf('ts_axis%d.xlsx', s.id);
    full_path = fullfile(output_dir, filename);
    
    writetable(T, full_path);
    fprintf('OK\n');
end
disp('--- CONCLUÍDO ---');