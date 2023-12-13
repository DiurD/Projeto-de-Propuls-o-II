import re,math
import Prop2


class turbojet:
    
    def __init__(self,name,M0):
        print("*** Criando um novo motor Turbo Jato. Defina seus parâmetros a seguir: ***\n")
        self.name = name
        #self.length = lenght
        self.M0 = M0
        #self.M3 = M3
        #self.D = diameters
        self.A=[float(0)]*10
        #self.airIntakes = intakes


    def calcula_parametrico(self,atmos:Prop2.AircraftEngines,A0,gamma_c,cp_c,gamma_t,cp_t,hpr,Tt4,pi_c,ideal,pi_d_max=1.0,pi_b=1.0,pi_n=1.0,e_c=1.0,e_t=1.0,eta_b=1.0,eta_m=1.0,P0_P9=1.0):
        

        T0,P0,_,_ = atmos.get_param()
        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10

        Ms = [float(1)]*10
        Ms[0] = self.M0
        #Ms[1] = self.M0
        #Ms[2] = 0.9*self.M0 #Pequena redução arbitrária de Mach antes de entrar no compressor.
        #Ms[3] = self.M3
        #Ms[4] = 1 #Página 562 Mattingly
        #Ms[5] = 1 #Página 562 Mattingly
            
        
           #output,tau_lambda,pi_r,  tau_r,  pi_d,  tau_d,  pi_c,  tau_c,  pi_b,  tau_b,  pi_t,  tau_t,  pi_n,  tau_n,  P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
        if ideal:     
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos.ideal_turbojet(self.M0,A0,gamma_c,cp_c,hpr,Tt4,pi_c)    
        else:
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos.real_turbojet(self.M0,A0, gamma_c, gamma_t, cp_c, cp_t, hpr, Tt4, pi_c, pi_d_max, pi_b, pi_n, e_c, e_t, eta_b, eta_m, P0_P9)
        
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

        Ps[9] = Pts[9]/Pt9_P9
        Ts[9] = Ts[0]*T9_T0
        Ms[9] = M9 # Já pego o Mach 9 do resultado do programa

        

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'Tt [K]': Tts,
        'Mach0': Ms[0],
        'Mach9': Ms[9],
        'T0 [K]': T0,
        'P0 [Pa]': P0,
        }

        return output,saidas
    
    
                         #self, gamma_c, gamma_t, cp_c, cp_t, hpr, atmos_REF:Prop2.AircraftEngines, atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_n,eta_b                                                                                                                                                                                                       
    def calcula_offdesign(self, A0, gamma_c, gamma_t, cp_c, cp_t, hpr, atmos_REF:Prop2.AircraftEngines, atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,P0_P9_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_t,tau_t,pi_n,eta_c,eta_b,eta_m,e_t,e_c):
                                                                                                                                                                                                                                                                                                                                     
        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10
        output_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        saida_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        
        
        T0,P0,_,_ = atmos_AT.get_param()

                                                                                     
        output_REF,saida_REF = self.calcula_parametrico(atmos_REF,A0,gamma_c,cp_c,gamma_t,cp_t,hpr,Tt4_R,pi_c_R,ideal,pi_d_max,pi_b,pi_n,e_c,e_t,eta_b,eta_m,P0_P9_R)
        
        if Pt9_P9_R == 1 and m0_R ==1:                                                                                                                                                                                                          
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9,N_NR = atmos_AT.offdesign_turbojet(M0_AT, A0, Tt4_AT, P0_P9_AT, gamma_c, cp_c, gamma_t, cp_t, hpr, pi_d_max, pi_b, pi_t, pi_n, tau_t, eta_c, eta_b, eta_m,saida_REF['Mach0'][0],saida_REF['T0 [K]'][0],saida_REF['P0 [Pa]'][0],saida_REF['Tau'][0],saida_REF['Pi'][0],saida_REF['Tt [K]'][4],saida_REF['Pi'][2],saida_REF['Pi'][3],saida_REF['Tau'][3],output_REF['Pt9/P9'][0],output_REF['m0_dot'][0])
        else:                                                                                                                                                                                                                                                                                                                                                                                               
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9,N_NR = atmos_AT.offdesign_turbojet(M0_AT, A0, Tt4_AT, P0_P9_AT, gamma_c, cp_c, gamma_t, cp_t, hpr, pi_d_max, pi_b, pi_t, pi_n, tau_t, eta_c, eta_b, eta_m,           M0_R,                 T0_R,                  P0_R,                   tau_r_R,            pi_r_R,            Tt4_R,                 pi_d_R,            pi_c_R,            tau_c_R,             Pt9_P9_R,               m0_R)


        Ms = [float(1)]*10
        
        Ms[0] = M0_AT
       # Ms[1] = M0_AT
       # Ms[2] = 0.9*M0_AT
       # Ms[3] = self.M3
       # Ms[4] = 1 #Página 562 Mattingly
       # Ms[5] = 1 #Página 562 Mattingly    
       # Ms[6] = Ms[7] = Ms[8] = Ms[9] = Ms[10] = M9 # Desconsiderar mudança de Mach após sair da turbina, ao longo do bocal de saída
        Ms[9] = M9
        
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9_AT]
        output['Pt9/P9'] = [Pt9_P9]
        output['T9/Tt9'] = [T9_Tt9]
        output['T9/T0'] = [T9_T0]
        output['N/N_R'] = [N_NR]
        


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
        'Mach9': Ms[9],
        'T0 [K]': T0,
        'P0 [Pa]': P0,
        }


        return output,saidas,output_REF,saida_REF

                    
    def calcula_datum(self,A0,gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,P0_P9_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,design:bool,pi_b,pi_d_max,pi_c_R,tau_c_R,pi_t,tau_t,pi_n,eta_c,eta_b,eta_m,e_c,e_t,eta_nt):

        secao = [0,    2 ,  3  ,  4  , 5  ,  8   ,9]
        datum = [0, 0.028, 0.38,0.666,0.762,0.958,1]


        output_Mattingly_REF= {}
        saida_REF = {}
        
        if design:                                                                                                                                             
            output_Mattingly,saida = self.calcula_parametrico(atmos_AT,A0,gamma_c,cp_c,gamma_t,cp_t,hpr,Tt4_AT,pi_c_R,ideal,pi_d_max,pi_b,pi_n,e_c,e_t,eta_b,eta_m,P0_P9_AT)
        else: 
            output_Mattingly,saida,output_Mattingly_REF,saida_REF = self.calcula_offdesign(A0, gamma_c, gamma_t, cp_c, cp_t, hpr, atmos_REF, atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,P0_P9_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_t,tau_t,pi_n,eta_c,eta_b,eta_m,e_t,e_c)

        nova_saida = {
        'Section': secao,
        'Datum':datum,
        'Pt [Pa]':[],
        'Tt [K]':[],
        }

        P_c = saida['Pt [Pa]'][5]*(1-1/eta_nt*((gamma_t-1)/(gamma_t+1)))**((gamma_t)/(gamma_t-1))
        output_Mattingly['P_c'] = P_c

        for i in range(1):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])
        
        for i in range(2,6):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

        for i in range(8,10):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

            return output_Mattingly,saida,output_Mattingly_REF,saida_REF,nova_saida
        
        

#jet = turbojet('jet',2)


  #CALCULO IDEAL ON DESIGN
#print('Ideal turbojet on design \n')
#atmosfera = Prop2.AircraftEngines(12000)
#gamma_c = 1.4
#gamma_t = 1.4
#cp_c = 1.004
#cp_t = 1.004
#hpr = 42800
#ideal = True
#Tt4 = 1667
#pi_c = 20
#A0 = 0.7

#print(jet.calcula_parametrico(atmosfera,A0,gamma_c,cp_c,gamma_t,cp_t,hpr,Tt4,pi_c,ideal))

# CALCULO NAO IDEAL ON DESIGN#
#print('\n Nao ideal turbojet on design \n')
#atmosfera = Prop2.AircraftEngines(12000)
#gamma_c = 1.4
#gamma_t = 1.35
#cp_c = 1.004
#cp_t = 1.239
#hpr = 42800
#pi_d_max = 0.98
#pi_b = 0.98
#pi_n = 0.98
#e_c = 0.92
#e_t = 0.91
#eta_b = 0.99
#eta_m = 0.98
#P0_P9 = 1
#Tt4 = 1667
#pi_c = 20
#A0 = 0.7
#ideal = False

#print(jet.calcula_parametrico(atmosfera,A0,gamma_c,cp_c,gamma_t,cp_t,hpr,Tt4,pi_c,ideal,pi_d_max,pi_b,pi_n,e_c,e_t,eta_b,eta_m,P0_P9))





# Teste Offdesign
#print('começa daqui offdesign \n')

#atmos_REF = Prop2.AircraftEngines(12000)
#gamma_c = 1.4
#cp_c = 1.004
#gamma_t = 1.3
#cp_t = 1.239
#Tt4_R = 1800
#M0_R = 2
#pi_c_R = 10
#tau_c_R = 2.0771
#eta_c = 0.8641
#tau_t = 0.8155
#pi_t = 0.3746
#pi_d_max = 0.95
#pi_d_R = 0.8788
#pi_b = 0.94
#pi_n = 0.96
#eta_b = 0.98
#eta_m = 0.99
#P0_P9_R = 0.5
#hpr = 42800
#f = 0.03567
#Pt9_P9_R = 11.62
#F_mo = 806.9
#S = 44.21
#P0_R = 19400
#T0_R = 216.7
#m0_R = 50
#F = 40345
#A0 = 0.2717
#ideal = False
#tau_r_R = 1.8
#pi_r_R = 7.824
#e_t = 0.92
#e_c = 0.91

#atmos_AT = Prop2.AircraftEngines(9000)
#M0_AT = 1.5
#Tt4_AT = 1670
#P0_P9_AT = 0.955


#print('\nOffdesign \n')
#print(jet.calcula_offdesign(A0,gamma_c,gamma_t,cp_c,cp_t,hpr,atmos_REF,atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,P0_P9_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_t,tau_t,pi_n,eta_c,eta_b,eta_m,e_t,e_c))

#print('\nDatum \n')
#design = False
#print(jet.calcula_datum(A0,gamma_c,gamma_t,cp_c,cp_t,hpr,atmos_REF,atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,P0_P9_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,design,pi_b,pi_d_max,pi_c_R,tau_c_R,pi_t,tau_t,pi_n,eta_c,eta_b,eta_m,e_c,e_t))


#print('on design \n')
#print(jet.calcula_parametrico())