import Prop2,Ramjet_missile
import re
from tabulate import tabulate
import numpy as np

class menu:
    
    def __init__(self):
        self.atmos = Prop2.AircraftEngines(0)
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
        opcao = input("-- MENU RAMJET --\n0 - Ver atmosfera atual\n1 - Criar nova atmosfera\n2 - Ver resultados do ciclo paramétrico com atmosfera atual\n3 - Simular um caso real \n4 - Voltar \n")
        while opcao !="4":
            match (opcao,ideal):
                case ("0",_):
                    print(self.atmos)

                case ("2",True):
                    print(self.atmos)
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2])*1000; hpr = float(variables[3])*1000; Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600
                    results = self.atmos.ideal_ramjet(M0, gamma, cp, hpr, Tt4)
                    self.exibe_resultados(results)

                case ("1",True):
                    self.cria_atmos()
                    print(self.atmos)

                case ("1"|"2",False):
                    print("Ciclo não ideal ainda não implementado!\n")

                case("3",_):
                    self.missil = Ramjet_missile.missile()
                    print(self.missil)
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\ngamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    gamma = float(variables[0]); cp =float(variables[1])*1000; hpr = float(variables[2])*1000; Tt4 = float(variables[3])
                    # 1.4 1.004 42000 1600
                    results1,results2 = self.missil.calcula_parametrico(gamma,cp,hpr,Tt4,self.atmos,ideal)
                    self.exibe_resultados(results1)
                    self.exibe_resultados(results2)
                    

                case ("5",_):
                    print(self.missil)
                    return
            opcao = input("-- MENU RAMJET --\n0 - Ver atmosfera atual\n1 - Criar nova atmosfera\n2 - Ver resultados do ciclo paramétrico com atmosfera atual\n3 - Simular um caso real \n4 - Voltar \n")
                    
            
                    

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
    
    def exibe_resultados(self, resultados:dict):
        resultados = {key : np.around(resultados[key], 8) for key in resultados}
        print("\n-------------------------------------------------------------------------------")
        #print(resultados)
        print(tabulate(resultados,headers="keys",tablefmt="github",numalign="center"))
        print("\n-------------------------------------------------------------------------------")




                

Menu = menu()
Menu.iniciar()
