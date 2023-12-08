import re,math
from app_motores_de_aeronaves.templates import Prop2


class missile:
    
    def __init__(self,name,diameters,lenght,M0,intakes):
        print("*** Criando um novo motor do tipo turbofan. Defina seus parâmetros a seguir: ***\n")
        self.name = name
        self.length = lenght
        self.M0 = M0
        self.D = diameters
        self.A=[float(0)]*21
        self.airIntakes = intakes

        for i in range(len(self.D)):
            if i == 1:
                self.A[i] = (math.pi*self.D[i]**2)/4*self.airIntakes
            else:
                if self.D[i]==0 and i!=0:
                    self.D[i] = self.D[i-1]
                    self.A[i] = self.A[i-1]
                else:
                    self.A[i] = (math.pi*self.D[i]**2)/4
        self.A[0] = 0
        self.A[2] = 0
        self.A[3] = 0
        self.A[5] = 0
        self.A[8] = self.A[6]-self.A[7]
        self.A[11] = self.A[9]-self.A[10]
        self.A[14] = self.A[12]-self.A[13]
        self.A[17] = self.A[15]-self.A[16]
        self.A[20] = self.A[18]-self.A[19]
        area_fan = self.A[8]-self.A[11]



    def __str__(self):
        string = "------------\nNome: {}".format(self.name)
        # string = string+ "\nDiâmetro: {}".format(self.diameter)
        string = string+ "\nComprimento: {}".format(self.length)
        # string = string+ "\nPeso: {}".format(self.weight)
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        for i in range(0,len(self.D)):
            string = string+ "\nDiâmetro e área da seção {}: {} [m] | {:.4f} [m²]".format(i,self.D[i],self.A[i])
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        return string 

    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos:Prop2.AircraftEngines,ideal,P0_P9,pi_b,pi_d_max,pi_n,eta_b):
        
        
        T0,P0,_,_ = atmos.get_param()
        secao = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
        pis = [float(1)]*14
        pis[6] = pi_b ; pis[10] = pi_n
        taus = [float(1)]*14
        Pts = [float(1)]*14
        Tts = [float(1)]*14
        Ps = [float(1)]*14
        Ts = [float(1)]*14
        


        Ms = [float(1)]*14
        Ms[0] = 0.01
        Ms[1] = self.M0
        Ms[3] = self.M3
        Ms[2] = Ms[4] =Ms[5] = Ms[6] = Ms[7] = self.M3*1.25
        Ms[8] = 1
        #Ms[9] = self.M0
            
        A_opt = [float(1)]*14
        A_Aopt = [float(1)]*14

        #if ideal:
        #    P0_P9 = 1.0
        #else:
        #    while 'P0_P9' not in locals():
        #        text = input("\n O fluxo é engasgado (choked)? ")
        #        if re.search('(?i)^sim|^s|^1',text):
        #            P0_P9 = float(1)
        #        elif re.search('(?i)^não|^n|^nao|^2',text):
        #            P0_P9 = float(input("Qual a razão de pressão P0/P9? "))
        #        else:
        #            print("Digite uma opção válida!\n")
            
        
        output,tau_lambda,taus[1],pis[1],pis[2],taus[2],taus[3],taus[4],taus[5],taus[7],taus[8],pis[7],pis[8],Pt9_P9,Tt9_T0,T9_T0,Pt19_P19,Tt19_T0,T19_T0 = atmos.real_turbofan(self,self.M0,gamma_c,gamma_t,cp_c,cp_t,hpr,Tt4,pi_d_max,pi_b,pi_n,pi_fn,e_cL,e_cH,e_f,e_tL,e_tH,eta_b,eta_mL,eta_mH,P0_P9,P0_P19,tau_n,tau_fn,pi_cL,pi_cH,pi_f,alpha,batch_size,min_pi_c,max_pi_c)
        # output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos.real_ramjet(self.M0, hpr, Tt4, self.A[1], pis[4], pi_d_max, pis[8], P0_P9, gamma_c, gamma_t, cp_c, cp_t, eta_b)
        #f = output.get('f')
        #air_comb = 1/f[0]
        #output['AF ratio'] = [air_comb]
        # Tt9_T0,Pt19_P19,Tt19_T0,T19_T0 
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9]
        output['Pt9/P9'] = [Pt9_P9]
        # output['T9/Tt9'] = [T9_Tt9]
        output['Tt9/T0'] = [Tt9_T0]
        output['Pt19/P19'] = [Pt19_P19]
        output['Tt19/T0'] = [Tt19_T0]
        output['T19/T0'] = [T19_T0]
        
        #pis[2] = pis[1]
        #taus[2] = taus[1]
        #pis[7] = pis[6] = pis[5] =pis[4]
        #taus[7] = taus[6] = taus[5] =taus[4]


        for i in range(len(secao)):
            if i<4:
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
        Ms[9] = (2/(gamma_t-1)*(Pt9_P9**((gamma_t-1)/gamma_t)-1) )**0.5
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


    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr,atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_n,eta_b):

        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        pis[4] = pi_b ; pis[8] = pi_n
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10
        output_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        saida_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        
        #print("\nA atmosfera de referência é a seguinte:\n")
        #print(atmos_REF)
        #print(f"\nCom velocidade de referência como Mach {self.M0}")
        #self.altera_M0()

        # M0_AT = float(input("\nQual o novo Mach para cálculo do off design? ")) #IMPORTANTES!!!!
        # P0_P9_AT = float(input("\nQual o P0/P9 para cálculo do off design? "))
        # Tt4_AT = float(input("\nQual o novo Tt4 [K] para cálculo do off design? "))

        # print("\nCrie agora a nova atmosfera para simulação do off-design:\n") IMPORTANTE!!!
        # atmos_AT = self.cria_atmos()
        # print(atmos_AT)
        
        T0,P0,_,_ = atmos_AT.get_param()

        output_REF,saida_REF = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,atmos_REF,ideal,P0_P9_AT,pi_b,pi_d_max,pi_n,eta_b)
        
        if Pt9_P9_R == 1 and m0_R ==1:
            output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos_AT.offdesign_ramjet(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pis[4],pis[8],eta_b,saida_REF['Mach'][0],saida_REF['T [K]'][0],saida_REF['P [Pa]'][0],saida_REF['Tau'][1],saida_REF['Pi'][1],saida_REF['Tt [K]'][4],saida_REF['Pi'][3],output_REF['Pt9/P9'][0],output_REF['m0_dot'][0])
        else:
            output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos_AT.offdesign_ramjet(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pis[4],pis[8],eta_b,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R)
        
        #P0_P9_REF = output_REF['P0/P9'][0]

        #while 'escolha' not in locals():
        #    mudar = 'sim' #input("\nDeseja simular com os parâmetros de referência do ciclo on desing?  Caso não, insira-os manualmente\n")
        #    if re.search('(?i)^sim|^s|^1|^on|design',mudar):
        #        print("\nRealizando análise prévia do on design:\n")

                
                
                
                
        #        escolha = True
        #    elif re.search('(?i)^nao|^2|^n|^man|^manualmente|manual',mudar):
        #        variables = re.split("\s",input("Por fim, insira os parâmetros de referência:\nM0_R, T0_R, P0_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, Pt9_P9_R, m0_R\n"))
        #        M0_R = float(variables[0]); T0_R = float(variables[1]); P0_R = float(variables[2]); tau_r_R = float(variables[3]); pi_r_R = float(variables[4]); Tt4_R = float(variables[5]); pi_d_R = float(variables[6]); Pt9_P9_R = float(variables[7]); m0_R = float(variables[8])
        #        
        #        escolha = False
        #    else:
        #        print("!!! DIGITE UMA OPÇÃO VÁLIDA !!!")


        Ms = [float(1)]*10
        Ms[0] = 0.01
        Ms[1] = M0_AT
        Ms[3] = self.M3
        Ms[2] = Ms[4] =Ms[5] = Ms[6] = Ms[7] = self.M3*1.10
        Ms[8] = 1
        #Ms[9] = self.M0
  
        A_opt = [float(1)]*10
        A_Aopt = [float(1)]*10

        #
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9_AT]
        output['Pt9/P9'] = [Pt9_P9]
        output['T9/Tt9'] = [T9_Tt9]
        output['T9/T0'] = [T9_T0]
        
        #pis[2] = pis[1]
        #taus[2] = taus[1]
        #pis[7] = pis[6] = pis[5] =pis[4]
        #taus[7] = taus[6] = taus[5] =taus[4]


        for i in range(len(secao)):
            if i<4:
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
        Ms[9] = (2/(gamma_t-1)*(Pt9_P9**((gamma_t-1)/gamma_t)-1) )**0.5
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
    
    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,design:bool,pi_b,pi_d_max,pi_n,eta_b):

        secao = [0,1,1.1,2,3,4,7,8,9]
        datum = [0, 0.068,0.086,0.128,0.412,0.744,0.744,0.838,1]
        posicao = [self.length*i for i in datum]

        #while 'escolha' not in locals():
        #        mudar = input("\n Deseja mudar as posições dos componentes em relação à entrada de ar? ")
        #        if re.search('(?i)^sim|^s|^1',mudar):
        #            escolha = input("\nDeseja mudar pelo datum ou posição total?\n1 - Datum\n2 - Posição Absoluta")
        #            if re.search('(?i)^datum|^1',escolha):
        #                for i in range(len(secao)):
        #                    datum[i] = float(input(f"Valor do datum da seção {secao[i]}"))
        #                    posicao[i] = datum[i]*self.length
        #            elif re.search('(?i)^pos|^2',escolha):
        #                for i in range(len(secao)):
        #                    posicao[i] = float(input(f"Posição absoluta da seção {secao[i]}"))
        #                    datum[i] = posicao[i]/self.length
        #            else:
        #                print("!!! DIGITE UM VALOR VÁLIDO !!!")

        #        elif re.search('(?i)^não|^n|^nao|^2',mudar):
        #            escolha = None
        #            pass
        #        else:
        #            print("Digite uma opção válida!\n")

        output_Mattingly_REF= {}
        saida_REF = {}

        if design:
            output_Mattingly,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,atmos_REF,ideal,P0_P9_AT,pi_b,pi_d_max,pi_n,eta_b)
        else: 
            output_Mattingly,saida,output_Mattingly_REF,saida_REF = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t , hpr,atmos_REF,atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R,pi_b,pi_d_max,pi_n,eta_b)

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
        'T [K]':[]
        }

        for i in range(2):
            nova_saida['A [m²]'].append(saida['A [m²]'][i])
            nova_saida['A* [m²]'].append(saida['A* [m²]'][i])
            nova_saida['A/A*'].append(saida['A/A*'][i])
            nova_saida['Mach'].append(saida['Mach'][i])
            nova_saida['D [m]'].append(self.D[i])
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['P [Pa]'].append(saida['P [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])
            nova_saida['T [K]'].append(saida['T [K]'][i])
        

        # Seção 1.1
        nova_saida['A [m²]'].append(saida['A [m²]'][1])
        nova_saida['A* [m²]'].append(saida['A [m²]'][1])
        nova_saida['A/A*'].append(1.0)
        nova_saida['Mach'].append(1.0)
        nova_saida['D [m]'].append((saida['A [m²]'][1]*4/math.pi)**0.5/self.airIntakes)
        nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][1])
        nova_saida['P [Pa]'].append( saida['Pt [Pa]'][1]/(1+(gamma_c-1)/2*1**2)**(gamma_c/(gamma_c-1)))
        nova_saida['Tt [K]'].append(saida['Tt [K]'][1])
        nova_saida['T [K]'].append(  saida['Tt [K]'][1]/(1+(gamma_c-1)/2*1**2))   

        for i in range(3,len(secao)):
            if i<6:
                nova_saida['A [m²]'].append(saida['A [m²]'][i-1])
                nova_saida['A* [m²]'].append(saida['A* [m²]'][i-1])
                nova_saida['A/A*'].append(saida['A/A*'][i-1])
                nova_saida['Mach'].append(saida['Mach'][i-1])
                nova_saida['D [m]'].append(self.D[i-1])
                nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i-1])
                nova_saida['P [Pa]'].append(saida['P [Pa]'][i-1])
                nova_saida['Tt [K]'].append(saida['Tt [K]'][i-1])
                nova_saida['T [K]'].append(saida['T [K]'][i-1])
            else:
                nova_saida['A [m²]'].append(saida['A [m²]'][i+1])
                nova_saida['A* [m²]'].append(saida['A* [m²]'][i+1])
                nova_saida['A/A*'].append(saida['A/A*'][i+1])
                nova_saida['Mach'].append(saida['Mach'][i+1])
                nova_saida['D [m]'].append(self.D[i+1])
                nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i+1])
                nova_saida['P [Pa]'].append(saida['P [Pa]'][i+1])
                nova_saida['Tt [K]'].append(saida['Tt [K]'][i+1])
                nova_saida['T [K]'].append(saida['T [K]'][i+1])

        return output_Mattingly,saida,output_Mattingly_REF,saida_REF,nova_saida