import re,math
# import Prop2
from app_motores_de_aeronaves.templates import Prop2

class motor_turboprop:
    
    def __init__(self,name,M0):
        print("*** Criando um novo motor turboprop. Defina seus parâmetros a seguir: ***\n")
        self.name = name
        #self.length = lenght
        self.M0 = M0
        #self.M3 = M3
        #self.D = diameters
        self.A=[float(0)]*11
        #self.airIntakes = intakes


    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,m0_dot,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL):
        

        T0,P0,_,_ = atmos.get_param()
        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11

        Ms = [float(1)]*11
        Ms[0] = self.M0
        #Ms[1] = self.M0
        #Ms[2] = 0.9*self.M0 #Pequena redução arbitrária de Mach antes de entrar no compressor.
        #Ms[3] = self.M3
        #Ms[4] = 1 #Página 562 Mattingly
        #Ms[5] = 1 #Página 562 Mattingly
            
        
       #output,tau_lambda,pi_r,  tau_r,  pi_d,  tau_d,  pi_c,  tau_c,  pi_b,  tau_b,  pi_tH, tau_tH, pi_tL, tau_tL, pi_n,  tau_n,  P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
        if ideal:     
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos.ideal_turboprop(self.M0,gamma_c,cp_c,hpr,Tt4,pi_c,tau_t,eta_prop)    
        else:
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos.real_turboprop(self.M0,Tt4,gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_n,pi_c,e_c,e_tH,e_tL,tau_t,eta_b,eta_mL,eta_mH,eta_g,eta_prop,m0_dot)
        
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9]
        output['Pt9/P9'] = [Pt9_P9]
        output['T9/Tt9'] = [T9_Tt9]
        output['T9/T0'] = [T9_T0]



        for i in range(len(secao)):
            if i<4:
                gamma = gamma_c
            else:
                gamma = gamma_t

            if i == 0:
                Pts[i] = pis[i]*P0
                Tts[i] = taus[i]*T0
                Ps[i] = P0
                Ts[i] = T0
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]

        Ps[10] = Pts[10]/Pt9_P9
        Ts[10] = Ts[0]*T9_T0
        Ms[10] = M9 # Já pego o Mach 9 do resultado do programa, o Mach[10] aqui que é o Mach 9 no caso, pq tem uma seção a mais no motor, a 4,5 relativa a entrada da turbina de baixa. Esse trecho diz que o Mach 5 do Mattingly (Mach[6] do programa), depois de sair da turbina continua o mesmo até o final.

        

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'Tt [K]': Tts,
        'Mach0': Ms[0],
        'Mach9': Ms[10],
        'T0 [K]': T0,
        'P0 [Pa]': P0,
        }

        return output,saidas
    
    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,Tt4_AT,M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH,design:bool, eta_c, eta_tL,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL,tau_t_R,eta_nt):

        secao = [0,    2 ,  3  ,  4  , 4.5 ,  5  ,  8   ,9]
        datum = [0, 0.060,0.408,0.616,0.679,0.715,0.9498,1]


        output_Mattingly_REF= {}
        saida_REF = {}

        if design:                                                                                                                                                
            output_Mattingly,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_AT, pi_c_R, tau_t, eta_prop,atmos_AT,ideal,m0_dot_R,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL)
        else:                                               
            output_Mattingly,saida,output_Mattingly_REF,saida_REF = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t ,hpr, tau_t_R,eta_prop,eta_propmax,pi_tH,tau_tH,atmos_REF,atmos_AT,ideal,M0_AT,Tt4_AT, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R,eta_c, eta_tL,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL)

        nova_saida = {
        'Section': secao,
        'Datum':datum,
        'Pt [Pa]':[],
        'Tt [K]':[],
        }

        P_c = saida['Pt [Pa]'][6]*(1-1/eta_nt*((gamma_t-1)/(gamma_t+1)))**((gamma_t)/(gamma_t-1))
        output_Mattingly['P_c'] = P_c

        for i in range(1):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])
        
        for i in range(2,7):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

        for i in range(9,11):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

            return output_Mattingly,saida,output_Mattingly_REF,saida_REF,nova_saida
                                                                                                                                                                                                                   
    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr, tau_t_R, eta_prop, eta_propmax, pi_tH, tau_tH, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,Tt4_AT,M0_R,T0_R,P0_R,m0_dot_R, tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,pi_tL_R,tau_tL_R,M9_R,Pt9_P9_R,eta_c, eta_tL, pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL):
                                                                                                                                                                                                                                                                                                                                     
        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
       # pis[4] = pi_b ; pis[9] = pi_n
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11
        output_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        saida_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        
        
        T0,P0,_,_ = atmos_AT.get_param()

                                                #(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,  pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):                                     
        output_REF,saida_REF = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,pi_c_R, tau_t_R, eta_prop,atmos_REF,                  ideal,m0_dot_R,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL)
        
        if Pt9_P9_R == 1 and m0_dot_R ==1:                                                                                                                                                                                                          #pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax,saida_REF['Mach0'][0],saida_REF['T0 [K]'][0],saida_REF['P0 [Pa]'][0],output_REF['m0_dot'][0],saida_REF['Tau'][0],saida_REF['Pi'][0],saida_REF['Tt [K]'][4],saida_REF['Pi'][2],saida_REF['Pi'][3],saida_REF['Tau'][3],saida_REF['Pi'][5],saida_REF['Tau'][5],saida_REF['Mach9'][0],output_REF['Pt9/P9'][0])
        else:                                                                                                                                                                                                                                                     #pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R                                                                                                                                                                                                                                                
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R)


        Ms = [float(1)]*11
        
        Ms[0] = M0_AT
       # Ms[1] = M0_AT
       # Ms[2] = 0.9*M0_AT
       # Ms[3] = self.M3
       # Ms[4] = 1 #Página 562 Mattingly
       # Ms[5] = 1 #Página 562 Mattingly    
       # Ms[6] = Ms[7] = Ms[8] = Ms[9] = Ms[10] = M9 # Desconsiderar mudança de Mach após sair da turbina, ao longo do bocal de saída
        Ms[10] = M9
        
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9]
        output['Pt9/P9'] = [Pt9_P9]
        output['T9/Tt9'] = [T9_Tt9]
        output['T9/T0'] = [T9_T0]
        


        for i in range(len(secao)):
            if i<4:
                gamma = gamma_c
            else:
                gamma = gamma_t

            if i == 0:
                Pts[i] = pis[i]*P0
                Tts[i] = taus[i]*T0
                Ps[i] = P0
                Ts[i] = T0
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
        

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'Tt [K]': Tts,
        'Mach0': Ms[0],
        'Mach9': Ms[10],
        }


        return output,saidas,output_REF,saida_REF


        
        

#tutu = motor_turboprop('tutu',0.8)


#CALCULO IDEAL ON DESIGN
#print('Ideal on design \n')
#atmosfera = Prop2.AircraftEngines(7600)
#gamma_c = 1.4
#gamma_t = 1.4
#cp_c = 1.004
#cp_t = 1.004
#hpr = 42800
#ideal = True
#Tt4 = 1370
#eta_prop = 0.83
#pi_c = 20
#tau_t = 0.6
#m0_dot = 15

#print(tutu.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmosfera,ideal,m0_dot))

# CALCULO NAO IDEAL ON DESIGN#print('Nao ideal on design \n')
#atmosfera = Prop2.AircraftEngines(0)
#gamma_c = 1.4
#gamma_t = 1.35
#cp_c = 1.004
#cp_t = 1.235
#hpr = 42800
#Tt4 = 1670
#pi_c = 30
#tau_t = 0.55
#eta_prop = 0.812
#ideal = False
#m0_dot = 14.55
#pi_b = 0.94
#pi_d_max = pi_d = 0.98
#pi_n = 0.99
#eta_b = 0.995
#eta_mL = 0.995
#eta_mH = 0.995
#eta_g = 0.99
#e_c = 0.90
#e_tH = 0.89
#e_tL = 0.91

#print(tutu.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,pi_c, tau_t, eta_prop,atmosfera,ideal,m0_dot,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL))





# Teste Offdesign

#print('começa daqui \n')
#gamma_c = 1.4
#gamma_t = 1.3
#cp_c = 1.004
#cp_t = 1.235
#hpr = 42800
#pi_c_R = 30
#tau_t_R = tau_t = 0.55
#eta_prop = 0.812
#eta_propmax = 0.812
#pi_tH = 0.2212
#tau_tH = 0.7336
#m0_dot_R = 14.55
#atmos_REF = Prop2.AircraftEngines(0)
#atmos_AT = Prop2.AircraftEngines(6000)
#ideal = False
#M0_AT = 0.6
#Tt4_AT = 1670
#M0_R = 0.1
#T0_R = 288.2
#P0_R = 101300
#tau_r_R = 1.002
#pi_r_R = 1.007
#Tt4_R = 1670
#pi_d_R = 0.98
#tau_c_R = 2.6426
#pi_tL_R = 0.2537
#tau_tL_R = 0.7497
#M9_R = 1 ##
#Pt9_P9_R = 1.89 ##
#eta_c = 0.845
#eta_tL = 0.9224
#pi_b = 0.94
#pi_d_max = 0.98
#pi_n = 0.98
#eta_b = 0.995
#eta_mL = 0.995
#eta_mH = 0.995
#eta_g = 0.99
#e_c = 0.90
#e_tH = 0.89
#e_tL = 0.91
#eta_nt = 1

#print('Offdesign \n')
#print(tutu.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t , hpr, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, atmos_REF,atmos_AT,ideal,M0_AT,Tt4_AT,M0_R,T0_R,P0_R,m0_dot_R, tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,pi_tL_R,tau_tL_R,M9_R,Pt9_P9_R,eta_c, eta_tL, pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL))

#print('Datum \n')
#design = False
#print(tutu.calcula_datum(gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF,atmos_AT,ideal,M0_AT,Tt4_AT,M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH,design, eta_c, eta_tL,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL,tau_t_R,eta_nt))


#print('on design \n')
#print(tutu.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_AT,pi_c_R, tau_t, eta_prop,atmos_AT,ideal,m0_dot_R,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL))