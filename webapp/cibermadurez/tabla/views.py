from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader

import json
from urllib import request as UR
import requests
# Create your views here.
url = ["http://localhost:5555/aidsclilogs/tabla/"]
def index(request):
    allData = []
    num_cli = 0
    cont = 0
    while(1):
        try:
            num_cli+=1
            name_cli = "Cliente {}".format(num_cli)
            r = UR.urlopen(url[0]+"Cliente_{}.txt".format(num_cli))
            # r = UR.urlopen('http://localhost:5555/aidsclilogs/tabla/Cliente_1.txt')
            listaServicio = r.read().decode("utf-8").split("\n")
            listaServicio.remove('')
            for linea in listaServicio:
                allData.append(dict(Cliente= name_cli, Funcion = linea.split()[1], Port = linea.split()[3], Sintoma = linea.split()[9] ,Fecha = linea.split()[5], Hora = linea.split()[7]))
            num_cli+=1            
        except:
            if cont > 3: break
            else:
                cont+=1
    # r = UR.urlopen('http://localhost:5555/aidsclilogs/tabla/Cliente_1.txt')
    # listaServicio = r.read().decode("utf-8").split("\n")
    # listaServicio.remove('')
    # for linea in listaServicio:
    #     allData.append(dict(Cliente= 'Cliente 1', Funcion = linea.split()[1], Port = linea.split()[3], Sintoma = linea.split()[9] ,Fecha = linea.split()[5], Hora = linea.split()[7]))

    print(allData)
    template = loader.get_template('tabla/index.html')
    context = {
        'data': allData,
    }

    return HttpResponse(template.render(context, request))