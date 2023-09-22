from django.shortcuts import render
from django.urls import resolve
from app_motores_de_aeronaves import Prop2

# Create your views here.

def home(request):
    return render(request,'propulsao2/home.html')

def motores(request):
    motor = request.resolver_match.url_name
    url = motor + '/home_'+motor+'.html'
    return render(request,url)

