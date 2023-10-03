import Prop2,re

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

    def __str__(self):
        string = "------------\nNome: {}".format(self.name)
        string = string+ "\nDiâmetro: {}".format(self.diameter)
        string = string+ "\nComprimento: {}".format(self.length)
        string = string+ "\nPeso: {}".format(self.weight)
        string += "\n°°°°°°°°°°°°°°°°°°°°"
        for i in range(0,len(self.D)):
            string = string+ "\nDiâmetro da seção {}: {}".format(i,self.D[i])
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




        