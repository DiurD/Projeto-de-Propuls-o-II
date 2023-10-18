import Prop2,re,math
from tabulate import tabulate


class missile:
    
    def __init__(self):
        print("*** Criando um novo míssil com motor do tipo ramjet. Defina seus parâmetros a seguir: ***\n")
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


    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos:Prop2.AircraftEngines,ideal,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0):
        

        T0,P0,_ = atmos.get_param()
        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        pis[4] = pi_b ; pis[8] = pi_n
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10
        

        while 'Mcomb' not in locals():
            text = input("\n Deseja manter o Mach na seção de combustão em seu valor padrão (M = 0.14)? ")
            if re.search('(?i)^sim|^s|^1',text):
                Mcomb = float(0.14)
            elif re.search('(?i)^não|^n|^nao|^2',text):
                Mcomb = float(input("Qual o Mach na câmara de combustão? "))
            else:
                print("Digite uma opção válida!\n")

        Ms = [float(1)]*10
        Ms[0] = 0.01
        Ms[1] = self.M0
        Ms[3] = Mcomb
        Ms[2] = Ms[4] =Ms[5] = Ms[6] = Ms[7] = Mcomb*1.25
        Ms[8] = 1
        #Ms[9] = self.M0
            
        A_opt = [float(1)]*10
        A_Aopt = [float(1)]*10

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
            
        

        output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos.real_ramjet(self.M0, hpr, Tt4, self.A[1], pis[4], pi_d_max, pis[8], P0_P9, gamma_c, gamma_t, cp_c, cp_t, eta_b)
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
    
    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos:Prop2.AircraftEngines,ideal, design:bool,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0):

        secao = [0,1,1.1,2,3,4,7,8,9]
        datum = [0, 0.068,0.086,0.128,0.412,0.744,0.744,0.838,1]
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
            _,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos,ideal,pi_b,pi_d_max,pi_n,eta_b)
        else: 
            _,saida = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos,ideal,pi_b,pi_d_max,pi_n,eta_b)

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
    


    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos_REF:Prop2.AircraftEngines,ideal,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0):

        T0,P0,_ = atmos_REF.get_param()
        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        pis[4] = pi_b ; pis[8] = pi_n
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10
        
        print("\nA atmosfera de referência é a seguinte:\n")
        print(atmos_REF)
        print(f"\n Com velocidade de referência como Mach {self.M0}")
        self.altera_M0()
        M0_AT = float(input("\nQual o novo Mach para cálculo do off design? "))
        print("\nCrie agora a nova atmosfera para simulação do off-design:\n")
        atmos_AT = self.cria_atmos()
        print(atmos_AT)

        output,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,atmos_REF,ideal,pi_b,pi_d_max,pi_n,eta_b)
        
        #while 'Mcomb' not in locals():
        #    text = input("\n Deseja manter o Mach na seção de combustão em seu valor padrão (M = 0.14)? ")
        #    if re.search('(?i)^sim|^s|^1',text):
        #        Mcomb = float(0.14)
        #    elif re.search('(?i)^não|^n|^nao|^2',text):
        #        Mcomb = float(input("Qual o Mach na câmara de combustão? "))
        #    else:
        #        print("Digite uma opção válida!\n")

        Ms = saida['Mach']
        P0_P9 = output['P0/P9'][0]
            
        A_opt = [float(1)]*10
        A_Aopt = [float(1)]*10

        while 'escolha' not in locals():
            mudar = input("\nDeseja simular com os parâmetros de referência do ciclo on desing?  Caso não, insira-os manualmente\n")
            if re.search('(?i)^sim|^s|^1|^on|design',mudar):
                output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos_AT.offdesign_ramjet(M0_AT, Tt4, P0_P9, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pis[4],pis[8],eta_b,saida['Mach'][0],saida['T [K]'][0],saida['P [Pa]'][0],saida['Tau'][1],saida['Pi'][1],saida['Tt [K]'][4],saida['Pi'][3],output['Pt9/P9'][0],output['m0_dot'][0])
                escolha = True
            elif re.search('(?i)^nao|^2|^n|^man|^manualmente|manual',mudar):
                variables = re.split("\s",input("Por fim, insira os parâmetros de referência:\nM0_R, T0_R, P0_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, Pt9_P9_R, m0_R\n"))
                M0_R = float(variables[0]); T0_R = float(variables[1]); P0_R = float(variables[2]); tau_r_R = float(variables[3]); pi_r_R = float(variables[4]); Tt4_R = float(variables[5]); pi_d_R = float(variables[6]); Pt9_P9_R = float(variables[7]); m0_R = float(variables[8])
                output,tau_lambda,taus[1],pis[1],taus[4],pis[4],pis[8],Pt9_P9,T9_Tt9,T9_T0,pis[3],taus[3] = atmos_AT.offdesign_ramjet(M0_AT, Tt4, P0_P9, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pis[4],pis[8],eta_b,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R,m0_R)
                escolha = True
            else:
                print("!!! DIGITE UMA OPÇÃO VÁLIDA !!!")
            
        
        #
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


        
        




        