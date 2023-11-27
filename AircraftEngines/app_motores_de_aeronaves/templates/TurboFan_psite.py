import Prop2,re,math
from tabulate import tabulate
import numpy as np

def calcula_secao(dia_imp, pi_c, pi_0, h_pr, gamma_c, gamma_t, c_pc, c_pt, R_c, R_t, Tt4, alpha, eta_b, pi_dmax, eta_r, epson_f, epson_cL, epson_cH, epson_tH, eta_mH, epson_tL, eta_mL, P0_P9, T_0, P0_P19, P_0, m_0):

# Cálculo dos Parâmetros do Turbofan: Ideal, Não Ideal ou Off Design

# Inputs padrão da planilha
# Ordem dos diâmetros de Entrada (D_int D_ext H_anelar) [mm]
# [ Motor ; Admissão ; Fan ; Admissão do Turbojato ; Turbina de Alta ; Bocal do Turbojato ; Bocal do Fan ]
# dia_imp = [0 57 0 ; 0 36.8 0 ; 36.8 14.1 11.3 ; 22.1 17.2 2.5 ; 17.2 14.7 1.23 ; 23.3 19.0 2.1 ; 41.7 35.5 3.1];
# pi_c = 1.265;
# pi_0 = 1;
# h_pr = 4.2*1e7;
# gamma_c = 1.4;
# gamma_t = 1.3;
# c_pc = 1004;
# c_pt = 1100;
# R_c = 287;
# R_t = 291;
# Tt4 = 1850;
# alpha = 5;
# eta_b = 0.7;
# pi_dmax = 0.97;
# eta_r = 1;
# epson_f = 0.98;
# epson_cL = 0.95;
# epson_cH = 0.95;
# epson_tH = 0.95;
# eta_mH = 0.99;
# epson_tL = 0.95;
# eta_mL = 0.98;
# P0_P9 = 0.46;
# T_0 = 288.15;
# P0_P19 = 1;
# P_0 = 101325;
# m_0 = 242;

# Cálculo das Áreas das Seções
dia_SI = dia_imp * 0.0254
area = (np.pi / 4) * dia_SI[:, 0:2] ** 2
area = np.column_stack([area, [0, 0, np.subtract(area[2:7, 0], area[2:7, 1])]])
area_fan = area[2, 2] - area[3, 2]

# Cálculo dos pi's Iniciais
# Compressor de Alta e de Baixa divididos em 3 e 9 seções, respectivamente
pi_fR = pi_0 * 1.7
comp_L = [pi_fR * pi_c, pi_fR * pi_c ** 2, pi_fR * pi_c ** 3]
comp_H = [pi_fR * pi_c ** 4, pi_fR * pi_c ** 5, pi_fR * pi_c ** 6, pi_fR * pi_c ** 7, pi_fR * pi_c ** 8,
  pi_fR * pi_c ** 9, pi_fR * pi_c ** 10, pi_fR * pi_c ** 11, pi_fR * pi_c ** 12]
pi_cL = pi_c ** 3
pi_cH = pi_c ** 9
pi_C = pi_cL * pi_cH

# Cálculo do Ponto de Projeto
# Organização das Seções/Parâmetros
#                                         Estágio  Pi  Tau  P_t(Pa)  T_t(K)  P(Pa)  T(K)  M  P(bar)  T(°C)  
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

tau_f = pi_fR**((gamma_c-1)/gamma_c/epson_f)

tau_cL = pi_cL**((gamma_c-1)/gamma_c/epson_cL)

f = ((Tt4*c_pt/(T_0*c_pc))-(1+(gamma_c-1)/2*0.01*0.01*(pi_dmax*eta_r)**((gamma_c-1)/gamma_c)*pi_fR**((gamma_c-1)/(gamma_c*epson_f))*pi_cL**((gamma_c-1)/(gamma_c*epson_cL))*pi_cH**((gamma_c-1)/gamma_c/epson_cH)))/(eta_b*h_pr/c_pc/T_0-(Tt4*c_pt/(T_0*c_pc)))

tau_tH = 1-((pi_cH**((gamma_c-1)/gamma_c/epson_cH))-1)/(1+f)/(Tt4*c_pt/(T_0*c_pc))*(1+(gamma_c-1)/2*0.01*0.01)*((pi_dmax*eta_r)**((gamma_c-1)/gamma_c))*tau_f*tau_cL*eta_mH

tau_lambda = Tt4*c_pt/(T_0*c_pc)

tau_tL = 1-((alpha*(tau_f-1)+(tau_cL-1))*eta_mL/(1+f)*(1+((gamma_c-1)/2*0.01**2))*((pi_dmax*eta_r)**((gamma_c-1)/gamma_c))/tau_lambda/tau_tH)

Pt9_P9 = P0_P9*(((1+(gamma_c-1)/2*0.01**2)**(gamma_c/(gamma_c-1)))*pi_dmax*eta_r*pi_fR*pi_cL*pi_cH*0.98*((tau_tH)**(gamma_t/(gamma_t-1)/epson_tH))*((tau_tL)**(gamma_t/(gamma_t-1)/epson_tL))*0.92*1)

Tt9_T0 = c_pc/c_pt*tau_lambda*tau_tL*1*1

T9_T0 = Tt9_T0/Pt9_P9**((gamma_t-1)/gamma_t)

Pt19_P19 = P0_P19*((1+(gamma_c-1)/2*0.01**2)**(gamma_c/(gamma_c-1)))*pi_dmax*eta_r*pi_fR*0.99

Tt19_T0 = (1+(gamma_c-1)/2*0.01**2)*((pi_dmax*eta_r)**((gamma_c-1)/gamma_c))*(pi_fR**((gamma_c-1)/(gamma_c*epson_f)))*1

T19_T0 = Tt19_T0/Pt19_P19**((gamma_c-1)/gamma_c)

V19_a0 = (np.sqrt(2/(gamma_c-1)*(Pt19_P19**((gamma_c-1)/gamma_c)-1)))*np.sqrt(T19_T0)

M = np.array([0, 0.01, 0.4, 0.4, 0.4, 0.4, 0.5, 0.5, 0.5, 1, (np.sqrt(2/(gamma_c-1)*(Pt9_P9**((gamma_c-1)/gamma_c)-1))), 0.5, np.sqrt(2/(gamma_c-1)*(Pt19_P19**((gamma_c-1)/gamma_c)-1)), np.sqrt(2/(gamma_c-1)*(Pt19_P19**((gamma_c-1)/gamma_c)-1))])

V9_a0 = M[9]*np.sqrt(T9_T0)

tau = np.array([1, 1+(gamma_c-1)/2*M[1]*M[1], (pi_dmax*eta_r)**((gamma_c-1)/gamma_c), pi_fR**((gamma_c-1)/(gamma_c*epson_f)), pi_cL**((gamma_c-1)/(gamma_c*epson_cL)), pi_cH**((gamma_c-1)/gamma_c/epson_cH), tau_tH, tau_tL, 1, 1, pi_fR**((gamma_c-1)/(gamma_c*epson_f)), 1, 1])

tau = np.concatenate([tau[:6], Tt4/(T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]), tau[6:13]])

T_t = np.array([T_0, T_0*tau[2], T_0*tau[2]*tau[3], T_0*tau[2]*tau[3]*tau[4], T_0*tau[2]*tau[3]*tau[4]*tau[5], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]*tau[7], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]*tau[7]*tau[8], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]*tau[7]*tau[8]*tau[9], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]*tau[7]*tau[8]*tau[9]*tau[10], T_0*tau[2]*tau[3]*tau[4]*tau[5]*tau[6]*tau[7]*tau[8]*tau[9]*tau[10]*tau[11], T_0*tau[2]*tau[3]*tau[4], T_0*tau[2]*tau[3]*tau[4]*tau[13], T_0*tau[2]*tau[3]*tau[4]*tau[13]*tau[14]])

pi = np.array([pi_0, tau[2]**(gamma_c/(gamma_c-1)), pi_dmax*eta_r, pi_fR, pi_cL, pi_cH, 0.98, tau[8]**(gamma_t/(gamma_t-1)/epson_tH), tau[9]**(gamma_t/(gamma_t-1)/epson_tL), 0.92, 1, pi_fR, 0.99, 1])

P_t = np.array([P_0, P_0*pi[2], (P_0*pi[2])*pi[3], ((P_0*pi[2])*pi[3])*pi[4], (((P_0*pi[2])*pi[3])*pi[4])*pi[5], ((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6], (((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6])*pi[7], ((((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6])*pi[7])*pi[8], (((((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6])*pi[7])*pi[8])*pi[9], ((((((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6])*pi[7])*pi[8])*pi[9])*pi[10], (((((((((P_0*pi[2])*pi[3])*pi[4])*pi[5])*pi[6])*pi[7])*pi[8])*pi[9])*pi[10])*pi[11], ((P_0*pi[2])*pi[3])*pi[4], (((P_0*pi[2])*pi[3])*pi[4])*pi[13], ((((P_0*pi[2])*pi[3])*pi[4])*pi[13])*pi[14]])

P_Pa = P_t/(1+(gamma_c-1)/2*M[1]**2)**(gamma_c/(gamma_c-1))

T_K = T_t/(1+(gamma_c-1)/2*M[1]**2)

P_bar = P_Pa/100000

T_C = T_K - 273.15

a_0 = np.sqrt(gamma_c*R_c*T_K[2])

Ff_mdot0 = alpha/(1+alpha)*a_0*(V19_a0-M[2])

Fc_mdot0 = 1/(1+alpha)*alpha*((1+f)*V9_a0-M[2])

F_m0 = Ff_mdot0+Fc_mdot0

S = f/(1+alpha)/F_m0

eta_t = a_0*a_0*((1+f)*V9_a0*V9_a0+alpha*V19_a0*V19_a0-(1+alpha)*M[2]**2)/(2*f*h_pr)*100

eta_p = 2*M[2]*((1+f)*V9_a0+alpha*V19_a0-(1+alpha)*M[2])/((1+f)*V9_a0*V9_a0+alpha*V19_a0*V19_a0-(1+alpha)*M[2]**2)*100

eta_0 = eta_t*eta_p/100

F_ratio = Ff_mdot0/Fc_mdot0

F = F_m0*m_0

F_C = S*F

AF_ratio = 1/f

m_c = m_0*1/(alpha+1)

m_f = m_0*alpha/(alpha+1)

eta_f = (pi_fR**((gamma_c-1)/gamma_c)-1)/(tau_f-1)

eta_cL = (pi_cL**((gamma_c-1)/gamma_c)-1)/(tau_cL-1)

pi_tL = tau_tL**(gamma_t/(gamma_t-1)/epson_tL)

eta_tL = (tau_tL-1)/(pi_tL**((gamma_t-1)/gamma_t)-1)

tau_cH = pi_cH**((gamma_c-1)/gamma_c/epson_cH)

eta_cH = (pi_cH**((gamma_c-1)/gamma_c)-1)/(tau_cH-1)

pi_tH = tau_tH**(gamma_t/(gamma_t-1)/epson_tH)

eta_tH = (tau_tH-1)/(pi_tH**((gamma_t-1)/gamma_t)-1)

tau_cHR = pi_cH**((gamma_c-1)/gamma_c)

tau_r = 1+(gamma_c-1)/2*M[2]**2

pi_r = tau_r**(gamma_c/(gamma_c-1))



# Organização dos Resultados

# Geometria
Geometria = {
'areas': area,
'area_fan': area_fan,
'bypass': alpha
}

# Compressão
Compressao = {
'pi_c': pi_c,
'pi_0': pi_0,
'pi_fR': pi_fR,
'pi_cL': pi_cL,
'pi_cH': pi_cH,
'pi_C': pi_C,
'Baixa_Pressao': comp_L.tolist(),
'Alta_Pressao': comp_H.tolist()
}

# Ponto Projeto
PontoProjeto = {
'Secoes': [secao, pi, tau, P_t, T_t, P_Pa, T_K, M, P_bar, T_C],
'SaidaTurboJato': {
'P0_P9': P0_P9,
'Pt9_P9': Pt9_P9,
'Tt9_T0': Tt9_T0,
'T9_T0': T9_T0,
'V9_a0': V9_a0
},
'SaidaFan': {
'P0_P19': P0_P19,
'Pt19_P19': Pt19_P19,
'Tt19_T0': Tt19_T0,
'T19_T0': T19_T0,
'V19_a0': V19_a0
},
'Resultados': {
'a0': a_0,
'F_m0': F_m0,
'S': S,
'eta_t': eta_t,
'eta_p': eta_p,
'eta_0': eta_0,
'Ff_mdot0': Ff_mdot0,
'Fc_mdot0': Fc_mdot0,
'F_ratio': F_ratio,
'm_0': m_0,
'F': F,
'F_C': F_C,
'AF_ratio': AF_ratio,
'm_c': m_c,
'm_f': m_f,
'alpha': alpha
}
}

# Compressor Turbina de Baixa
CompressorTurbinaL = {
'Fan': {
'Pi_f': pi_fR,
'Tau_f': tau_f,
'epson_f': epson_f,
'eta_f': eta_f
},
'CompressorBaixaPressao': {
'Pi_cL': pi_cL,
'Tau_cL': tau_cL,
'epson_cL': epson_cL,
'eta_cL': eta_cL
},
'TurbinaBaixaPressao': {
'Pi_tL': pi_tL,
'Tau_tL': tau_tL,
'epson_tL': epson_tL,
'eta_tL': eta_tL
},
'Dados': {
'Tau_cL': tau_cL,
'Tau_lambda': tau_lambda,
'Tau_r': tau[1],
'Tau_d': tau[2],
'Tau_f': tau_f,
'Tau_tH': tau_tH,
'alpha': alpha,
'f': f,
'eta_mL': eta_mL
}
}

# Compressor Turbina de Alta
CompressorTurbinaH = {
'CompressorAltaPressao': {
'Pi_cH': pi_cH,
'Tau_cH': tau_cH,
'epson_cH': epson_cH,
'eta_cH': eta_cH
},
'TurbinaAltaPressao': {
'Pi_tH': pi_tH,
'Tau_tH': tau_tH,
'epson_tH': epson_tH,
'eta_tH': eta_tH
},
'Dados': {
'Tau_cH': tau_cH,
'Tau_lambda': tau_lambda,
'Tau_r': tau[1],
'Tau_d': tau[2],
'Tau_f': tau_f,
'Tau_cL': tau_cL,
'f': f,
'eta_mH': eta_mH
}
}

# Fora Ponto Projeto
ForaPontoProjeto = {
'Dados' : {
'eta_cH': eta_cH,
'eta_f': eta_f,
'Pi_rT': pi[1],
'Pi_dR': pi[2],
'Pi_fR': pi_fR,
'Pi_cHR': pi_cH,
'Pi_tLR': pi_tL,
'Tau_rR': tau[2],
'Tau_fR': tau[4],
'Tau_cHR': tau_cHR,
'Tau_tLR': tau_tL,
'alpha_R': alpha,
'M_9R': M[11],
'M_19R': M[14],
'Tau_lambdaR': tau_lambda,
'Tt_4R': Tt4,
'gamma_c': gamma_c,
'R_c': R_c,
'gamma_t': gamma_t,
'R_t': R_t,
'a_0': a_0
},

'Resultados' : {
 'M_0' : M[1],
 'V_0' : a_0 * M[1],
 'Tau_r' : tau_r,
 'Pi_r' : pi_r,
 'eta_r' : eta_r,
 'Tt_4' : Tt4 / 2,
 'Pi_d' : eta_r * 1,
 'Tau_Lambda' : c_pt * (Tt4 / 2) / c_pc / T_K[0],
 'Pi_tL' : pi_tL,
 'Pi_cL' : 0.3,
 'Pi_fn' : 0.99,
 'Pt19_P0' : pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99,
 'Pt19_P0critico' : ((gamma_c + 1) / 2) ** (gamma_c / (gamma_c)),
 'Pt19_P19' : pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99,
 'Pi_b' : pi[6],
 'Pi_tH' : pi_tH,
 'Pi_n' : pi[9],
 'Pt9_P0' : pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.3 * ((1 + ((1 + (c_pt * (Tt4 / 2) / c_pc / T_K[0]) / tau_r / (tau_lambda / tau[1]) * (tau_cHR - 1)) - 1) * eta_cH) ** (gamma_c / (gamma_c - 1))) * pi[6] * pi_tL * pi_tL * pi[9],
 'Pt9_P0critico' : ((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1)),
 'Pt9_P9' : ((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1)),
 'mdot_0' : ((pi_dmax) / (pi[2])) * sqrt((Tt4 / 2) / Tt4),
 'T9_T0' : ((c_pt * (Tt4 / 2) / c_pc / T_K[0]) * tau_tH * tau_tL / ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t))) * (c_pc / c_pt),
 'V9_a0' : (sqrt(2 / (gamma_t - 1) * ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t) - 1))) * sqrt(gamma_t * R_t * (((c_pt * (Tt4 / 2) / c_pc / T_K[0]) * tau_tH * tau_tL / ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t))) * (c_pc / c_pt)) / (gamma_c * R_c)),
 'T19_T0' : tau_r * tau_f / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c)),
 'V19_a0' : (sqrt(2 / (gamma_c - 1) * ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c) - 1))) * (tau_r * tau_f / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c))),
 'F_mdot0' : ((1 / (1 + alpha)) * a_0 * ((1 + ((c_pt * (Tt4 / 2) / c_pc / T_K[0]) - tau_r * tau_cL * (1 + (c_pt * (Tt4 / 2) / c_pc / T_K[0]) / tau_r / (tau_lambda / tau[1]) * (tau_cHR - 1))) / (h_pr * eta_b / (c_pc * T_0) - (c_pt * (Tt4 / 2) / c_pc / T_K[0]))) * ((sqrt(2 / (gamma_t - 1) * ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t) - 1))) * sqrt(gamma_t * R_t * (((c_pt * (Tt4 / 2) / c_pc / T_K[0]) * tau_tH * tau_tL / ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t))) * (c_pc / c_pt)) / (gamma_c * R_c))) - M[1] + (1 + (((c_pt * (Tt4 / 2) / c_pc / T_K[0]) - tau_r * tau_cL * (1 + (c_pt * (Tt4 / 2) / c_pc / T_K[0]) / tau_r / (tau_lambda / tau[1]) * (tau_cHR - 1))) / (h_pr * eta_b / (c_pc * T_0) - (c_pt * (Tt4 / 2) / c_pc / T_K[0])))) * (R_t / R_c) * ((((c_pt * (Tt4 / 2) / c_pc / T_K[0]) * tau_tH * tau_tL / ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t))) * (c_pc / c_pt)) / ((sqrt(2 / (gamma_t - 1) * ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t) - 1))) * sqrt(gamma_t * R_t * (((c_pt * (Tt4 / 2) / c_pc / T_K[0]) * tau_tH * tau_tL / ((((gamma_t + 1) / 2) ** (gamma_t / (gamma_t - 1))) ** ((gamma_t - 1) / gamma_t))) * (c_pc / c_pt)) / (gamma_c * R_c)))) * ((1 - (1 / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.3 * ((1 + ((1 + ((c_pt * (Tt4 / 2) / c_pc / T_K[0]) - tau_r * tau_cL * (1 + (c_pt * (Tt4 / 2) / c_pc / T_K[0]) / tau_r / (tau_lambda / tau[1]) * (tau_cHR - 1)) - 1) * eta_cH) ** (gamma_c / (gamma_c - 1))) * pi[6] * pi_tL * pi_tL * pi[9])))))) / gamma_c) + (alpha / (1 + alpha)) * a_0 * (((sqrt(2 / (gamma_c - 1) * ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c) - 1))) * (tau_r * tau_f / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c)))) - M[1] + ((tau_r * tau_f / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / ( gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c))) / ((sqrt(2 / (gamma_c - 1) * ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c) - 1))) * (tau_r * tau_f / ((pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99) ** ((gamma_c - 1) / gamma_c)))))) * ((1 - ((1) / (pi_r * eta_r * 1 * ((1 + (tau_f - 1) * eta_f) ** (gamma_c / (gamma_c - 1))) * 0.99)))) / gamma_c)),
 'F': F,
 'm0': m0,
 'f': f,
 'S': S,
 'eta_T': eta_T,
 'eta_P': eta_P,
 'eta_Total': eta_Total,
 'alpha': alpha,
 'pi_f': pi_f,
 'pi_cH': pi_cH,
 'pi_tL': pi_tL,
 'tau_f': tau_f,
 'tau_cH': tau_cH,
 'tau_tL': tau_tL,
 'M9': M9,
 'M19': M19,
 'N_fan': N_NR_fan,
 'N_hp_spool': N_NR_H
}
}

    return Geometria, Compressao, PontoProjeto, CompressorTurbinaL, CompressorTurbinaH, ForaPontoProjeto 
