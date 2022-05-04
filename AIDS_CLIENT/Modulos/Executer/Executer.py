#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import sys
from threading import Thread
import Modulos.Executer.Actuador as a
import logging
import datetime as dt
import requests
import json
from time import sleep
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

RUTA_LOG = config['EXECUTER']['RUTA_LOG']
MAQUINA = config['CLIENTE']['MAQUINA']

VALID_NAMES = ["ClosePort", "OpenPort", "ScanPort", "BlockIP"]

URL = "http://192.168.0.15:5555/pushclientlogtabla"

class Executer:
    def __init__(self):
        self.entrada = ""
        self.__confirm = False

    '''
        Parametros:
            port: puerto o ip a comprobar. <String>
            func: funcion a comprobar. <String>
        Retorna:
            Boolean: True si lo encuentra; False si no.
        Busca el puerto/ip y la función en el log para saber si ya fue aplicada o no la función.
    '''
    def comprobarAcciones(self, port, func):
        try:
            file = open(RUTA_LOG, 'r')
            for linea in file:
                lista = linea.split()
                if lista[1] == func and lista[3]==port:
                    return True
            return False
        except FileNotFoundError:
            return False
    '''
        Parametros:
            name: String con el nombre de la funcion a ejecutar.
            args: Lista con el puerto y/o la IP
            sintomas: Lista con los sintomas asociado a cada medida

        Envía las instrucciones al Executer para ejecutar las funciones
        llegadas desde el planner.
    '''
    def exec(self, name, args, sintoma):
        flag = self.getFlag(name)
        if flag != "-B":
            try:
                port = int(args[0])
                error = "no"
            except:
                error = "port error"
        elif flag == "-B":
            if ":" not in args[0]:
                port = args[0]
                error = "no"
            else: error = "port error"
        else:
            error = "port error"
            
        if(error != "port error"):
            if(flag != "error"):
                if(not self.comprobarAcciones(str(port),name)):
                    ac = a.Actuador(port)
                    if(flag == "-s"):
                        ac.executeFunction(flag, ip=args[1])
                    else:
                        ac.executeFunction(flag)
                    self.log(name, port, sintoma)
                    return ("OK")
                else: print("Saltando: port ->{} func ->{} (ya aplicado)".format(port,name))    
            else:
                return ("flag error")
        else:
            print ("ELSE:",error)
    
    def log(self, name, port, sintoma):
        now = dt.datetime.today()
        fecha = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        hora = now.strftime("%H:%M:%S")

        ##WEBSERVICE##
        logData =[]
        logData.append({"maquina": MAQUINA})
        dic = {
            "Funcion": name,
            "Port": port,
            "Fecha": fecha,
            "Hora": hora,
            "Sintoma": sintoma
        }
        logData.append(dic)
        payload = json.dumps(logData)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        ##############
        try:
            logger = logging.getLogger('Executer')
            logger.setLevel(logging.INFO)
            handler = logging.FileHandler(RUTA_LOG)
            logger.addHandler(handler)
            if (logger.hasHandlers()):
                logger.handlers.clear()
            logger.addHandler(handler)
            logger.info('Funcion: {} \t puerto/ip: {} \t Fecha: {} \t Hora: {} \t Sintoma: {}'.format(name, port, fecha, hora, sintoma))
            r = requests.post(URL, data=payload, headers=headers)
            sleep(1)
        except FileNotFoundError:
            file = open(RUTA_LOG, 'w')
            file.write('Funcion: {} \t puerto/ip: {} \t Fecha: {} \t Hora: {} \t Sintoma: {}'.format(name, port, fecha, hora, sintoma))
            r = requests.post(URL, data=payload, headers=headers)
            file.close()
            sleep(1)
        except:
            "No fue posible conectarse con web service."


    '''
        sintomas: Sintomas asociados a los ataque en el plan

        La función maneja el atributo entrada y le da el formato necesario.
        lo divide en una lista para poder ejecutar las funciones necesarias
        La entrada que recibe es de la siguiente forma:
        NombreFunción, Puerto

        Si se encuentra "-m" se habilita la ejecución en paralelo
    '''
    def manageEntry(self, sintomas):
        comandos = []
        lista = self.entrada.strip().split(";")

        listaComando = []
        #Variables auxiliares para decodificar la entrada.
        aux = []
        aux2 = []
        
        #Este for le da el formato a las listas. Dando como resultado una lista de listas
        #[['NombreFuncion', puerto], ['NombreFuncion', puerto, flag]]
        for item in lista:
            #Si detecta "-m" en la entrada, divide los comandos y quita los ( )
            if ("-m" in item):
                aux = item.strip("() ").split("(")

                for i in aux:
                    aux2.append(i.strip().split(","))
                aux.clear()
                aux.append(aux2[0])

                for item in aux2[1:]:
                    for i in item:
                        aux.append(i.strip().split())
                comandos.append(aux)
            else:
                listaComando = item.strip().split()
                comandos.append(listaComando)

        #Si hay un item "-m" dentro de los comandos, se ejecuta en paralelo, sino se ejecuta secuencial   

        index = 0
        for item in comandos:
            if (item != []):
                if( ["-m"] in item):
                    try:
                        if(item[0] in VALID_NAMES):
                            self.generarThreads(item[1:], sintomas)
                            return str(comandos)
                            
                        else:
                            print("Formato de entrada incorrecto")
                    except:
                        return ("Formato de entrada incorrecto")
                else:
                    if(item[0] in VALID_NAMES):
                        try:
                            self.exec(item[0], item[1:], sintomas[index])
                            index+=1
                        except IndexError:
                            pass
                    else:
                        print("Hay problema con:",item[0], item[1:])
            
        
    def getFlag(self, name):
        if name=="ScanPort":
            return "-s"
        elif name == "ClosePort":
            return "-c"
        elif name == "OpenPort":
            return "-o"
        elif name == "BlockIP":
            return "-B"
        else:
            return "error" 
    '''
        listaComando: Lista con las funciones a ejecutar en paralelo

        Recorre la lista y ejecuta todas las funciones en ella en paralelo.
    '''
    def generarThreads(self, listaComando, sintomas):
        print("Generar threads:",listaComando)
        index = 0
        for item in listaComando:
            try:
                name = item[0]
                lista = item[1:]
                Thread(target= self.exec, args = (name, lista, sintomas[index])).start()
            except ValueError:
                print("Error de ingreso")
            except:
                pass
            intex+=1
    
    '''
        Parámetros: 
                comandos: string que representa los comandos a ejecutar llegados desde planner
                          de la siguiente manera:
                        "PUERTO, MEDIDA;PUERTO, MEDIAD1.MEDIDA2;PUERTO,MEDIDA1.MEDIDA2;"
        retorna:
                salida: string con el formato adecuado para ejecutar las acciones.

        Recibe un string y lo modifica para que sea compatible con la entrada de Executer.
    '''
    def decode(self, comandos):

        entrada = comandos.split(";") #generando lista

        #intenta borrar algún elemento vacio de la lista. 
        try:
            entrada.remove("")
        except:
            pass #no pasa nada porque no lo encontró

        salida = ""
        
        #recorre los items de la lista y obtiene las acciones necesarias para
        #cada puerto y las concatena en un solo string.
        for item in entrada:
            aux = item.split(",")
            puerto = aux[0] if aux[0] != "https" else 443
            acciones = aux[1].split(".")
            #en caso de que en el puerto deban ser aplicadas varias medidas
            #concatena el puerto con dichas medidas
            for accion in acciones:
                salida += accion+" "+str(puerto)+";"
        return salida

    '''
        Parámetros:
                comandosExec: string sin procesar llegado desde Planner con instrucciones
        Retorna: 
                Nada

        Toma la entrada sin procesar llegada desde el planner, decodifica el mensaje e indica que 
        funciones deben ser tomadas y pide una confirmación para ejecutar funciones.
        (Esto cambiará, dado que será autonomo. Se pide confirmación porque aun no se implementan 
        metodos para revertir las medidas.).
    '''
    def report(self, comandosExec):
        puertos_executer = comandosExec.split(";")
        port_type = [] #matriz de la siguiente forma [ [puerto, [medidas]] ] *medidas es otra lista; son strings todos los contenidos
        

        for item in puertos_executer:
            port_type.append(item.split(","))
        print("\nPreparando medidas...")

        #por mientras que arreglo el ultimo item vacio
        port_type = port_type[:-1]
        for item in port_type:
            item[1] = item[1].split(".")

        #MEDIDAS_TOMADAS:   diccionario que alamacena la accion como key y los puertos (list) como value
        #PROBABLEMENTE ESTO CAMBIEN MÁS ADELANTE A UNA LISTA MÁS COMPLEJA (CON OBJETOS o DICT)
        MEDIDAS_TOMADAS = {}
        
        #Puerto: item[0] (String); Medidas: item[1] (List) 
        for item in port_type: 
            #intenta castear un numero en formtato string a int
            #si no puede pasa.
            try:
                port = item[0] if item[0] != "https" else 443 #si el puerto no es "https" lo deja tal cual, sino lo iguala a 443
                for medida in item[1]:
                    if medida in MEDIDAS_TOMADAS:
                        MEDIDAS_TOMADAS[medida].append(port)
                    else:
                        MEDIDAS_TOMADAS[medida] = [port]
            except:
                pass 
        
        print("Se aplicarán las siguientes medidas:")
        for key, value in MEDIDAS_TOMADAS.items():
            if key == "BlockIP":
                print("La acción: {} se aplicará a las siguientes IP(s):\t {}".format(key, value))
            else:
                print("La acción: {} se aplicará a los siguientes puerto(s):\t {}".format(key, value))

        print("\nLas medidas se tendrán que borrar manualmente")
        self.__confirm = True
    
    def setEntrada(self, comando):
        self.entrada = comando

    def getEntrada(self):
        return self.entrada

    def getConfirm(self):
        return self.__confirm
