import Prop2
import re
from tabulate import tabulate

class menu:
    
    def __init__(self):
        self.motor = Prop2.AircraftEngines(0)
        pass

    def iniciar(self):
        escolha = "999"
        while escolha != "3":
            print('**** Menu Inicial do Programa de simulação de voo que será transformado em browser****\n')
            escolha = input("1 - Criar motor\n2 - Exibir motores\n3 - Encerrar programa\n")
            match escolha:
                case "1":
                    self.escolha_motores()
                case "2":
                    print("Ainda a ser implementado (talvez no browser)\n")
                case "3":
                    print ("**** Finalização do programa, obrigado pela participação ****\n")
                    return 
                case _:
                    print("!! Digite um valor válido !!\n")
        

    def escolha_motores(self):
        escolha = "999"
        while escolha != "3":
            print("-- Escolha seu motor para simulação --")
            escolha = input("1 - Ramjet\n2 - Turbofan\n3 - Sair\n")
            match escolha:
                case "1":
                    self.ramjet( self.checa_ideal() )
                case "2":
                    print("Ainda não implementado\n")
                case "3":
                    print("Voltando ao menu inicial!\n")
                    return
                case _:
                    print("Digite um valor válido!\n")

    def ramjet(self,ideal):
        opcao = input("Deseja ver os resultados com a atmosfera atual ou criar nova atmosfera para simulação do Ramjet? \n0 - Ver atmosfera atual\n1 - Ver resultados com atmosfera atual\n2 - Criar nova atmosfera e simular\n3 - Voltar \n")
        while opcao !="3":
            match (opcao,ideal):
                case ("0",_):
                    print(self.motor)

                case ("1",True):
                    print(self.motor)
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2]); hpr = float(variables[3]); Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600
                    self.results = self.motor.ideal_ramjet(M0, gamma, cp*1000, hpr*1000, Tt4)
                    self.exibe_resultados(self.results)

                case ("2",True):
                    self.cria_motor()
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2]); hpr = float(variables[3]); Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600
                    self.results = self.motor.ideal_ramjet(M0, gamma, cp*1000, hpr*1000, Tt4)
                    self.exibe_resultados(self.results)

                case ("1"|"2",False):
                    print("Ciclo não ideal ainda não implementado!\n")

                case ("3",_):
                    return
            opcao = input("-- MENU RAMJET --")
                    
            
                    

    def checa_ideal(self) -> bool:
        while 'ideal' not in locals():
            text = input("O ciclo de análise é ideal?  ")
            if re.search('(?i)^sim|^s|^1',text):
                ideal = True
                print("Realizando análise para ciclo ideal\n")
            elif re.search('(?i)^não|^n|^nao|^2',text):
                ideal = False
                print("Realizando análise em ciclo não ideal:\n")
            else:
                print("Digite uma opção válida!\n")
        return ideal
    
    def cria_motor(self) -> Prop2.AircraftEngines:
        while 'novo_motor' not in locals():
            escolha = input("Deseja inserir os parâmetros de desempenho pela altitude (tabela ISA) ou manualmente?\n"+
                            "1 - Altitude\n2 - Manualmente\n")
            match escolha:
                case "1":
                    h0 = float(input("Digite a altitude de análise do motor em [m]: "))
                    novo_motor = self.motor = Prop2.AircraftEngines(h0)
                case "2":
                    novo_motor = self.motor
                    T0 = input('Qual a temperatura no motor? [K]')
                    P0 = input('Qual a pressão estática sobre o motor (P0)? [Pa]')
                    a0 = input('Qual a velocidade do som na altitude do motor (a0)? [m/s] ')
                    self.motor.set_param(T0,P0,a0)
                case _:
                    print("Digite um valor válido!")
        return novo_motor
    
    def exibe_resultados(self, resultados:dict):
        print("\n-------------------------------------------------------------------------------")
        print(tabulate(resultados,headers="keys"))
        print("\n-------------------------------------------------------------------------------")




                

Menu = menu()
Menu.iniciar()
