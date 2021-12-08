from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import json
from urllib import request as UR
import requests

# Create your views here.
url = ["http://localhost:5555/aidsclilogs/stats/"]

def index(request):
    allData = []
    num_cli = 0
    cont = 0
    while(1):
        try:
            num_cli+=1
            name_cli = "Cliente {}".format(num_cli)
            print(url[0]+"Cliente_{}.txt".format(num_cli))
            r = UR.urlopen(url[0]+"Cliente_{}.txt".format(num_cli))
            listaServicio = r.read().decode("utf-8").split("\n")
            listaServicio.remove('')
            for linea in listaServicio:
                allData.append(dict(Cliente= name_cli, Componente = linea.split()[1], Función = linea.split()[3] ,Fecha = linea.split()[5], Hora = linea.split()[7]))
        except:
            if cont > 3: break
            else:
                cont+=1

    
    template = loader.get_template('stats/index.html')
    context = {
        'data': allData,
    }

    return HttpResponse(template.render(context, request))


