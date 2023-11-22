from django.shortcuts import render
from django.urls import resolve
from app_motores_de_aeronaves.templates import Prop2

# Create your views here.

def index(request):
    template = "Site_arquivos/index.html"
    return render(request,template)

def teste(request):
    escolha = request.resolver_match.url_name
    url = "Site_arquivos/" + escolha + '.html'
    return render(request,url)

def home(request):
    return render(request,'propulsao2/home.html')


def motores(request):
    motor = request.resolver_match.url_name
    url = motor + '/home_'+motor+'.html'
    return render(request,url)

