%% Modelling and control of point mass aircraft model
%
%%
%clear
%close all
%bdclose all
warning('off')


% ... (Seu código de constantes continua igual até aqui) ...
% Periode echantillonnage
Ts = 0.6; % sec



% --- RODA A SIMULAÇÃO ---
% (Isso garante que os dados 'out' ou variáveis existam no Workspace)
sim('CaptAxeModeleAvionNonLineaireDiscret'); 

% --- PREPARAÇÃO DOS DADOS ---
% Nota: Dependendo da sua versão do Matlab/Simulink, os dados podem vir 
% dentro de um objeto 'out'. Ajuste conforme necessário (ex: out.sim_psi).
% Estou assumindo que você usou "To Workspace" com formato "Array" ou "Timeseries".

% 1. Pegar o tempo (basta de uma das variáveis)
t_vec = sim_psi.Time; 
n = length(t_vec);

% 2. Pegar as variáveis dinâmicas (verifique se os nomes batem com seus blocos To Workspace)
psi_data = sim_psi.Data;
phi_data = sim_phi.Data;
x_data   = sim_x.Data;
y_data   = sim_y.Data;
ey_data  = sim_ey.Data;  % O erro lateral calculado no Simulink
v_data   = TAS_m_s.Data; % Sua velocidade

% 3. Criar vetores de constantes (Cenário) para o Python ler
% Isso é o "Pulo do Gato" para o teste automático saber o gabarito
wind_spd_vec = W * ones(n, 1);
wind_dir_vec = psiW * ones(n, 1);
xa_vec       = xa * ones(n, 1);
ya_vec       = ya * ones(n, 1);
rhoa_vec     = rhoa * ones(n, 1);
Ts_vec       = Ts * ones(n,1);

% --- CRIAÇÃO DA TABELA ---
T = table(t_vec, v_data, psi_data, phi_data, x_data, y_data, ey_data, ...
          wind_spd_vec, wind_dir_vec, xa_vec, ya_vec, rhoa_vec, Ts_vec, ...
          'VariableNames', ...
          {'Time', 'TAS', 'Psi', 'Phi', 'X', 'Y', 'Ey', ...
           'Input_W', 'Input_PsiW', 'Input_Xa', 'Input_Ya', 'Input_Rhoa', 'Input_Ts'});

% --- SALVAR EXCEL ---
filename = 'Ts_axis1.xlsx';
writetable(T, filename);
disp(['Dados salvos com sucesso em: ', filename]);