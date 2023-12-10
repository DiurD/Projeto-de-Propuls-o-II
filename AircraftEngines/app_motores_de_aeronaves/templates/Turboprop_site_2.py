import re,math
import Prop2


class motor_turboprop_2:
    
    def __init__(self,name,M0):
        print("*** Criando um novo motor turboprop. Defina seus parâmetros a seguir: ***\n")
        self.name = name
        #self.length = lenght
        self.M0 = M0
        #self.M3 = M3
        #self.D = diameters
        self.A=[float(0)]*11
        #self.airIntakes = intakes

        #for i in range(len(self.D)):
        #    if i == 1:
        #        self.A[i] = (math.pi*self.D[i]**2)/4*self.airIntakes
        #    else:
        #        if self.D[i]==0 and i!=0:
        #            self.D[i] = self.D[i-1]
        #            self.A[i] = self.A[i-1]
        #        else:
        #            self.A[i] = (math.pi*self.D[i]**2)/4
        # self.A[0] = self.A[1]-self.A[0]


    #def __str__(self):
        #string = "------------\nNome: {}".format(self.name)
        # string = string+ "\nDiâmetro: {}".format(self.diameter)
        #string = string+ "\nComprimento: {}".format(self.length)
        # string = string+ "\nPeso: {}".format(self.weight)
        #string += "\n°°°°°°°°°°°°°°°°°°°°"
        #for i in range(0,len(self.D)):
        #    string = string+ "\nDiâmetro e área da seção {}: {} [m] | {:.4f} [m²]".format(i,self.D[i],self.A[i])
        #string += "\n°°°°°°°°°°°°°°°°°°°°"
        #return string 

    def calcula_parametrico(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):
        

        T0,P0,_,_ = atmos.get_param()
        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11

        Ms = [float(1)]*11
        Ms[0] = self.M0
        #Ms[1] = self.M0
        #Ms[2] = 0.9*self.M0 #Pequena redução arbitrária de Mach antes de entrar no compressor.
        #Ms[3] = self.M3
        #Ms[4] = 1 #Página 562 Mattingly
        #Ms[5] = 1 #Página 562 Mattingly
        # O resto dos Machs é definido com base no Mach na seção 9 calculado após o ciclo.


# Não alterei essa parte debaixo comentada do "if ideal", se for um problema, me avise.
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
            
        
       #output,tau_lambda,pi_r,  tau_r,  pi_d,  tau_d,  pi_c,  tau_c,  pi_b,  tau_b,  pi_tH, tau_tH, pi_tL, tau_tL, pi_n,  tau_n,  P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9
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
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]

        Ps[10] = Ps[10]/Pt9_P9
        Ts[10] = Ts[0]*T9_T0
        Ms[10] = M9 # Já pego o Mach 9 do resultado do programa, o Mach[10] aqui que é o Mach 9 no caso, pq tem uma seção a mais no motor, a 4,5 relativa a entrada da turbina de baixa. Esse trecho diz que o Mach 5 do Mattingly (Mach[6] do programa), depois de sair da turbina continua o mesmo até o final.

        

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'Tt [K]': Tts,
        }

        return output,saidas
    
    def calcula_datum(self,gamma_c,gamma_t, cp_c , cp_t , hpr, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R, pi_c, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, A0,design:bool, eta_c=1.0, eta_tL=1.0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):

        secao = [0,    2 ,  3  ,  4  , 4.5 ,  5  ,  8   ,9]
        datum = [0, 0.060,0.408,0.616,0.679,0.715,0.9498,1]

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

        if design:                                                                                                            #pq _AT?                                     
            output_Mattingly,saida = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R, pi_c, tau_t, eta_prop,atmos_AT,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0)
        else: 
            output_Mattingly,saida,output_Mattingly_REF,saida_REF = self.calcula_offdesign(gamma_c,gamma_t, cp_c , cp_t ,hpr, pi_c,tau_t,eta_prop,eta_propmax,pi_tH,tau_tH,A0,atmos_REF,atmos_AT,ideal,M0_AT,P0_P9_AT,Tt4_AT, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R,eta_c, eta_tL,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL)

        nova_saida = {
        'Section': secao,
        'Datum':datum,
        'Pt [Pa]':[],
        'Tt [K]':[],
        }

        for i in range(1):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])
        
        for i in range(2,7):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

        for i in range(9,11):
            nova_saida['Pt [Pa]'].append(saida['Pt [Pa]'][i])
            nova_saida['Tt [K]'].append(saida['Tt [K]'][i])

            return output_Mattingly,saida,output_Mattingly_REF,saida_REF,nova_saida
                                                                                                                                                                                                                   
    def calcula_offdesign(self, gamma_c,gamma_t, cp_c , cp_t , hpr, pi_c, tau_t, eta_prop, eta_propmax, pi_tH, tau_tH, A0, atmos_REF:Prop2.AircraftEngines,atmos_AT:Prop2.AircraftEngines,ideal,M0_AT,P0_P9_AT,Tt4_AT,M0_R,T0_R,P0_R,m0_dot_R, tau_r_R,pi_r_R,Tt4_R,pi_d_R,pi_c_R,tau_c_R,pi_tL_R,tau_tL_R,M9_R,Pt9_P9_R,eta_c=1.0, eta_tL=1.0, pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):
                                                                                                                                                                                                                                                                                                                                     
        secao = [0,1,2,3,4,4.5,5,6,7,8,9]
        pis = [float(1)]*11
       # pis[4] = pi_b ; pis[9] = pi_n
        taus = [float(1)]*11
        Pts = [float(1)]*11
        Tts = [float(1)]*11
        Ps = [float(1)]*11
        Ts = [float(1)]*11
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

                                                #(self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4,  pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):                                     
        output_REF,saida_REF = self.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4_R,pi_c, tau_t, eta_prop,atmos_REF,                  ideal,A0,pi_b,pi_d_max,pi_n,eta_b,eta_mL,eta_mH,eta_g,e_c,e_tH,e_tL)
        
        if Pt9_P9_R == 1 and m0_dot_R ==1: #Que isso??????                                                                                                                                                                                                            #pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax,saida_REF['Mach'][0],saida_REF['T [K]'][0],saida_REF['P [Pa]'][0],output_REF['m0_dot'][0],saida_REF['Tau'][0],saida_REF['Pi'][0],saida_REF['Tt [K]'][4],saida_REF['Pi'][2],saida_REF['Pi'][3],saida_REF['Tau'][3],saida_REF['Pi'][5],saida_REF['Tau'][5],saida_REF['Mach'][10],output_REF['Pt9/P9'][0])
        else:                                                                                                                                                                                                                                                     #pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R                                                                                                                                                                                                                                                
            output,tau_lambda,pis[0],taus[0],pis[2],taus[2],pis[3],taus[3],pis[4],taus[4],pis[5],taus[5],pis[6],taus[6],pis[9],taus[9],P0_P9,Pt9_P9,T9_Tt9,T9_T0,M9 = atmos_AT.offdesign_turboprop(M0_AT, Tt4_AT, P0_P9_AT, gamma_c,cp_c,gamma_t,cp_t,hpr,pi_d_max,pi_b,pi_tH,pi_n,tau_tH,eta_c,eta_b,eta_tL, eta_mL, eta_g, eta_propmax, M0_R, T0_R, P0_R, m0_dot_R, tau_r_R, pi_r_R, Tt4_R, pi_d_R, pi_c_R, tau_c_R, pi_tL_R, tau_tL_R, M9_R, Pt9_P9_R)
           
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


        Ms = [float(1)]*11
        
        Ms[0] = M0_AT
       # Ms[1] = M0_AT
       # Ms[2] = 0.9*M0_AT
       # Ms[3] = self.M3
       # Ms[4] = 1 #Página 562 Mattingly
       # Ms[5] = 1 #Página 562 Mattingly    
       # Ms[6] = Ms[7] = Ms[8] = Ms[9] = Ms[10] = M9 # Desconsiderar mudança de Mach após sair da turbina, ao longo do bocal de saída
        Ms[10] = M9
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
            else:
                Pts[i] = pis[i]*Pts[i-1]
                Tts[i] = taus[i]*Tts[i-1]
        

        saidas = {
        'Section': secao,
        'Pi':pis,
        'Tau':taus,
        'Pt [Pa]': Pts,
        'Tt [K]': Tts,
        'Mach': Ms,
        }


        return output,saidas,output_REF,saida_REF


        
        

tutu = motor_turboprop_2('tutu',1)
atmosfera = Prop2.AircraftEngines(7600)

#self, gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmos:Prop2.AircraftEngines,ideal,A0,pi_b=1.0,pi_d_max=1.0,pi_n=1.0,eta_b=1.0,eta_mL=1.0,eta_mH=1.0,eta_g=1.0,e_c=1.0,e_tH=1.0,e_tL=1.0):
gamma_c = 1.4
gamma_t = 1.
cp_c = 1.004
cp_t = 1.004
hpr = 42800
ideal = True
Tt4 = 1370
eta_prop = 0.83
pi_c = 20
tau_t = 0.5
A0 = 0.7
print(tutu.calcula_parametrico(gamma_c,gamma_t, cp_c , cp_t , hpr, Tt4, pi_c, tau_t, eta_prop,atmosfera,ideal,A0))
        