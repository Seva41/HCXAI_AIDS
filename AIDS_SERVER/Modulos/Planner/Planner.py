#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys, subprocess
import csv
import json
import requests


CLOSE_PORT_RESPONSES = ["Backdoor", "Exploits", "Shellcode"]
BLOCK_IP_RESPONSES = ["DoS", "Fuzzers"]
CUARENTENA_RESPONSES = ["Worms", "Generic"]

URL = "http://192.168.0.15:5555/pushsintomas"
'''
por ahora, solo recibe los puertos.

file = ruta con el archivo log
'''
class Planner:
    def __init__(self, path = "test.csv", maquina = ""):
        self.__file = path
        self.__maquina = maquina
        
    def sendPlan(self, strInfo):
        #subprocess.call([sys.executable, "..\Executer\Executer.py", strInfo])
        print("strInfo", strInfo)
        print("aqui deberia ir el servicio")

    def getPuertos(self):
        return self.__file

    '''
    Parametros: none

    Retorna: 
        plan: (String) Contiene el plan generado de la siguiente forma 
                "puerto1, tipo_de_ataque1; puerto2, tipo_de_ataque2; puerto3, tipo_de_ataque4.tipo_de_ataque5;"
        sintomas: (List<String>) Contiene los síntomas encontrados.

    Lee el archivo log y retorna un plan de mitigaciones (String) y sus síntomas (List)

            *Nota:  
                notar que en puerto3, tipo de ataque 4 y tipo de ataque 5, están con un "."
                Esto indica que al puerto 3 llegaron dos ataques. Si fueran más estos
                tambien estarían separados por un "."
    '''
    def getFileInfo(self):
        print("Obteniendo información desde archivo...")
        contramedida = ""
        plan = ""
        sintomas = ""
        dic ={}
        sintomas= []
        with open(self.__file) as archivo:
            csv_reader = csv.reader(archivo, delimiter=',')
            for row in csv_reader:
                if row != []:
                    #row0: port, row1: ataque
                    ataques = row[1].strip('"').split(",")
                    contramedida=self.classify(row[0],ataques)+";"
                    sintomas.append(ataques)
                    plan+=row[0]+","+contramedida[:-1]+";"
                else: pass
        if (plan == ""): 
            return ("No hay amenazas detectadas",[])
        else: 
            return (plan, sintomas)

    ''' 
        Parámetros:
            port: int
                puerto al que llegó el síntoma
            sintoma: String
                representa el sintoma que llegó desde analyzer.
        Retorna: String

        Recibe un síntoma y según él retorna el tipo de contramedida para ese síntoma.
    '''
    def classify(self, port, sintoma):
        print("Clasificando ataque: \n\tPuerto/IP: {}\tSíntoma(s): {}".format(port, sintoma))
        retorno = ""
        for item in sintoma:
            if item in CLOSE_PORT_RESPONSES:
                retorno+="ClosePort."
            elif item in BLOCK_IP_RESPONSES:
                retorno+="BlockIP."
            elif item in CUARENTENA_RESPONSES:
                retorno+="CUARENTENA."
            else:
                retorno+="NO-APLICA."
        return retorno[:-1]

    def __sendSintomas(self, port, sintomas):
        logData = []
        logData.append({"maquina": self.__maquina})
        dic ={
            "Port": port,
            "Sintoma": sintomas
        }
        logData.append(dic)
        payload = json.dumps(logData)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(URL, data=payload, headers=headers)
        return r.text
