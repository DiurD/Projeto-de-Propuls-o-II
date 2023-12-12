import re,math
from app_motores_de_aeronaves.templates import Prop2


class motor_turbofan:
    
    def __init__(self,name,diameters,lenght,M0,M3,estagios_compressor_baixa,estagios_compressor_alta,aumento_pressao,diam_fan):
        print("*** Criando um novo motor do tipo turbofan. Defina seus parâmetros a seguir: ***\n")
        self.name = name
        self.length = lenght
        self.M0 = M0
        self.M3 = M3
        self.D = diameters
        diametros_fan = [num for num in diam_fan if num]
        self.D.extend(diametros_fan)
        self.A= diameters
        
        self.compressores_baixa = estagios_compressor_baixa
        self.compressores_alta = estagios_compressor_alta
        self.pi_cL = self.compressores_baixa**aumento_pressao
        self.pi_cH = self.compressores_alta**aumento_pressao
        self.pi_c = self.pi_cL*self.pi_cH

        for i in range(len(self.D)):
            if self.D[i]==0 and i!=0:
                self.D[i] = self.D[i-1]
                self.A[i] = self.A[i-1]
            else:
                self.A[i] = (math.pi*self.D[i]**2)/4
        self.A[2] = self.A[2]-self.A[3]
        self.A[10] = self.A[2]
        self.A[-1] = self.A[-1]-self.A[3]
        self.A[-2] = self.A[-1]
        self.alpha = self.A[2]/self.A[3]

    def __str__(self):
        string = "------------\nNome: {}".format(self.name)
        string = string+ "\nComprimento: {}".format(self.length)
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        for i in range(0,len(self.D)):
            string = string+ "\nDiâmetro e área da seção {}: {} [m] | {:.4f} [m²]".format(i,self.D[i],self.A[i])
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        return string 

    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos:Prop2.AircraftEngines,ideal,P0_P9,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f):
        
        T0,P0,_,_ = atmos.get_param()
        secao = [0,1,2,2.1,2.5,3,4,4.5,5,8,9,13,18,19]
        pis = [float(1)]*14
        pis[2] = pi_f
        pis[4] = self.pi_cL
        pis[5] = self.pi_cH
        pis[6] = pi_b  
        pis[10] = pi_n
        pis[13] = pi_fn
        taus = [float(1)]*14

        for i in range(len(taus)):
            if i<=6:
                taus[i] = pis[i]**((gamma_c - 1)/gamma_c)
            else:
                taus[i] = pis[i]**((gamma_t - 1)/gamma_t)

        Pts = [float(1)]*14
        Tts = [float(1)]*14
        Ps = [float(1)]*14
        Ts = [float(1)]*14
        Ms = [float(1)]*14
        Ms[0] = self.M0
        Ms[1] = 0.01
        Ms[2] = Ms[3]= Ms[4] = Ms[5] = self.M3
        Ms[6] = self.M3*1.2
        Ms[7] = Ms[8] =Ms[6]
        Ms[9] = 1   
        A_opt = [float(1)]*14
        A_Aopt = [float(1)]*14

        output,self.T0,taus[1],pis[1],pis[2],taus[2],taus[3],tau_lambda,taus[4],taus[5],taus[7],taus[8],pis[7],pis[8],Pt9_P9,Tt9_T0,T9_T0,Pt19_P19,Tt19_T0,T19_T0 = atmos.real_turbofan(self,self.M0,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4,pi_d_max,pi_b,pi_n,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_b,eta_mL,eta_mH,P0_P9,P0_P19,taus[10],taus[13],self.pi_cL,self.pi_cH,pi_f,self.alpha)
            
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9]
        output['Pt9/P9'] = [Pt9_P9]
        output['Tt9/T0'] = [Tt9_T0]
        output['Pt19/P19'] = [Pt19_P19]
        output['Tt19/T0'] = [Tt19_T0]
        output['T19/T0'] = [T19_T0]
        output['T9/T0'] = [T9_T0]
        
        taus[6] = Tt4/Tts[5]
        taus[11] = taus[3]
        pi_f = pis[3] = pis[11]
        pi_cL = pis[4]
        pi_cH = pis[5]
        pis[9] = 0.92
        Ms[10] = (2/(gamma_c-1)*(Pt9_P9**((gamma_c-1)/gamma_c)-1) )**0.5
        Ms[12] = Ms[13] = (2/(gamma_c-1)*(Pt19_P19^((gamma_c-1)/gamma_c)-1))**0.5

        for i in range(len(secao)):
            if i<4 or i>10:
                gamma = gamma_c
            else:
                gamma = gamma_t

            if i == 0:
                Pts[i] = P0
                Tts[i] = T0
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]

        Ps[9] = Pts[9]/Pt9_P9
        Ts[9] = Tts[0]*T9_T0
        A_Aopt[9] = (1/(Ms[9]**2)* (2/(gamma_t+1)*(1+(gamma_t-1)/2*Ms[9]**2))**((gamma_t+1)/(gamma_t-1))   )**0.5
        A_opt[9]=self.A[9]/A_Aopt[9]

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'P [Pa]': Ps,
        'Tt [K]': Tts,
        'T [K]': Ts,
        'Mach': Ms,
        'A [m²]' : self.A,
        'A* [m²]': A_opt,
        'A/A*': A_Aopt,
        }

        return output,saidas

    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr,atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f,eta_f,eta_cL,eta_cH,eta_tL,M9_R,M19_R,tau_lambda_R,pi_f_R,pi_cH_R,pi_cL_R,pi_tL_R,tau_f_R,tau_tL_R,alpha_R,Tt4):

        secao = [0,1,2,2.1,2.5,3,4,4.5,5,8,9,13,18,19]
        pis = [float(1)]*14
        pis[0] = 1
        pis[6] = pi_b ; pis[10] = pi_n
        taus = [float(1)]*14
        Pts = [float(1)]*14
        Tts = [float(1)]*14
        Ps = [float(1)]*14
        Ts = [float(1)]*14
        output_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        saida_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        
        T0,P0,_,_ = atmos_AT.get_param()

        output_REF,saida_REF = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,atmos_REF,ideal,P0_P9_AT,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f)
        output,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos_AT,ideal,P0_P9_AT,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f)

        if Pt9_P9_R == 1 and m0_R ==1:
            output,self.T0,taus[5],taus[4],taus[1],pis[1],pis[2],tau_lambda,taus[8],taus[3],taus[4],pis[8],pis[4],taus[5],pis[5],pis[3],Pt19_P0,Pt19_P19,Pt9_P0,Pt9_P9,taus[3],taus[8],tau_f_R,tau_cL_R,pi_tL_R,T9_T0,T19_T0,P19_P0,P9_P0 = atmos_AT.real_turbofan_off_design(M0_AT,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4_AT,pi_d_max,pi_b,self.pi_c,pis[7],pi_n,pi_fn,saida['Tau'][7],eta_f,eta_cL,eta_cH,eta_b,eta_mL,eta_mH,eta_tL,saida_REF['Mach'][0],saida_REF['T [K]'][0],saida_REF['P [Pa]'][0],saida_REF['Tau'][1],tau_lambda_R,saida_REF['Pi'][1],saida_REF['Tt [K]'][4],saida_REF['Pi'][3],saida_REF['Pi'][3],saida_REF['Pi'][5],saida_REF['Pi'][4],saida_REF['Pi'][8],saida_REF['Tau'][3],saida_REF['Tau'][8],alpha_R,saida_REF['Mach'][1],saida_REF['Mach'][13],output_REF['m0_dot'][0])
        else:
            output,self.T0,taus[5],taus[4],taus[1],pis[1],pis[2],tau_lambda,taus[8],taus[3],taus[4],pis[8],pis[4],taus[5],pis[5],pis[3],Pt19_P0,Pt19_P19,Pt9_P0,Pt9_P9,taus[3],taus[8],tau_f_R,tau_cL_R,pi_tL_R,T9_T0,T19_T0,P19_P0,P9_P0 = atmos_AT.real_turbofan_off_design(M0_AT,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4_AT,pi_d_max,pi_b,self.pi_c,pis[7],pi_n,pi_fn,saida['Tau'][7],eta_f,eta_cL,eta_cH,eta_b,eta_mL,eta_mH,eta_tL,M0_R,T0_R,P0_R,tau_r_R,output_REF['Tau_lambda'] ,pi_r_R,Tt4_R,pi_d_R,pi_f_R,pi_cH_R,pi_cL_R,pi_tL_R,tau_f_R,tau_tL_R,self.alpha,M9_R,M19_R,m0_R)
        
        Ms = [float(1)]*14
        Ms[0] = self.M0
        Ms[1] = 0.01
        Ms[2] = Ms[3]= Ms[4] = Ms[5] = self.M3
        Ms[6] = self.M3*1.2
        Ms[7] = Ms[8] =Ms[6]
        Ms[9] = 1
        A_opt = [float(1)]*14
        A_Aopt = [float(1)]*14

        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9_AT]
        output['Pt9/P9'] = [Pt9_P9]
        output['Pt19/P19'] = [Pt19_P19]
        output['T9/T0'] = [T9_T0]
        output['Pt19/P0'] = [Pt19_P0]
        output['P19/P0'] = [P19_P0]
        output['Pt9/P0'] = [Pt9_P0]
        output['T19/T0'] = [T19_T0]
        output['P9/P0'] = [P9_P0]
        
        taus[6] = Tt4_R/Tts[5]
        tau_tH = taus[7]
        taus[11] = taus[3]
        pi_tH = pis[7]
        pis[9] = 0.92
        pis[3] = pis[11]
        Ms[10] = (2/(gamma_c-1)*(Pt9_P9**((gamma_c-1)/gamma_c)-1) )**0.5
        Ms[12] = Ms[13] = (2/(gamma_c-1)*(Pt19_P19^((gamma_c-1)/gamma_c)-1))**0.5

        for i in range(len(secao)):
            if i<4 or i>10:
                gamma = gamma_c
            else:
                gamma = gamma_t

            if i == 0:
                Pts[i] = P0
                Tts[i] = T0
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]

        Ps[9] = Pts[9]/Pt9_P9
        Ts[9] = Tts[0]*T9_T0
        A_Aopt[9] = (1/(Ms[9]**2)* (2/(gamma_t+1)*(1+(gamma_t-1)/2*Ms[9]**2))**((gamma_t+1)/(gamma_t-1))   )**0.5
        A_opt[9]=self.A[9]/A_Aopt[9]

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'P [Pa]': Ps,
        'Tt [K]': Tts,
        'T [K]': Ts,
        'Mach': Ms,
        'A [m²]' : self.A,
        'A* [m²]': A_opt,
        'A/A*': A_Aopt,
        }

        return output,saidas,output_REF,saida_REF
    
    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,design:bool,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f,eta_f,eta_cL,eta_cH,eta_tL,M9_R,M19_R,tau_lambda_R,pi_f_R,pi_cH_R,pi_cL_R,pi_tL_R,tau_f_R,tau_tL_R,eta_nt_CORE,eta_nt_FAN):

        secao = [0,1,2,2.1,2.5,3,4,4.5,5,8,9,13,18,19]
        datum = [0.0000,0.1566,0.2202,0.2522,0.3144,0.4158,0.6903,0.7641,0.8275,0.8736,1.0000,0.4488,0.5348,0.6119]
        posicao = [self.length*i for i in datum]
        
        output_Mattingly_REF= {}
        saida_REF = {}

        if design:
            output_Mattingly,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,atmos_REF,ideal,P0_P9_AT,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f)
        else: 
            output_Mattingly,saida,output_Mattingly_REF,saida_REF = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t , hpr,atmos_REF,atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_n,eta_b,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_mL,eta_mH,P0_P19,pi_f,eta_f,eta_cL,eta_cH,eta_tL,M9_R,M19_R,tau_lambda_R,pi_f_R,pi_cH_R,pi_cL_R,pi_tL_R,tau_f_R,tau_tL_R,self.alpha,Tt4_AT)

        nova_saida = {
        'Section': secao,
        'Pos.':posicao,
        'Datum':datum,
        'D [m]':[],
        'A [m²]': [],
        'A* [m²]': [],
        'A/A*': [],
        'Mach':[],
        'Pt [Pa]':[],
        'P [Pa]':[],
        'Tt [K]':[],
        'T [K]':[],
        'P_c [Pa]': []
        }

        P_c_CORE = saida['Pt [Pa]'][10]*(1-1/eta_nt_CORE*((gamma_c-1)/(gamma_c+1)))**((gamma_c)/(gamma_c-1))
        output_Mattingly['P_c_CORE'] = P_c_CORE
        P_c_FAN = saida['Pt [Pa]'][13]*(1-1/eta_nt_FAN*((gamma_t-1)/(gamma_t+1)))**((gamma_t)/(gamma_t-1))
        output_Mattingly['P_c_FAN'] = P_c_FAN

        nova_saida['A [m²]'] = saida['A [m²]']
        nova_saida['A* [m²]'] = saida['A* [m²]']
        nova_saida['A/A*'] = saida['A/A*']
        nova_saida['Mach'] = saida['Mach']
        nova_saida['D [m]'] = self.D
        nova_saida['Pt [Pa]'] = saida['Pt [Pa]']
        nova_saida['P [Pa]'] = saida['P [Pa]']
        nova_saida['Tt [K]'] = saida['Tt [K]']
        nova_saida['T [K]'] = saida['T [K]']

        # for i in range(2):
        #     nova_saida['A [m²]'].append(saida['A [m²]'][i])
        #     nova_saida['A* [m²]'].append(saida['A* [m²]'][i])
        #     nova_saida['A/A*'].append(saida['A/A*'][i])
        #     nova_saida['Mach'].append(saida['Mach'][i])
        #     nova_saida['D [m]'].append(self.D[i])
        #     nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
        #     nova_saida['P [Pa]'].append(saida['P [Pa]'][i])
        #     nova_saida['Tt [K]'].append(saida['Tt [K]'][i])
        #     nova_saida['T [K]'].append(saida['T [K]'][i])
        

        # # Seção 1.1
        # nova_saida['A [m²]'].append(saida['A [m²]'][1])
        # nova_saida['A* [m²]'].append(saida['A [m²]'][1])
        # nova_saida['A/A*'].append(1.0)
        # nova_saida['Mach'].append(1.0)
        # nova_saida['D [m]'].append((saida['A [m²]'][1]*4/math.pi)**0.5)
        # nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][1])
        # nova_saida['P [Pa]'].append( saida['Pt [Pa]'][1]/(1+(gamma_c-1)/2*1**2)**(gamma_c/(gamma_c-1)))
        # nova_saida['Tt [K]'].append(saida['Tt [K]'][1])
        # nova_saida['T [K]'].append(  saida['Tt [K]'][1]/(1+(gamma_c-1)/2*1**2))   

        # for i in range(3,len(secao)):
        #     if i<6:
        #         nova_saida['A [m²]'].append(saida['A [m²]'][i-1])
        #         nova_saida['A* [m²]'].append(saida['A* [m²]'][i-1])
        #         nova_saida['A/A*'].append(saida['A/A*'][i-1])
        #         nova_saida['Mach'].append(saida['Mach'][i-1])
        #         nova_saida['D [m]'].append(self.D[i-1])
        #         nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i-1])
        #         nova_saida['P [Pa]'].append(saida['P [Pa]'][i-1])
        #         nova_saida['Tt [K]'].append(saida['Tt [K]'][i-1])
        #         nova_saida['T [K]'].append(saida['T [K]'][i-1])
        #     else:
        #         nova_saida['A [m²]'].append(saida['A [m²]'][i+1])
        #         nova_saida['A* [m²]'].append(saida['A* [m²]'][i+1])
        #         nova_saida['A/A*'].append(saida['A/A*'][i+1])
        #         nova_saida['Mach'].append(saida['Mach'][i+1])
        #         nova_saida['D [m]'].append(self.D[i+1])
        #         nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i+1])
        #         nova_saida['P [Pa]'].append(saida['P [Pa]'][i+1])
        #         nova_saida['Tt [K]'].append(saida['Tt [K]'][i+1])
        #         nova_saida['T [K]'].append(saida['T [K]'][i+1])

        return output_Mattingly,saida,output_Mattingly_REF,saida_REF,nova_saida