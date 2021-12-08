#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys, subprocess
import csv

RUTA_REGISTRO_ATAQUES = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Analyzer\\ataques_procesados.csv"

CLOSE_PORT_RESPONSES = ["Backdoor", "Exploits", "Shellcode"]
BLOCK_IP_RESPONSES = ["DoS", "Fuzzers"]
CUARENTENA_RESPONSES = ["Worms", "Generic"]

'''
por ahora, solo recibe los puertos.

file = ruta con el archivo log
'''
class Planner:
    def __init__(self, path = "test.log"):
        self.__file = path
        
    def sendPlan(self, strInfo):
         subprocess.call([sys.executable, "..\Executer\Executer.py", strInfo])
    
    def generatePlan(self):
        #TODO 
        pass

    def getPuertos(self):
        return self.__file

    '''
    Parametros: none

    Retorna: 
        strInfo: String
    
    Lee el archivo log y retorna un string de la siguiente forma:
        "puerto1, tipo_de_ataque1; puerto2, tipo_de_ataque2; puerto3, tipo_de_ataque4.tipo_de_ataque5;"

            *Nota:  
                notar que en puerto3, tipo de ataque 4 y tipo de ataque 5, están con un "."
                Esto indica que al puerto 3 llegaron dos ataques. Si fueran más estos
                tambien estarían separados por un "."
    '''
    def getFileInfo(self):
        print("Obteniendo información desde archivo...")
        contramedida = ""
        strInfo = ""
        with open(self.__file) as archivo:
            csv_reader = csv.reader(archivo, delimiter=',')
            for row in csv_reader:
                if row != []:
                    #row0: port, row1: ataque
                    ataques = row[1].strip('"').split(",")
                    contramedida=self.classify(row[0],ataques)+";"
                    
                    strInfo+=row[0]+","+contramedida[:-1]+";"
                else: pass
        return strInfo

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
if __name__ == '__main__':
    print("\n\tPlanner")
    #sys.argv[1]: contiene la ruta del archivo csv generado por Analyzer
    try:
        planner = Planner(sys.argv[1])
    except:
        planner = Planner(RUTA_REGISTRO_ATAQUES)

    plan = planner.getFileInfo()
    print(plan)
    planner.sendPlan(plan)
  
