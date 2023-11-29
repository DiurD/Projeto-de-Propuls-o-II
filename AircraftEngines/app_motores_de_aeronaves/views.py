from django.shortcuts import render
from app_motores_de_aeronaves.templates import Prop2,ramjet
from app_motores_de_aeronaves.models import atmos,motor
import re


def index(request):
    template = "Site_arquivos/index.html"

    return render(request,template)

def teste(request):
    escolha = request.resolver_match.url_name
    url = "Site_arquivos/" + escolha + '.html'
    return render(request,url)

def results(request):
    # Implementar aqui a lógica para criacao das instãncias e do context
    # Todos os dados são recebidos via POST no objeto request.POST
    
    #print("\n \n")
    tipo = [elem for elem in request.POST.getlist('motor') if elem != '']
    tipo = tipo[0]

    ideal = True if request.POST['ideal'] == 'true' else False
    on_design = True if request.POST['onDesign'] == 'true' else False
            
    nome = [elem for elem in request.POST.getlist('nome') if elem != ''] 
    nome = nome[0]

    lenght = [elem for elem in request.POST.getlist('comprimento') if elem != ''] 
    lenght = float(lenght[0]) if lenght else ''

    choked = [elem for elem in request.POST.getlist('fluxo-engasgado') if elem != ''] 
    choked = True if choked == 'on' else False

    height = [elem for elem in request.POST.getlist('altitude') if elem != ''] 
    height = float(height[0]) if height else 0

    gamma_c = [elem for elem in request.POST.getlist('gamma_c') if elem != ''] 
    gamma_c = float(gamma_c[0])

    gamma_t = [elem for elem in request.POST.getlist('gamma_t') if elem != '']
    gamma_t = float(gamma_t[0]) if gamma_t else gamma_c

    cp_c = [elem for elem in request.POST.getlist('cp_c') if elem != ''] 
    cp_c = float(cp_c[0])

    cp_t = [elem for elem in request.POST.getlist('cp_t') if elem != '']
    cp_t = float(cp_t[0]) if cp_t else cp_c

    hpr = [elem for elem in request.POST.getlist('hpr') if elem != ''] 
    hpr = float(hpr[0])

    Tt4 = [elem for elem in request.POST.getlist('Tt4') if elem != ''] 
    Tt4 = float(Tt4[0])

    M0 = [elem for elem in request.POST.getlist('M0') if elem != ''] 
    M0 = float(M0[0])

    M3 = [elem for elem in request.POST.getlist('M3') if elem != ''] 
    M3 = float(M3[0])

    T0 = [elem for elem in request.POST.getlist('T0') if elem != '']
    T0 = float(T0[0]) if T0 else False

    P0 = [elem for elem in request.POST.getlist('P0') if elem != '']
    P0 = float(P0[0]) if P0 else False

    P0_P9 = [elem for elem in request.POST.getlist('P0_P9') if elem != '']
    P0_P9 = float(P0_P9[0]) if P0_P9 else float(1)

    pi_b = [elem for elem in request.POST.getlist('pi_b') if elem != '']
    pi_b = float(pi_b[0]) if pi_b else float(1)

    pi_n = [elem for elem in request.POST.getlist('pi_n') if elem != '']
    pi_n = float(pi_n[0]) if pi_n else float(1)

    pi_dmax = [elem for elem in request.POST.getlist('pi_dmax') if elem != '']
    pi_dmax = float(pi_dmax[0]) if pi_dmax else float(1)

    eta_b = [elem for elem in request.POST.getlist('eta_b') if elem != '']
    eta_b = float(eta_b[0]) if eta_b else float(1)

    ## CRIAÇÃO DO BANCO DE DADOS ATMOSFÉRICOS

    atmosfera = Prop2.AircraftEngines(height)
    
    [_,_,a0,_] = atmosfera.get_param()

    if (P0 and T0):
        atmosfera.set_param(T0,P0,a0)

    [T0,P0,a0,rho0] = atmosfera.get_param()
    
    nova_atmos = atmos(alt = atmosfera.height, T0 = T0, P0=P0,rho0=rho0,a0=a0)
    ###

    ### PARÂMETROS DE REFERÊNCIA

    altitude_ref = [elem for elem in request.POST.getlist('altitude_ref') if elem != '']
    altitude_ref = float(altitude_ref[0]) if altitude_ref else height

    M0_ref = [elem for elem in request.POST.getlist('M0_ref') if elem != '']
    M0_ref = float(M0_ref[0]) if M0_ref else M0

    T0_ref = [elem for elem in request.POST.getlist('T0_ref') if elem != '']
    T0_ref = float(T0_ref[0]) if T0_ref else 1

    P0_ref = [elem for elem in request.POST.getlist('P0_ref') if elem != '']
    P0_ref = float(P0_ref[0]) if P0_ref else 1

    atmosfera_ref = Prop2.AircraftEngines(altitude_ref)
    
    [_,_,a0_ref,_] = atmosfera.get_param()

    if (P0_ref !=1 and T0_ref != 1):
        atmosfera_ref.set_param(T0_ref,P0_ref,a0_ref)

    [T0_ref,P0_ref,a0_ref,rho0_ref] = atmosfera_ref.get_param()

    Tt4_ref = [elem for elem in request.POST.getlist('Tt4_ref') if elem != '']
    Tt4_ref = float(Tt4_ref[0]) if Tt4_ref else Tt4

    pi_d_ref = [elem for elem in request.POST.getlist('pi_d_ref') if elem != '']
    pi_d_ref = float(pi_d_ref[0]) if pi_d_ref else pi_dmax

    pi_r_ref = [elem for elem in request.POST.getlist('pi_r_ref') if elem != '']
    pi_r_ref = float(pi_r_ref[0]) if pi_r_ref else float(1)

    tau_r_ref = [elem for elem in request.POST.getlist('tau_r_ref') if elem != '']
    tau_r_ref = float(tau_r_ref[0]) if tau_r_ref else float(1)

    Pt9_P9_ref = [elem for elem in request.POST.getlist('Pt9_P9_ref') if elem != '']
    Pt9_P9_ref = float(Pt9_P9_ref[0]) if Pt9_P9_ref else float(1)

    m0_ref = [elem for elem in request.POST.getlist('m0_ref') if elem != '']
    m0_ref = float(m0_ref[0]) if m0_ref else float(1)

    ###

    D = diametros(request)

    # print('\n--- \n')
    # print(D)
    # print('\n---\n')
    # print(atmosfera)

    ## CRIAÇÃO DO BANCO DE DADOS MOTOR
    
    novo_motor = motor(name=nome,motor_type=tipo,d0=D[0],d1=D[1],d2=D[2],d3=D[3],d4=D[4],d5=D[5],d6=D[6],d7=D[7],d8=D[8],d9=D[9],
                       lenght = lenght,speed_in_combustion = M3, on_design=on_design,choked = choked,ideal = ideal,Tt4 = Tt4,M0 = M0,
                       hpr = hpr, cp_c = cp_c,cp_t = cp_t, gamma_c=gamma_c,gamma_t = gamma_t)

    novo_motor.save()

    ###

    match tipo:
        case 'ramjet':
            RAMJETAO = ramjet.missile(nome,D,lenght,M0,M3,1)
            print(RAMJETAO)
            #RAMJETAO.calcula_datum(gamma_c,gamma_t,cp_c,cp_t,hpr,atmosfera_ref,atmosfera,ideal,M0,P0_P9,Tt4,M0_ref,T0_ref,P0_ref,tau_r_ref,pi_r_ref,Tt4_ref,pi_d_ref,Pt9_P9_ref,m0_ref,on_design,pi_b,pi_dmax,pi_n,eta_b)
            Mattingly,Todas_Secoes,Mattingly_REF,Todas_Secoes_REF,Datum = RAMJETAO.calcula_datum(gamma_c,gamma_t,cp_c,cp_t,hpr,atmosfera_ref,atmosfera,ideal,M0,P0_P9,Tt4,M0_ref,T0_ref,P0_ref,tau_r_ref,pi_r_ref,Tt4_ref,pi_d_ref,Pt9_P9_ref,m0_ref,on_design,pi_b,pi_dmax,pi_n,eta_b)
                                                                          
        case 'turbojet':
            pass

        case 'turboprop':
            pass

        case 'turbofan':
            pass

        case _:
            pass
            

    #dicionario_teste = {'x':list(range(10)),
    #                    'y': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
    #                    'z': [69,420,69,420,69,420,69,420,69,420]}

    context = { "Mattingly": Mattingly, # Mattlingly tem uma chave incompativel com templates "P0/P9", você pode então
                "P0_P9": Mattingly.pop("P0/P9"), # separar essa chave do dicionário e passá-la individualmente.  
                "Pt9_P9": Mattingly.pop("Pt9/P9"),
                "T9_T0": Mattingly.pop("T9/T0"),
                "T9_Tt9": Mattingly.pop("T9/Tt9"),
                "Todas_Secoes": Todas_Secoes,
                "Todas_Secoes_len": range(len(Todas_Secoes['Section'])),
                "Mattingly_REF": Mattingly_REF,
                "Todas_Secoes_REF": Todas_Secoes_REF,
                "Datum": Datum,
                "Datum_len": range(len(Datum['Section'])),
                "motor": novo_motor,
                "atmosfera": atmosfera,
                "atmosfera_ref":atmosfera_ref
                }

    print(request.POST) #Caso queira ver as chaves no terminal
    
    print("\n \n")

    print(context)

    return render(request, 'Site_arquivos/resultados.html', context)

def home(request):
    return render(request,'propulsao2/home.html')


def motores(request):
    motor = request.resolver_match.url_name
    url = motor + '/home_'+motor+'.html'
    return render(request,url)

def diametros(request):

    diametros = [float(0)]*10

    for key in request.POST:
        #print(key)

        if key in ['d0','d1','d2','d3','d4','d5','d6','d7','d8','d9']:

            num = int(re.findall("[0-9]",key)[0])
            #print(num)
            #print(request.POST.getlist(key))

            value = [elem for elem in request.POST.getlist(key) if elem != '']
            #print(value)
            
            absoluto = True if request.POST['absoluto'] == 'true' else False
            #print(request.POST['absoluto'])
            #print(absoluto)

            if absoluto:
                if request.POST.getlist(key):
                    diametros[num] = float(value[0])
                else:
                    diametros[num] = float(0)

            else:
                if request.POST.getlist(key):
                    diam = [elem for elem in request.POST.getlist('diametro-nominal') if elem != '']
                    if diam:
                        print(diam)
                        diametros[num] = float(value[0])*float(diam[0])/100
                    else:
                        diametros[num] = 0
                else:
                    diametros[num] = float(0)
        
    return diametros


        