import Prop2
import re
from tabulate import tabulate

class menu:
    
    def __init__(self):
        self.motor = Prop2.AircraftEngines(10000)
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
        ideal = bool(True)
        while escolha != "3":
            print("-- Escolha seu motor para simulação --")
            escolha = input("1 - Ramjet\n2 - Turbofan\n3 - Sair\n")
            match escolha:
                case "1":
                    if re.search('(?i)^sim|^s|^1',input("O ciclo de análise é ideal? ")):
                        ideal = True
                        print("Realizando análise em ciclo ideal:\n")
                        self.ramjet(ideal)
                    else:
                        ideal = False
                        print("Ciclo ideal ainda não implementado!\n")
                case "2":
                    print("Ainda não implementado\n")
                case "3":
                    print("Voltando ao menu inicial!\n")
                    return
                case _:
                    print("Digite um valor válido!\n")

    def ramjet(self,ideal):
        #if not hasattr(self,'motor'):
            escolha = input("Deseja inserir os parâmetros de desempenho pela altitude (tabela ISA) ou manualmente?\n"+
                            "1 - Altitude\n2 - Manualmente\n")
            if escolha =="1":
                h0 = float(input("Digite a altitude de análise do motor em [m]: "))
                self.motor = Prop2.AircraftEngines(h0)

            else:
                T0 = input('Qual a temperatura no motor? [K] ')
                P0 = input('Qual a pressão estática sobre o motor (P0)? [Pa]')
                a0 = input('Qual a velocidade do som na altitude do motor (a0)? [m/s] ')
                self.motor.set_param(T0,P0,a0)
            
            match ideal:
                case True:
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2]); hpr = float(variables[3]); Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600
                    Results = self.motor.ideal_ramjet(M0, gamma, cp*1000, hpr*1000, Tt4)
                    print("\n")
                    print(tabulate(Results,headers="keys")+"\n")
                case False:
                    print("Ciclo não ideal ainda não implementado!\n")
        #else:
            # opcao = input("Deseja ver os resultados antigos ou criar nova atmosfera? \n1 - Ver antigo\n2- Criar novo\n3 - Voltar \n")
            # match opcao

                

Menu = menu()
Menu.iniciar()
