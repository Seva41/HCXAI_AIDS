from Modulos.Analyzer.Analyzer import Analyzer
from Modulos.Planner.Planner import Planner
import datetime as dt
import logging

from urllib import request
import requests
import json
import time as tt
import os
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

RUTA_REGISTRO_ATAQUES =  config['ANALYZER']['RUTA_ATAQUES_PROCESADOS']
RUTA_DATAINFO = config['SERVER']['RUTA_DATA_INFO']
SERVER_LOG = config['SERVER']['SERVER_LOG']
url = [
    "http://192.168.0.15:5555/pushserverdone", #0
    "http://192.168.0.15:5555/plkpjhbx/", #1
    "http://192.168.0.15:5555/filaclientes/fila_clientes.txt", #2
    "http://192.168.0.15:5555/pushplan" #3
    ]
def log(componente, func):
    now = dt.datetime.today()
    fecha = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
    hora = now.strftime("%H:%M:%S")

    logger = logging.getLogger('CLI')
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(SERVER_LOG)
    logger.addHandler(handler)
    if (logger.hasHandlers()):
        logger.handlers.clear()
    logger.addHandler(handler)
    
    logger.info('Componente: {} \t Funcion: {} \t Fecha: {} \t Hora: {}'.format(componente, func, fecha, hora))

def log2(port, aType, date, hora, ip, veces):
    if veces == 0:
        f = open(RUTA_DATAINFO, "w")
    else:
        f = open(RUTA_DATAINFO, "a")
    f.write('Port: {} \t Tipo: {} \t Fecha: {} \t Hora: {} \t IP: {}\n'.format(port, aType, date, hora, ip))
    f.close()


def writeFile(data):
    cont = 0
    if '' in data: data.remove('')

    for d in data:
        l= d.split()
        log2(l[1], l[3], l[5], l[7], l[9], cont)
        cont+=1

def consumirServicio(tipo, url, text="x"):
    try:
        #tipo 1: POST
        #tipo 2: GET
        if tipo == 1:
            payload = text
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
            r = requests.post(url, data=payload, headers=headers)
            return r.text
        elif tipo == 2:
            response = request.urlopen(url)
            return response.read().decode("utf-8").split("\n")
        else: return "Error"
    except:
        "Se cayó el servicio"
#############

def postServer(url, data):
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=data, headers=headers)
    return r.text

attempts = 0
segundos = 1
while(True):
    planes = []
    try:
        fila = consumirServicio(tipo=2, url=url[2])
        log("server", "consumirServicio")
        if '' in fila: fila.remove("")
        if fila == ['ok']: 
            print("Esperando...")
            tt.sleep(2)
        else:
            for cliente in fila:
                data = consumirServicio(tipo=2, url=url[1]+cliente+".txt")     
                writeFile(data)
                log("server", "writeFile")
                
                print("Analyzer")
                an = Analyzer()

                an.generateList()
                log("Analyzer", "generateList")
                an.writeDataCsv(tipo=1, mensaje="Generando registro de ataques...")
                log("Analyzer", "writeDataCsv")
                an.processData()
                log("Analyzer", "processData")
                
                print("Planner")
                print("\n\tGenerando plan para {}".format(cliente))
                p = Planner(RUTA_REGISTRO_ATAQUES, cliente)
                plan, sintomas = p.getFileInfo()
                log("Planner", "getFileInfo")
                
                print("Plan generado satisfactoriamente...")
                tt.sleep(2)
                p = {
                    "maquina": cliente,
                    "plan": plan,
                    "sintomas": sintomas
                }
                planes.append(p)
            postServer(url[3], json.dumps(planes))
            tt.sleep(1)
            consumirServicio(tipo=1, url= url[0], text=json.dumps([{"server":"ok"}]))
            tt.sleep(2)
            attempts = 0
            segundos = 1
    except TypeError:
        attempts+=1
        segundos+=3
        print("\n\nNo se puede establecer conexión con servicios web...")
        print("Si el problema persiste contacte al administrador...")
        print("Volviendo a intentar en {} segundos... Intentos: {}".format(segundos, attempts))
        tt.sleep(segundos)
