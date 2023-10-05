import Prop2,re,math

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
        print(self.D)
        self.cd = float(input("\nPor fim, qual o coeficiente de arrasto do míssil? "))
        self.A=[float(0)]*10

        for i in range(0,len(self.D)):
            if i == 1:
                self.A[i] = (math.pi*self.D[i]**2)/2*self.airIntakes
            else:
                if self.D[i]==0:
                    self.A[i] = self.A[i-1]
                else:
                    self.A[i] = (math.pi*self.D[i]**2)/2



    def __str__(self):
        string = "------------\nNome: {}".format(self.name)
        string = string+ "\nDiâmetro: {}".format(self.diameter)
        string = string+ "\nComprimento: {}".format(self.length)
        string = string+ "\nPeso: {}".format(self.weight)
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        for i in range(0,len(self.D)):
            string = string+ "\nDiâmetro e área da seção {}: {} [m] | {} [m²]".format(i,self.D[i],self.A[i])
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        return string
         
    def insere_porcentagem(self) -> list:
        while 'resp' not in locals():
            text = input("\n Deseja inserir os dados dos diâmetros das seções em porcentagem?  ")
            if re.search('(?i)^sim|^s|^1',text):
                resp=[float(0)]*10
                print("Insira os dados em porcentagem do diâmetro nominal (ex: 50 caso 50%): \n")
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

    def calculatabela(self, M0, gamma, cp, hpr, Tt4,atmos:Prop2.AircraftEngines):
        R = (gamma-1)/gamma*cp
        T0,P0,a0 = atmos.get_param()
        secao = [0,1,2,3,4,5,6,7,8,9]
        pis = [float(1)]*10
        taus = [float(1)]*10
        Pts = [float(1)]*10
        Tts = [float(1)]*10
        Ps = [float(1)]*10
        Ts = [float(1)]*10
        
        Ms = [float(1)]*10
        Ms[0] = 0
        Ms[1] = self.M0

        As = [float(1)]*10
        A_optimum = [float(1)]*10

        
        while 'P0_P9' not in locals():
            text = input("\n O fluxo é engasgado (choked)? ")
            if re.search('(?i)^sim|^s|^1',text):
                P0_P9 = float(1)
            elif re.search('(?i)^não|^n|^nao|^2',text):
                P0_P9 = float(input("Qual a razão de pressão P0/P9?"))
            else:
                print("Digite uma opção válida!\n")

        output,tau_lambda,taus[1],pis[1],taus[4],Pt9_P9,T9_Tt9,T9_T0 = atmos.real_ramjet(self, M0, hpr, Tt4, self.A[1], pis[4], pis[3], pis[8], P0_P9=P0_P9)
        f = output.get('f')
        air_comb = 1/f
        Ms[9] = (2/(gamma-1)*Pt9_P9**((gamma-1)/gamma-1)  )**0.5


        for i in range(len(secao)):
            if i == 0:
                Pts[i] = P0
                Tts[i] = T0
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)
            else:
                Pts[i] = pis[i]*Ps[i-1]
                Tts[i] = taus[i]*Ts[i-1]
                Ps[i] = Pts[i]/(1+(gamma-1)/2*Ms[i]**2)**(gamma/(gamma-1))
                Ts[i] = Tts[i]/(1+(gamma-1)/2*Ms[i]**2)


        
        




        