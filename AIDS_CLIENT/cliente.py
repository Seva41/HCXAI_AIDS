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

MAQUINA = config["CLIENTE"]["MAQUINA"]

# server_address = ("localhost", 5555)  # Local
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


def consumirServicio(tipo, url, payload=None):
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
    logData = []
    logData.append({"maquina": MAQUINA})
    now = dt.datetime.today()
    fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    hora = now.strftime("%H:%M:%S")
    dic = {"Componente": componente, "Funcion": func, "Fecha": fecha, "Hora": hora}
    logData.append(dic)
    payload = json.dumps(logData)
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post(url[2], data=payload, headers=headers)


def cliente():
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
