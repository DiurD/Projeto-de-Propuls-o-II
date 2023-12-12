import Prop2,re,math
from tabulate import tabulate


class motor_turboprop:
    def __init__(self):
        print("*** Criando um novo motor do tipo turboprop. Defina seus parâmetros a seguir: ***\n")
        self.name = input("Qual o nome do motor?  ")
        self.diameter = float(input("\nDiâmetro nominal (em metros): "))
        self.length = float(input("\nComprimento (em metros): "))
        self.weight = float(input("\nPeso total (em quilogramas): "))
        self.weightWarhead = float(input("\nPeso warhead (em quilogramas): "))
        self.solidMotor = float(input("\nVelocidade final do motor foguete (em Mach): "))
        self.solidMotordv = float(input("\nVariação da velocidade do motor foguete (em G's): "))
        self.M0 = float(input("\nVelocidade na entrada do motor ramjet (em Mach): "))
        self.propellent = input("\nNome do combustível do ramjet: ")
        self.minReach = float(input("\nAlcance mínimo (em metros): "))
        self.maxReach = float(input("\nAlcance máximo (em metros): "))
        self.maxAlt = float(input("\nAltitude máxima (em km): "))*1000
        self.loadDistance = float(input("\nDistância de arme (em metros): "))
        self.D = self.insere_porcentagem()
        self.cd = float(input("\nPor fim, qual o coeficiente de arrasto do míssil? "))
        self.A=[float(0)]*10

        for i in range(len(self.D)):
            if i == 1:
                self.A[i] = (math.pi*self.D[i]**2)/4*self.airIntakes
            else:
                if self.D[i]==0:
                    self.D[i] = self.D[i-1]
                    self.A[i] = self.A[i-1]
                else:
                    self.A[i] = (math.pi*self.D[i]**2)/4
        self.A[0] = self.A[1]-self.A[0]
        self.D[2] = self.D[3]
        self.A[2] = self.A[3]


    def __str__(self):
        string = "------------\nNome: {}".format(self.name)
        string = string+ "\nDiâmetro: {}".format(self.diameter)
        string = string+ "\nComprimento: {}".format(self.length)
        string = string+ "\nPeso: {}".format(self.weight)
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        for i in range(0,len(self.D)):
            string = string+ "\nDiâmetro e área da seção {}: {} [m] | {:.4f} [m²]".format(i,self.D[i],self.A[i])
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        return string
         
    def insere_porcentagem(self) -> list:
        while 'resp' not in locals():
            text = input("\n Deseja inserir os dados dos diâmetros das seções em porcentagem?  ")
            if re.search('(?i)^sim|^s|^1',text):
                resp=[float(0)]*10
                print("Insira os dados em porcentagem do diâmetro nominal (ex: 17.3 caso 17.3%): \n")
                resp[9]=float(input("\nDiâmetro da seção de saída: "))/100*self.diameter
                resp[8]=float(input("\nDiâmetro da garganta: "))/100*self.diameter
                resp[1]=float(input("\nDiâmetro de cada entrada de ar: "))/100*self.diameter
                self.airIntakes = float(input("\nQuantidade de entradas de ar: "))
                resp[3] = float(input("\nDiâmetro de câmara de combustão: "))/100*self.diameter
                resp[0] = float(input("\nDiâmetro do cone de entrada de ar: "))/100*self.diameter
            elif re.search('(?i)^não|^n|^nao|^2',text):
                resp = [float(0)]*10
                print("Insira os dados a seguir em metros:\n")
                resp[9] = float(input("\nDiâmetro da seção de saída: "))
                resp[8] = float(input("\nDiâmetro da garganta: "))
                resp[1] = float(input("\nDiâmetro de cada entrada de ar: "))
                self.airIntakes = float(input("\nQuantidade de entradas de ar: "))
                resp[3] = float(input("\nDiâmetro de câmara de combustão: "))
                resp[0] = float(input("\nDiâmetro do cone de entrada de ar: "))
            else:
                print("Digite uma opção válida!\n")
        return resp     

    def altera_diam(self):
        self.D = self.insere_porcentagem()
        for i in range(len(self.D)):
            if i == 1:
                self.A[i] = (math.pi*self.D[i]**2)/4*self.airIntakes
            else:
                if self.D[i]==0:
                    self.D[i] = self.D[i-1]
                    self.A[i] = self.A[i-1]
                else:
                    self.A[i] = (math.pi*self.D[i]**2)/4
        self.A[0] = self.A[1]-self.A[0]
        self.D[2] = self.D[3]
        self.A[2] = self.A[3]
                
    def altera_param(self):
        self.name = input("Qual o nome do míssil?  ")
        self.diameter = float(input("\nDiâmetro nominal (em metros): "))
        self.length = float(input("\nComprimento (em metros): "))
        self.weight = float(input("\nPeso total (em quilogramas): "))
        self.weightWarhead = float(input("\nPeso warhead (em quilogramas): "))
        self.solidMotor = float(input("\nVelocidade final do motor foguete (em Mach): "))
        self.solidMotordv = float(input("\nVariação da velocidade do motor foguete (em G's): "))
        self.M0 = float(input("\nVelocidade na entrada do motor ramjet (em Mach): "))
        self.propellent = input("\nNome do combustível do ramjet: ")
        self.minReach = float(input("\nAlcance mínimo (em metros): "))
        self.maxReach = float(input("\nAlcance máximo (em metros): "))
        self.maxAlt = float(input("\nAltitude máxima (em km): "))*1000
        self.loadDistance = float(input("\nDistância de arme (em metros): "))

    def altera_M0(self):
        while 'M0' not in locals():
                text = input(f"\n Deseja alterar o Mach de referência (Atual: {self.M0})? ")
                if re.search('(?i)^sim|^s|^1',text):
                    M0 = self.M0 = float(input("\nInsira o valor de Mach novo: "))
                elif re.search('(?i)^não|^n|^nao|^2',text):
                    print(f"\nMantendo o valor de Mach ( {self.M0} )\n")
                    M0 = self.M0
                else:
                    print("Digite uma opção válida!\n")


    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):
                                  
        T0,P0,_ = atmos.get_param()
        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11

        while 'Mcomb' not in locals():
            text = input("\n Deseja manter o Mach na seção de combustão em seu valor padrão (M_3 = 0.14)? ")
            if re.search('(?i)^sim|^s|^1',text):
                Mcomb = float(0.14)
            elif re.search('(?i)^não|^n|^nao|^2',text):
                Mcomb = float(input("Qual o Mach na câmara de combustão? "))
            else:
                print("Digite uma opção válida!\n")

        Ms = [float(1)]*11
        Ms[0] = self.M0
        Ms[1] = self.M0
        Ms[2] = 0.9*self.M0
        Ms[3] = Mcomb
        Ms[4] = 1 #Página 562 Mattingly
        Ms[5] = 1 #Página 562 Mattingly
        
            
        A_opt = [float(1)]*11
        A_Aopt = [float(1)]*11

        if ideal:
            P0_P9 = 1.0
        else:
            while 'P0_P9' not in locals():
                text = input("\n O fluxo é engasgado (choked)? ")
                if re.search('(?i)^sim|^s|^1',text):
                    P0_P9 = float(1)
                elif re.search('(?i)^não|^n|^nao|^2',text):
                    P0_P9 = float(input("Qual a razão de pressão P0/P9? "))
                else:
                    print("Digite uma opção válida!\n")
            
        
       #output,tau_lambda,pi_r,  tau_r,  pi_d,  tau_d,  pi_c,  tau_c,  pi_b,  tau_b,  pi_tH, tau_tH, pi_tL, tau_tL, pi_n,  tau_n,  P0_P9,Pt9_P9,T9_Tt9,T9_T0
        output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos.real_turboprop(self.M0,Tt4,gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_n,pi_c,e_c,e_tH,e_tL,tau_t,eta_b,eta_mL,eta_mH,eta_g,eta_prop,A0)

        #f = output.get('f')
        #air_comb = 1/f[0]
        #output['AF ratio'] = [air_comb]
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9]
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
                Pts[i] = pis[i]*P0
                Tts[i] = taus[i]*T0
                Ps[i] = P0
                Ts[i] = T0
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]

        Ps[10] = Pts[10]/Pt9_P9
        Ts[10] = Ts[0]*T9_T0
        Ms[6] = Ms[7] = Ms[8] = Ms[9] = Ms[10] = M9
        A_Aopt[10] = (1/(Ms[10]**2)* (2/(gamma_t+1)*(1+(gamma_t-1)/2*Ms[10]**2))**((gamma_t+1)/(gamma_t-1))   )**0.5
        A_opt[10]=self.A[10]/A_Aopt[10]
        
        
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

    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, A0, atmos:Prop2.AircraftEngines,ideal, design:bool, eta_c=1.0, eta_tL=1.0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):

        secao = [0,    2 ,  3  ,  4  , 4.5 ,  5  ,  8   ,9]
        datum = [0, 0.060,0.408,0.616,0.679,0.715,0.9498,1]
        posicao = [self.length*i for i in datum]

        while 'escolha' not in locals():
                mudar = input("\n Deseja mudar as posições dos componentes em relação à entrada de ar? ")
                if re.search('(?i)^sim|^s|^1',mudar):
                    escolha = input("\nDeseja mudar pelo datum ou posição total?\n1 - Datum\n2 - Posição Absoluta")
                    if re.search('(?i)^datum|^1',escolha):
                        for i in range(len(secao)):
                            datum[i] = float(input(f"Valor do datum da seção {secao[i]}"))
                            posicao[i] = datum[i]*self.length
                    elif re.search('(?i)^pos|^2',escolha):
                        for i in range(len(secao)):
                            posicao[i] = float(input(f"Posição absoluta da seção {secao[i]}"))
                            datum[i] = posicao[i]/self.length
                    else:
                        print("!!! DIGITE UM VALOR VÁLIDO !!!")

                elif re.search('(?i)^não|^n|^nao|^2',mudar):
                    escolha = None
                    pass
                else:
                    print("Digite uma opção válida!\n")

        if design:
            _,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0)
        else: 
            _,saida,_,_ = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, A0, atmos,ideal, eta_c=1.0, eta_tL=1.0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0)

        nova_saida = {
        'Section': secao,
        'Pos. [m]':posicao,
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
        nova_saida['P [Pa]'].append(  saida['Pt [Pa]'][1]/(1+(gamma_c-1)/2*1**2)**(gamma_c/(gamma_c-1)))
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

        return nova_saida
    


    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, A0, atmos_REF:Prop2.AircraftEngines,ideal, eta_c=1.0, eta_tL=1.0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):


        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
       #pis[4] = pi_b ; pis[9] = pi_n
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11
        output_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        saida_REF={'Parâmetros inseridos manualmente': ["Cálculo de seções não ocorreu"]}
        
        print("\nA atmosfera de referência é a seguinte:\n")
        print(atmos_REF)
        print(f"\nCom velocidade de referência como Mach {self.M0}")
        self.altera_M0()

        M0_AT = float(input("\nQual o novo Mach para cálculo do off design? "))
        P0_P9_AT = float(input("\nQual o P0/P9 para cálculo do off design? "))
        Tt4_AT = float(input("\nQual o novo Tt4 [K] para cálculo do off design? "))

        print("\nCrie agora a nova atmosfera para simulação do off-design:\n")
        atmos_AT = self.cria_atmos()
        print(atmos_AT)
        
        T0,P0,_ = atmos_AT.get_param()

        while 'escolha' not in locals():
            mudar = input("\nDeseja simular com os parâmetros de referência do ciclo on desing?  Caso não, insira-os manualmente\n")
            if re.search('(?i)^sim|^s|^1|^on|design',mudar):
                print("\nRealizando análise prévia do on design:\n")
                                      
                output_REF,saida_REF = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos_REF,ideal,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL,A0)
                output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b, pi_tH, pi_n, tau_tH, eta_c, eta_b, eta_tL, eta_mL, eta_g, eta_propmax, saida_REF['Mach'][0], saida_REF['T [K]'][0],saida_REF['P [Pa]'][0], output_REF['m0_dot'][0], saida_REF['Tau'][0],saida_REF['Pi'][0],saida_REF['Tt [K]'][4],saida_REF['Pi'][2], saida_REF['Pi'][3], saida_REF['Tau'][3], saida_REF['Pi'][6], saida_REF['Tau'][6], saida_REF['Mach'][10], output_REF['Pt9/P9'][0])

               
                P0_P9_REF = output_REF['P0/P9'][0]
                escolha = True
            elif re.search('(?i)^nao|^2|^n|^man|^manualmente|manual',mudar):
                                                                                              #saida_REF['Tau'][0],saida_REF['Pi'][0],saida_REF['Tt [K]'][4],saida_REF['Pi'][2], saida_REF['Pi'][3], saida_REF['Tau'][3], saida_REF['Pi'][6], saida_REF['Tau'][6], saida_REF['Mach'][10], output_REF['Pt9/P9'][0]
                variables = re.split("\s",input("Por fim, insira os parâmetros de referência:\nM0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R\n"))
                M0_R = float(variables[0]); T0_R = float(variables[1]); P0_R = float(variables[2]); m0_dot_R = float(variables[3]); tau_r_R = float(variables[4]); pi_r_R = float(variables[5]); Tt4_R = float(variables[6]); pi_d_R = float(variables[7]); pi_c_R = float(variables[8]); tau_c_R = float(variables[9]); pi_tL_R = float(variables[10]); tau_tL_R = float(variables[11]); M9_R = float(variables[12]); Pt9_P9_R = float(variables[13])
                output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b, pi_tH, pi_n, tau_tH, eta_c, eta_b, eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R)                                                                                                                                       
                escolha = False                                         
            else:
                print("!!! DIGITE UMA OPÇÃO VÁLIDA !!!")
        
        
        while 'Mcomb' not in locals():
            text = input("\n Deseja manter o Mach na seção de combustão em seu valor padrão PARA O CICLO OFF DESIGN (M_3 = 0.14)? ")
            if re.search('(?i)^sim|^s|^1',text):
                Mcomb = float(0.14)
            elif re.search('(?i)^não|^n|^nao|^2',text):
                Mcomb = float(input("Qual o Mach na câmara de combustão? "))
            else:
                print("Digite uma opção válida!\n")



        Ms = [float(1)]*11
        Ms[0] = M0_AT
        Ms[1] = M0_AT
        Ms[2] = 0.9*M0_AT
        Ms[3] = Mcomb
        Ms[4] = 1 #Página 562 Mattingly
        Ms[5] = 1 #Página 562 Mattingly    
        Ms[6] = Ms[7] = Ms[8] = Ms[9] = Ms[10] = M9 # Desconsiderar mudança de Mach ao longo do bocal de saída
    
  
        
            
        A_opt = [float(1)]*11
        A_Aopt = [float(1)]*11

        
            
        #
        output['Tau_lambda'] = [tau_lambda]
        output['P0/P9'] = [P0_P9_AT]
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
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
                A_Aopt[i] = (1/(Ms[i]**2)* (2/(gamma+1)*(1+(gamma-1)/2*Ms[i]**2))**((gamma+1)/(gamma-1))   )**0.5
                A_opt[i]=self.A[i]/A_Aopt[i]

        Ps[10] = Pts[10]/Pt9_P9
        Ts[10] = Tts[0]*T9_T0
        A_Aopt[10] = (1/(Ms[10]**2)* (2/(gamma_t+1)*(1+(gamma_t-1)/2*Ms[10]**2))**((gamma_t+1)/(gamma_t-1))   )**0.5
        A_opt[10]=self.A[10]/A_Aopt[10]


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
    
    def cria_atmos(self) -> Prop2.AircraftEngines:
        while 'nova_atmos' not in locals():
            escolha = input("Deseja inserir os parâmetros de desempenho pela altitude (tabela ISA) ou manualmente?\n"+
                            "1 - Altitude\n2 - Manualmente\n")
            match escolha:
                case "1":
                    h0 = float(input("Digite a altitude de análise do motor em [m]: "))
                    nova_atmos = self.atmos = Prop2.AircraftEngines(h0)
                case "2":
                    nova_atmos = self.atmos
                    T0 = float(input('Qual a temperatura ambiente (T0)? [K] '))
                    P0 = float(input('Qual a pressão estática sobre o motor (P0)? [Pa] '))
                    a0 = float(input('Qual a velocidade do som na altitude do motor (a0)? [m/s] '))
                    self.atmos.set_param(T0,P0,a0)
                case _:
                    print("Digite um valor válido!")
        return nova_atmos 


        
        




        