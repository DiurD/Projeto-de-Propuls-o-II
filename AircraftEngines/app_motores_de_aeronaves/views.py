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
    tipo = request.POST['motor']
    ideal = True if request.POST['ideal'] == 'true' else False
    on_design = True if request.POST['onDesign'] == 'true' else False
            
    nome = [elem for elem in request.POST.getlist('nome') if elem != ''] 
    nome = nome[0]

    lenght = [elem for elem in request.POST.getlist('comprimento') if elem != ''] 
    lenght = float(lenght[0])

    choked = [elem for elem in request.POST.getlist('fluxo-engasgado') if elem != ''] 
    choked = True if choked == 'on' else False

    height = [elem for elem in request.POST.getlist('altitude') if elem != ''] 
    height = float(height[0])

    gamma_c = [elem for elem in request.POST.getlist('gamma_c') if elem != ''] 
    gamma_c = float(gamma_c[0])

    cp_c = [elem for elem in request.POST.getlist('cp_c') if elem != ''] 
    cp_c = float(cp_c[0])

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

    D = diametros(request)

    print('\n--- \n')
    print(D)
    print('\n---\n')

    novo_motor = motor(name=nome,motor_type=tipo,d0=D[0],d1=D[1],d2=D[2],d3=D[3],d4=D[4],d5=D[5],d6=D[6],d7=D[7],d8=D[8],d9=D[9],
                       lenght = lenght,speed_in_combustion = M3, on_design=on_design,choked = choked,ideal = ideal,Tt4 = Tt4,M0 = M0)
    novo_motor.save()

    atmosfera = Prop2.AircraftEngines(height)
    
    [_,_,a0,_] = atmosfera.get_param()

    if (P0 and T0):
        atmosfera.set_param(T0,P0,a0)

    [T0,P0,a0,rho0] = atmosfera.get_param()
    
    nova_atmos = atmos(alt = atmosfera.height, T0 = T0, P0=P0,rho0=rho0,a0=a0)
    
    print(atmosfera)

    match tipo:
        case 'ramjet':
            RAMJETAO = ramjet.missile(nome,D,lenght,M0,M3,1)
            print(RAMJETAO)

            match (on_design,ideal):
                case (True,True):
                    pass
                case (True,False):
                    pass
                case (False,False):
                    pass

        case 'turbojet':
            pass

        case 'turboprop':
            pass

        case 'turbofan':
            pass

        case _:
            pass
            
    context = {}

    print(request.POST) #Caso queira ver as chaves no terminal
    
    print("\n \n")
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


        