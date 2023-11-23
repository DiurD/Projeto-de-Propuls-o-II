import Prop2,re,math
from tabulate import tabulate
import numpy as np

# Cálculo das Áreas das Seções
# Ordem dos diâmetros de Entrada (D_int D_ext H_anelar) [mm]
# [ Motor ; Admissão ; Fan ; Admissão do Turbojato ; Turbina de Alta ; Bocal do Turbojato ; Bocal do Fan ]
dia_imp = np.array([[0, 57, 0],
                    [0, 36.8, 0],
                    [36.8, 14.1, 11.3],
                    [22.1, 17.2, 2.5],
                    [17.2, 14.7, 1.23],
                    [23.3, 19.0, 2.1],
                    [41.7, 35.5, 3.1]])

dia_SI = dia_imp * 0.0254
area = (np.pi / 4) * dia_SI[:, 0:2]**2
area = np.column_stack([area, [0, 0, *area[2:7, 0] - area[2:7, 1]]])

# Cálculo dos pi's Iniciais
# Compressor de Alta e de Baixa divididos em 3 e 9 seções respectivamente
pi_c = 1.265
pi_0 = 1

pi_fR = pi_0 * 1.7
comp_L = np.array([pi_fR * pi_c, pi_fR * pi_c**2, pi_fR * pi_c**3])
Comp_H = np.array([pi_fR * pi_c**4, pi_fR * pi_c**5, pi_fR * pi_c**6, pi_fR * pi_c**7,
                   pi_fR * pi_c**8, pi_fR * pi_c**9, pi_fR * pi_c**10, pi_fR * pi_c**11, pi_fR * pi_c**12])
pi_cL = pi_c**3
pi_cH = pi_c**9
pi_c = pi_cL * pi_cH

# Cálculo do Ponto de Projeto
h_pr = 4.2 * 10e7
gamma_c = 1.4
gamma_t = 1.3
c_pc = 1004
c_pt = 1100
R_c = 287
R_t = 291
Tt4 = 1850
alpha = 5
eta_b = 0.7
pi_dmax = 0.97
eta_r = 1
epson_f = 0.98
epson_cL = 0.95
epson_cH = 0.95
epson_tH = 0.95
eta_mH = 0.99
epson_tL = 0.95
eta_mL = 0.95

# Organização das Seções/Parâmetros
#                                         Índice  Pi  Tau  P_t(Pa)  T_t(K)  P(Pa)  T(K) M  
# Escoamento livre (0)
# Entrada de ar ( r)
# Entrada do fan (d)
# Saída do fan (f)
# Saída do compressor  de baixa (c L)
# Saída do Compressor de alta (c H)
# Saída da câmara de combustão (b)
# Saída da turbina de alta pressão (t H)
# Saída da turbina de baixa (t L)
# Garganta da tubeira 
# Saída da tubeira (n)
# Saída do fan (f)
# Garganta da tubeira  fan 
# Saída da tubeira fan (fn)

secao = np.array([0, 1, 2, 2.1, 2.5, 3, 4, 4.5, 5, 8, 9, 13, 18, 19])
Pt9_P9 =  # Preencha o valor adequado aqui
M = np.array([0, 0.01, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 1, (np.sqrt(2 / (gamma_c - 1) * (Pt9_P9 ** ((gamma_c - 1) / gamma_c) - 1)))])
Tt = np.array([288.15])  # Preencha o valor adequado aqui
tau_lambda = Tt4 * c_pt / (Tt[0] * c_pc)
tau_tH = 1 - ((pi_cH ** ((gamma_c - 1) / gamma_c / epson_cH)) - 1) / (1 + D20) / tau_lambda * (
        1 + (gamma_c - 1) / 2 * M[1] * M[1]) * ((pi_dmax * eta_r) ** ((gamma_c - 1) / gamma_c)) * D18 * D19 * D21
tau = np.array([1, 1 + (gamma_c - 1) / 2 * M[1] * M[1], (pi_dmax * eta_r) ** ((gamma_c - 1) / gamma_c),
                pi_fR ** ((gamma_c - 1) / (gamma_c * epson_f)), pi_cL ** ((gamma_c - 1) / (gamma_c * epson_cL)),
                pi_cH ** ((gamma_c - 1) / gamma_c / epson_cH), Tt4 / Tt[5], 4.5, 5, 1, 1,
                pi_fR ** ((gamma_c - 1) / (gamma_c * epson_f)), 1, 1])
pi = np.array([pi_0, tau[1] ** (gamma_c / (gamma_c - 1)), pi_dmax * eta_r, pi_fR, pi_cL, pi_cH, 0.98,
               tau[7] ** (gamma_t / (gamma_t - 1) / epson_tH), tau[8] ** (gamma_t / (gamma_t - 1) / epson_tL), 0.92, 1,
               pi_fR ** ((gamma_c - 1) / (gamma_c * epson_f)), 0.99, 1])