#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import sys
from threading import Thread
import Log as l

VALID_NAMES = ["ClosePort", "OpenPort", "ScanPort", "blockIP"]

class Executer:
    def __init__(self):
        self.entrada = ""
        self.__confirm = False

    '''
        Parametros:
            name: String con el nombre de la funcion a ejecutar.
            args: Lista con el puerto y/o la IP

        Envía las instrucciones al Executar para ejecutar las funciones
        llegadas desde el planner.
    '''
    def exec(self, name, args):
        flag = self.getFlag(name)
        try:
            port = int(args[0])
            error = "no"
        except:
            error = "port error"
        
        if(error != "port error"):
            if(flag != "error"):
                try:
                    if(flag == "-s"):
                        subprocess.call([sys.executable, "..\Executer\Actuador.py", args[0], flag, args[1]])
                    else:
                        subprocess.call([sys.executable, "..\Executer\Actuador.py", args[0], flag])
                    self.log(name)
                    return ("OK")
                except ValueError:
                    return ("Error de forma")
                except IndexError:
                    return("Error de opción")
                except:
                    return("No se pudo nomás.")
            else:
                return ("flag error")
        else:
            return error
    
    def log(self, name):
        l.log(name)

    '''
        Entrada: representa los comandos a ejecutar. Es un string.

        La función maneja el string y le da el formato necesario.
        lo divide en una lista para poder ejecutar las funciones necesarias
        La entrada que recibe es de la siguiente forma:
        NombreFunción, Puerto

        Si se encuentra "-m" se habilita la ejecución en paralelo
    '''
    def manageEntry(self):
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
        for item in comandos:
            if (item != []):
                print(item)
                if( ["-m"] in item):
                    try:
                        if(item[0] in VALID_NAMES):
                            self.generarThreads(item[1:])
                            return str(comandos)
                        else:
                            print("Formato de entrada incorrecto")
                    except:
                        return ("Formato de entrada incorrecto")
                else:
                    if(item[0] in VALID_NAMES):
                            self.exec(item[0], item[1:])
                            return str(comandos)
                    else:
                        return "Formato de entrada incorrecto"
        
    def getFlag(self, name):
        if name=="ScanPort":
            return "-s"
        elif name == "ClosePort":
            return "-c"
        elif name == "OpenPort":
            return "-o"
        elif name == "BlockIp":
            return "-B"
        else:
            return "error" 
    '''
        listaComando: Lista con las funciones a ejecutar en paralelo

        Recorre la lista y ejecuta todas las funciones en ella en paralelo.
    '''
    def generarThreads(self, listaComando):
        print("Generar threads:",listaComando)
        for item in listaComando:
            try:
                name = item[0]
                lista = item[1:]
                Thread(target= self.exec, args = (name, lista)).start()
            except ValueError:
                print("Error de ingreso")
            except:
                pass
    
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
        
        #TODO: Agregar soporte para las IPS
        print("Se aplicarán las siguientes medidas:")
        for key, value in MEDIDAS_TOMADAS.items():
            if key == "BlockIP":
                print("La acción: {} se aplicará a las siguientes IP(s):\t {}".format(key, value))
            else:
                print("La acción: {} se aplicará a los siguientes puerto(s):\t {}".format(key, value))

        print("\nNo se recomienda ejecutar las medidas.\nSe tendrán que borrar manualmente las medidas si se ejecutan.\nDesea continuar? [N/y]")
        #value = input("")
        value = "N" #BORRAR ESTO 
        if value == "N" or value =="n" or value == "":
            pass
        elif value == "Y" or value == "y":
            self._confirm = True
        else:
            pass
    
    def setEntrada(self, comando):
        self.entrada = comando

    def getEntrada(self):
        return self.entrada

    def getConfirm(self):
        return self.__confirm

if __name__ == '__main__':
    print("\n\tExecuter...")

    #comandos: se recibe como argumento desde planner. 
    #          es una lista de tuplas.

    print("Recibiendo comandos...")
    
    comandos = sys.argv[1] 
    print(comandos)
    e = Executer()
    e.setEntrada(e.decode(comandos))
    e.report(comandos)
    
    if e.getConfirm():
        e.manageEntry()
        print("Medidas aplicadas.")
    else:
        print("No se aplicaron medidas.")
    