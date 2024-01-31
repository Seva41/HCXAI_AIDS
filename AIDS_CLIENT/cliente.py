import subprocess
import sys
import datetime as dt
import json
from time import sleep
import threading as tt
import configparser
import logging
import requests
from Modulos.Classifier.Classifier import Classifier
from Modulos.Planner.Planner import Planner
from Modulos.Analyzer.Analyzer import Analyzer
from Modulos.Executer.Executer import Executer

# Configuración
config = configparser.ConfigParser()
config.read("config.ini")

FILE = config["CLIENTE"]["FILE"]
MAQUINA = config["CLIENTE"]["MAQUINA"]
MONITOREO = int(config["CLIENTE"]["SCAN_SEGUNDOS"])

server_address = ("localhost", 5555)  # Local
url = [
    "tcp://localhost:5555",
    "http://localhost:5555/pushclientdone",
    "http://localhost:5555/plans/Cliente_1.json",
    "http://localhost:5555/pushclientlogstats",
    "http://localhost:5555/pushserverdone",
]


class Analyzer:
    def __init__(self):
        pass

    def loadConfig(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)

        # Ejemplo de cómo obtener valores
        self.ruta_registro_ataques = config["ANALYZER"]["RUTA_REGISTRO_ATAQUE"]


def getFileData():
    print("Obteniendo datos del archivo...")
    data = []
    data.append({"maquina": MAQUINA})
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


def consumirServicio(tipo, url, payload=None):
    print("Consumiendo servicio...")
    try:
        if tipo == 1:
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            r = requests.post(url, data=json.dumps(payload), headers=headers)
            return r.text
        elif tipo == 2:
            # ...
            return "Datos desde el servidor"
        else:
            return "Error"
    except Exception as e:
        print(f"Error al consumir servicio: {e}")
        return "Error"


def log(componente, func):
    print("Enviando log...")
    logData = []
    logData.append({"maquina": MAQUINA})
    now = dt.datetime.today()
    fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    hora = now.strftime("%H:%M:%S")
    dic = {"Componente": componente, "Funcion": func, "Fecha": fecha, "Hora": hora}
    logData.append(dic)
    payload = json.dumps(logData)
    headers = {"Content-type": "application/json", "Accept": "text/plain"}

    # Debug
    print("Haciendo request...")
    print(f"URL de solicitud: {url[2]}")
    print(f"Datos de payload: {payload}")
    print(f"Cabeceras: {headers}")

    try:
        r = requests.post(url[2], data=payload, headers=headers)
        r.raise_for_status()  # Verificar si hay errores HTTP
        print("Request hecho")
    except requests.exceptions.RequestException as e:
        print(f"Error en la solicitud: {e}")


def cliente():
    print("Iniciando cliente...")
    classifier = Classifier(maquina="Cliente_1")
    planner = Planner()
    analyzer = Analyzer()
    analyzer.loadConfig("config.ini")
    executer = Executer()

    attempts = 0
    segundos = 1

    while True:
        try:
            fila = consumirServicio(tipo=2, url=url[2])
            log("server", "consumirServicio")

            print("Sensor")
            s = Sensor()
            s.sniff()
            log("Sensor", "sniff")

            print("Preprocessing")
            pp = Preprocessing()
            pp.callArgus()
            log("Preprocessing", "callArgus")

            print("Classifier")
            m = Classifier(MAQUINA)
            m.generateModels()
            log("Classifier", "generateModels")

            m.readFile()
            log("Classifier", "readFile")

            m.classifyData()
            log("Classifier", "classifyData")

            if "" in fila:
                fila.remove("")
            if fila == ["ok"]:
                print("Esperando...")
                sleep(2)
            else:
                # Ejemplos
                planes = [
                    {
                        "maquina": "Cliente_1",
                        "plan": "Plan_1",
                        "sintomas": ["Sintoma_1", "Sintoma_2"],
                    },
                    {
                        "maquina": "Cliente_2",
                        "plan": "Plan_2",
                        "sintomas": ["Sintoma_3", "Sintoma_4"],
                    },
                ]
                print("Enviando datos al servidor:", planes)

                for cliente in fila:
                    data = consumirServicio(tipo=2, url=url[1] + cliente + ".txt")
                    # ...

                postServer(url[3], json.dumps(planes))
                sleep(1)
                consumirServicio(tipo=1, url=url[0], payload=[{"server": "ok"}])
                sleep(2)
                attempts = 0
                segundos = 1
        except Exception as e:
            attempts += 1
            segundos += 3
            print(f"\n\nError al conectarse con servicios web: {e}")
            print(
                "Volviendo a intentar en {} segundos... Intentos: {}".format(
                    segundos, attempts
                )
            )
            sleep(segundos)


if __name__ == "__main__":
    cliente()
