from django.shortcuts import render
from app_motores_de_aeronaves.templates import Prop2
from app_motores_de_aeronaves.models import atmos
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
    for i in range(len(request.POST.getlist('nome'))):
        if request.POST.getlist('nome')[i]:
            nome = request.POST.getlist('nome')[i]
            tipo = request.POST['motor']
            ideal = request.POST['ideal']
            on_design = request.POST['onDesign']

    match request.POST['motor']:
        case 'ramjet':
            print(request.POST['ideal'])


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

        if key in ['d0','d1','d2','d3','d4','d5','d6','d7','d8','d9']:

            num = int(re.findall("[0-9]",key)[0])

            if request.POST['absoluto']:
                if request.POST[key]:
                    diametros[num] = request.POST[key]
                else:
                    diametros[num] = float(0)
            else:
                if request.POST[key]:
                    diametros[num] = request.POST[key]*request.POST['diametro-nominal']
                else:
                    diametros[num] = float(0)

        