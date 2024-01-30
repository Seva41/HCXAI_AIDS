from Modulos.Sensor.Sensor import Sensor
from Modulos.Preprocessing.Preprocessing import Preprocessing
from Modulos.Classifier.Classifier import Classifier
from Modulos.Executer.Executer import Executer
from Modulos.Analyzer.Analyzer import Analyzer
from Modulos.Planner.Planner import Planner

import datetime as dt
import logging
import json
from urllib import request

# import requests
import server
import time as t
import configparser
import socket

local_ipv4 = "192.168.0.11"

config = configparser.ConfigParser()
config.read("config.ini")
FILE = config["CLIENTE"]["FILE"]
MAQUNA = config["CLIENTE"]["MAQUINA"]
MONITOREO = int(config["CLIENTE"]["SCAN_SEGUNDOS"])
url = [
    f"http://{local_ipv4}:5555/pushclientdone",
    f"http://{local_ipv4}:5555/plans/{MAQUNA}.json",
    f"http://{local_ipv4}:5555/pushclientlogstats",
    f"http://{local_ipv4}:5555/pushserverdone",
]


def getFileData():
    data = []
    data.append({"maquina": MAQUNA})
    file = open(FILE, "r")
    for linea in file:
        info = linea.split()
        t = (
            info[1],
            info[3],
            info[5],
            info[7],
            info[9],
        )  # [0] puerto, [1] tipo, [2] fecha, [3] hora, [4] ip
        if t[1] == "DoS" or t[1] == "Fuzzers":
            puerto = t[4]
        else:
            puerto = t[0]

        dic = {"port": puerto, "tipo": t[1], "fecha": t[2], "hora": t[3], "ip": t[4]}
        data.append(dic)
    file.close()
    return json.dumps(data)


def consumirServicio(tipo, url):
    # tipo 1: post
    # tipo 2: get
    r = "nope"
    if tipo == 1:
        payload = json.dumps([{"maquina": MAQUNA}])
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        r = requests.post(url, data=payload, headers=headers)
        return r.text
    elif tipo == 2:
        response = request.urlopen(url)
        return json.loads(response.read())
    # obtner datos del servicio
    else:
        return "Error"


def log(componente, func):
    logData = []
    logData.append({"maquina": MAQUNA})
    now = dt.datetime.today()
    fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    hora = now.strftime("%H:%M:%S")
    dic = {"Componente": componente, "Funcion": func, "Fecha": fecha, "Hora": hora}
    logData.append(dic)
    payload = json.dumps(logData)
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post(url[2], data=payload, headers=headers)


#####
print("Iniciando...")

while True:
    print("Sensor")
    s = Sensor()
    s.sniff()
    log("Sensor", "sniff")

    print("Preprocessing")
    pp = Preprocessing()
    pp.callArgus()
    log("Preprocessing", "callArgus")

    print("Classifier")
    m = Classifier(MAQUNA)
    m.generateModels()
    log("Classifier", "generateModels")

    m.readFile()
    log("Classifier", "readFile")

    m.classifyData()
    log("Classifier", "classifyData")

    #####WEBSERVICE####

    intentos = 1
    conn = False
    while intentos <= 3:
        try:
            respuesta = consumirServicio(tipo=1, url=url[0])
            log("Cliente", "consumirServicio")
        except:
            respuesta = "Error"
        if '"status":200' in respuesta:
            print("Conexión exitosa. Esperando AIDS_SERVER...")
            conn = True
            t.sleep(5)
            break
        else:
            print("No se pudo conectar con el servidor...")
            print("Volviendo a intentar. Intento {}/3".format(intentos))
            intentos += 1

    if conn:
        respuesta = consumirServicio(tipo=2, url=url[1])
        log("Cliente", "consumirServicio")
        if respuesta["plan"] == "No hay amenazas detectadas":
            print("No se requiere aplicar medidas")
        else:
            e = Executer()
            entry = e.decode(respuesta["plan"])
            log("Executer", "decode")
            e.setEntrada(entry)
            log("Executer", "setEntrada")
            e.report(respuesta["plan"])
            log("Executer", "report")
            if e.getConfirm():
                log("Executer", "getConfirm")
                e.manageEntry(respuesta["sintomas"])
                log("Executer", "manageEntry")
                print("Medidas aplicadas.")
            else:
                print("No se aplicaron medidas.")

        try:
            fila = consumirServicio(tipo=2, url=url[2])
            log("server", "consumirServicio")
            if "" in fila:
                fila.remove("")
            if fila == ["ok"]:
                print("Esperando...")
                t.sleep(2)
            else:
                for cliente in fila:
                    data = consumirServicio(tipo=2, url=url[1] + cliente + ".txt")
                    writeFile(data)
                    log("server", "writeFile")

                    print("Analyzer")
                    an = Analyzer()

                    # ... (Rest of the code remains the same)

                    print("Planner")
                    print("\n\tGenerando plan para {}".format(cliente))
                    p = Planner(RUTA_REGISTRO_ATAQUES, cliente)
                    plan, sintomas = p.getFileInfo()
                    log("Planner", "getFileInfo")

                    print("Plan generado satisfactoriamente...")
                    t.sleep(2)
                    p = {"maquina": cliente, "plan": plan, "sintomas": sintomas}
                    planes.append(p)
                postServer(url[3], json.dumps(planes))
                t.sleep(1)
                consumirServicio(
                    tipo=1, url=url[0], text=json.dumps([{"server": "ok"}])
                )
                t.sleep(2)
                attempts = 0
                segundos = 1
        except TypeError:
            attempts += 1
        segundos += 3
        print("\n\nNo se puede establecer conexión con servicios web...")
        print("Si el problema persiste contacte al administrador...")
        print(
            "Volviendo a intentar en {} segundos... Intentos: {}".format(
                segundos, attempts
            )
        )
        tt.sleep(segundos)
    else:
        print(
            "No es posible conectarse con el servidor. Pongase en contacto con el administrador."
        )
        print("Llamando al Sensor...")
    print(
        "Monitoreo finalizado.\nSiguiente Monitoreo en {} segundos.".format(MONITOREO)
    )
    t.sleep(MONITOREO)
