import Prop2,Ramjet_missile
import re
from tabulate import tabulate
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

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
                    design = self.checa_design
                    ideal = self.checa_ideal(design)
                    self.ramjet( design,ideal )
                case "2":
                    print("Ainda não implementado\n")
                case "3":
                    print("Voltando ao menu inicial!\n")
                    return
                case _:
                    print("Digite um valor válido!\n")

    def ramjet(self,design,ideal):
        opcao = input("-- MENU RAMJET --\n0 - Ver atmosfera atual\n1 - Criar nova atmosfera\n2 - Ver resultados do ciclo paramétrico com atmosfera atual\n3 - Simular um caso real \n4 - Voltar \n")
        while opcao !="4":
            match (opcao,design):
                case ("0",_): # Printa atmosfera
                    print(self.atmos)

                case ("2",True): # Análise on design, ideal e não ideal
                    print(self.atmos)
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2])*1000; hpr = float(variables[3])*1000; Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600

                    if ideal:
                        results = self.atmos.ideal_ramjet(M0, gamma, cp, hpr, Tt4)
                        self.exibe_resultados(results)
                    else:
                        variables = re.split("\s",input("Como o ciclo é não ideal, adicione os seguintes parâmetros:\npi_b []; pi_n []; pi_d_max []; eta_b []; P0/P9 []\n"))
                        pi_b = float(variables[0]); pi_n = float(variables[1]);pi_d_max = float(variables[2]); eta_b = float(variables[3]); P0_P9 = float(variables[4])
                        results,_,_,_,_,_,_,_,_,_,_,_= self.atmos.real_ramjet(M0, hpr, Tt4, 0, pi_b, pi_d_max, pi_n, P0_P9, gamma, gamma, cp, cp, eta_b)
                        self.exibe_resultados(results)

                case("2",False):
                    print(self.atmos)
                    variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\nM0 [Mach]; gamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
                    # print(variables)
                    M0 = float(variables[0]); gamma = float(variables[1]); cp =float(variables[2])*1000; hpr = float(variables[3])*1000; Tt4 = float(variables[4])
                    # 1 1.4 1.004 42000 1600
                    variables = re.split("\s",input("Como o ciclo é não ideal, adicione os seguintes parâmetros:\npi_b []; pi_n []; pi_d_max []; eta_b []; eta_m []; P0/P9 []\n"))
                    pi_b = float(variables[0]); pi_n = float(variables[1]);pi_d_max = float(variables[2]); eta_b = float(variables[3]); eta_m = float(variables[4]); P0_P9 = float(variables[5])
                    variables = re.split("\s",input("Por fim, insira os parâmetros de referência:\nM0_R, T0_R, P0_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, Pt9_P9_R\n"))
                    M0_R = float(variables[0]); T0_R = float(variables[1]); P0_R = float(variables[2]); tau_r_R = float(variables[3]); pi_r_R = float(variables[4]); Tt4_R = float(variables[5]); pi_d_R = float(variables[6]); Pt9_P9_R = float(variables[7])
                    results,_,_,_,_,_,_,_,_,_,_,_= self.atmos.offdesign_ramjet(M0, Tt4, P0_P9, gamma,cp,gamma,cp,hpr,pi_d_max,pi_b,pi_n,eta_b,eta_m,M0_R,T0_R,P0_R,tau_r_R,pi_r_R,Tt4_R,pi_d_R,Pt9_P9_R)
                    self.exibe_resultados(results)

                case ("1",True): # Cria atmosfera
                    self.cria_atmos()
                    print(self.atmos)

                case ("1",False):
                    print("Ciclo não ideal ainda não implementado!\n")

                case("3",_):
                    self.simula_missil(ideal)
                    
                case ("5",_):
                    print(self.missil)
                    return
            opcao = input("-- MENU RAMJET --\n0 - Ver atmosfera atual\n1 - Criar nova atmosfera\n2 - Ver resultados do ciclo paramétrico com atmosfera atual\n3 - Simular um caso real \n4 - Voltar \n")
                    
            
    def checa_design(self) -> bool:
        while 'design' not in locals():
            text = input("O ciclo de análise é on-design ou off-design?  ")
            if re.search('(?i)^on',text):
                design = True
                print("Realizando análise on design\n")
            elif re.search('(?i)^off',text):
                design = False
                print("Realizando análise off design\n")
            else:
                print("Digite uma opção válida!\n")
        return design

    def checa_ideal(self,design) -> bool:

        if not design:
            ideal = False

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

    def exibe_grafico(self, resultados:dict):
        #resultados = {key : np.around(resultados[key], 8) for key in resultados}
        print("\n------MENU GRÁFICO------------------------------------------------------------------\n")
        print("Estas são as características que você pode plotar:\n")
        print(resultados.keys())
        x_axis = input("Digite o eixo X do gráfico, exatamente como aparece na lista acima: ")
        while x_axis not in resultados.keys():
            x_axis = input("Valor inválido, digite novamente o eixo X do gráfico: ")
        
        contador = int(input("Quantos dados deseja inserir no eixo Y? "))
        while contador not in [1,2]:
            contador = input(f"Digite um valor válido. Você poderá plotar apenas um ou dois dados por vez no eixo Y.\n Você tentou plotar {contador} dados.")
        if contador == 1 :
            print(resultados.keys())
            y_axis = input("Digite o dado do eixo Y do gráfico, exatamente como aparece na lista acima: ")
            while y_axis not in resultados.keys():
                y_axis = input("Valor inválido, digite novamente o dado do eixo Y do gráfico: ")
            plt.plot(resultados[x_axis],resultados[y_axis],'bs-')
            plt.xlabel(x_axis) ; plt.ylabel(y_axis); plt.grid(which='minor')
            plt.xlim(resultados[x_axis][0], resultados[x_axis][-1])
        
        else:
            print(resultados.keys())
            y1_axis = input("Digite o dado do 1° eixo Y do gráfico, exatamente como aparece na lista acima: ")
            while y1_axis not in resultados.keys():
                y1_axis = input("Valor inválido, digite novamente o 1° eixo Y do gráfico: ")

            y2_axis = input("Digite o dado do 2° eixo Y do gráfico, exatamente como aparece na lista acima: ")
            while y2_axis not in resultados.keys():
                y2_axis = input("Valor inválido, digite novamente o 2° eixo Y do gráfico: ")
            
            fig, ax1 = plt.subplots()

            color = 'tab:red'
            ax1.set_xlabel(x_axis); ax1.set_xlim(resultados[x_axis][0], resultados[x_axis][-1])
            ax1.set_ylabel(y1_axis, color=color)
            ax1.plot(resultados[x_axis], resultados[y1_axis],'s-' ,color=color)
            ax1.tick_params(axis='y', labelcolor=color)
            ax1.grid()

            ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

            color = 'tab:blue'
            ax2.set_ylabel(y2_axis, color=color)  # we already handled the x-label with ax1
            ax2.plot(resultados[x_axis], resultados[y2_axis],'o-' ,color=color)
            ax2.tick_params(axis='y', labelcolor=color)
            ax2.grid()

            fig.tight_layout()  # otherwise the right y-label is slightly clipped
        
        plt.show()

        
        print("\n-------------------------------------------------------------------------------")

    def simula_missil(self,design:bool,ideal:bool):
        self.missil = Ramjet_missile.missile()
        texto = "on-design" if ideal else "off-design"
        string = "ideal" if ideal else "não ideal"
        print(self.missil)
        escolha = input(f"\n-- MENU SIMULA MÍSSIL ({texto}) --\n1 - Exibir tabelas de ciclo paramétrico {string}\n2 - Exibir tabelas com datum para ciclo {string}\n3 - Exibir gráficos\n9 - Voltar\n")
        while escolha != "9":
            pi_d_max = 1
            eta_b = 1
            eta_m = 1.0
            variables = re.split("\s",input("Insira as seguintes variáveis, em ordem e espaçadas por um espaço em branco:\ngamma [];cp [kJ/kg]; h_PR [kJ/kg]; T_t4 [K]\n"))
            # print(variables)
            gamma = float(variables[0]); cp =float(variables[1])*1000; hpr = float(variables[2])*1000; Tt4 = float(variables[3])
            # 1.4 1.004 42000 1600
            
            if not design:
                variables = re.split("\s",input("Como o ciclo é não ideal, adicione os seguintes parâmetros:\npi_b []; pi_n []; pi_d_max []; eta_b []; eta_m []\n"))
                pi_b = float(variables[0]); pi_n = float(variables[1]);pi_d_max = float(variables[2]); eta_b = float(variables[3]); eta_m = float(variables[4])

            elif not ideal:
                variables = re.split("\s",input(f"Como o ciclo é {string}, adicione os seguintes parâmetros:\npi_d_max []; eta_b []\n"))
                pi_d_max = float(variables[0]); eta_b = float(variables[1])
                

            match escolha:
                case "1":
                    if design:
                        results1,results2 = self.missil.calcula_parametrico(gamma,cp,hpr,Tt4,self.atmos,ideal,pi_d_max,eta_b)
                    else:
                        results1,results2 = self.missil.calcula_offdesign(gamma,cp,hpr,Tt4,self.atmos,ideal,pi_d_max,eta_b,eta_m)
                        
                    self.exibe_resultados(results1)
                    self.exibe_resultados(results2)
                case "2": 
                    results = self.missil.calcula_datum(gamma,cp,hpr,Tt4,self.atmos,ideal,pi_d_max,eta_b,design,eta_m)
                    self.exibe_resultados(results)
                case "3":
                    results = self.missil.calcula_datum(gamma,cp,hpr,Tt4,self.atmos,ideal,pi_d_max,eta_b,design,eta_m)
                    self.exibe_resultados(results)
                    self.exibe_grafico(results)

                case _:
                    print("!!! Digite um valor válido !!!")   

            escolha = input(f"\n-- MENU SIMULA MÍSSIL ({texto}) --\n1 - Exibir tabelas de ciclo paramétrico {string}\n2 - Exibir tabelas com datum para ciclo {string}\n3 - Exibir gráficos\n9 - Voltar\n")

        
        




                

Menu = menu()
Menu.iniciar()
