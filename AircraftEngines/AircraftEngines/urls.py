"""
URL configuration for AircraftEngines project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app_motores_de_aeronaves import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # rota (ex: prop2.com/pagina1 -> "pagina1/"), view responsável e nome de referência

    
    # CÓDIGO OBSOLETO ABAIXO (PRIMEIRA VERSÃO)
    # path('',views.home,name='home'),
    # path('turbojet/',views.motores,name='turbojet'),
    # path('turbofan/',views.motores,name='turbofan'),
    # path('turboprop/',views.motores,name='turboprop'),
    #path('ramjet/',views.motores,name='ramjet'),

    path('',views.index,name='index'),
    path('sobre',views.teste,name='sobre'),
    path('instrucoes',views.teste,name='instrucoes'),
    path('resultados',views.teste,name='resultados'),
    path('bibliografia',views.teste,name='bibliografia'),
    
]
