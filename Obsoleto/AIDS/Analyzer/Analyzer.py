import csv
import datetime as d
import subprocess, sys
import Ataque as a
import DataAtaque as dt
import pandas as pd

RUTA_REGISTRO_ATAQUES = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Analyzer\\registro_ataques.csv"
RUTA_ATAQUES_PROCESADOS = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Analyzer\\ataques_procesados.csv"
RUTA_LOG_MONITORING = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Monitoring\\log.txt" 

'''
    Ataques máximos antes de reportar al planner
    por tipo de ataque:
    key =   tipo de ataque: String
    value = tolerancia máxima: int
'''
TOLERANCIA_ATAQUES = {
        "Analysis":10,
        "Backdoor":10,
        'DoS': 2,
        'Exploits':10,
        "Fuzzers": 10,
        "Generic": 10,
        "Reconnaissance":10,
        "Shellcode": 10,
        "Worms": 10
    }

'''
    Tiempo máximo entre ataques antes de reportar al planner
    por tipo de ataque:
    key = tipo de ataque: String
    value = (lapso de tiempo, unidad de tiempo): Tuple<int, String>

    D: Días, M: Meses, A: Años, S: Semanas
'''
TOLERANCIA_TIEMPO = {
        "Analysis":(3, "D"),
        "Backdoor":(3, "D"),
        'DoS': (3, "D"),
        'Exploits':(3, "D"),
        "Fuzzers": (3, "D"),
        "Generic": (3, "D"),
        "Reconnaissance":(3, "D"),
        "Shellcode": (3, "D"),
        "Worms": (3, "D")
    }

class Analyzer:
    def __init__(self):
        self.__toleranciaTiempo = TOLERANCIA_TIEMPO
        self.__toleranciaAtaques = TOLERANCIA_ATAQUES
        self.__archivo = RUTA_REGISTRO_ATAQUES
        self.__listaAtaque = [] #lista de Ataque

    '''
        Parámetros: no posee

        A partir de la información entregada por Monitoring genera un lista
        con los ataques detectados y la cantidad de veces.
        Compara esos valores con las ventanas de tiempo y cantidad de ataques tolerados
        y genera un archivo con los ataques que cumplan la ventana.
    '''
    def processData(self):
        listaDataAtaque = [] #List<DataAtaque>

        print("Obteniendo datos desde el registro de ataques...")
        #leyendo archivo y generando una lista (List<DataAtaque>)
        with open(self.__archivo) as archivo:
            csv_reader = csv.reader(archivo, delimiter=',')
            for row in csv_reader:
                if row != []:
                    #   row[0]: port, row[1]: ataques, row[2]: cantidadAtaque
                    #   row[3]: fechaPrimera, row[4]: horaPrimera, row[5]: fechaUltima
                    #   row[6]: horaUltima
                    #   row[7]: ips
                    puerto = row[0]
                    ataquesDetectados = row[1].split(";")
                    cantidadAtaques = row[2].split(";")
                    fechaPrimeraDeteccion = row[3].split(";")
                    fechaUltimaDeteccion = row[5].split(";")
                    horaPrimeraDeteccion = row[4].split(";")
                    horaUltimaDeteccion = row[6].split(";")
                    #ips = row[7].split(";")

                    ataque = dt.DataAtaque() #instancia objeto DataAtaque
                    ataque.setPuerto(puerto)
                    ataque.setCantidadAtaques(ataquesDetectados, cantidadAtaques)
                    ataque.setFecha(ataquesDetectados, fechaPrimeraDeteccion, fechaUltimaDeteccion)
                    ataque.setHora(ataquesDetectados, horaPrimeraDeteccion, horaUltimaDeteccion)
                    #ataque.setIp(ips)
                    listaDataAtaque.append(ataque)
                else: pass


        print("Procesando data...")
        dictAtaques = {} #diccionario de ataques detectado que cumplen con la ventana. key=puerto/ip; value= [] ataques asociados a ese puerto/ip
        for item in listaDataAtaque: #cada item es DataAtaque
            #getData retorna de la siguiente manera:
            #1) puerto
            #2) diccionario con ataques y veces detectados. key: Ataque, Value: veces detectado
            #3) diccionario con fecha de la primera detección y ultima. key: tipo ataque, Value: (primera fecha, ultima fecha)
            #4) diccionario con hora de la primera detección y ultima. key: tipo ataque, Value:  (primera hora, ultima hora)
            #5) ip source
            puerto, cantidadAtaques, fechas, horas = item.getData() #falta ip

            for key, value in fechas.items():

               if self.analizarVentana(value[0], value[1], key):
                   if int(cantidadAtaques[key]) > self.__toleranciaAtaques[key]:
                        if puerto in dictAtaques:
                            dictAtaques[puerto].append(key)

                        else:
                            if key != "DoS" or key != "Fuzzers":
                                dictAtaques[puerto] = [key]
                            else:
                                dictAtaques[puerto] = [key]
 
        self.writeDataCsv(mensaje="Generando resultados del analisis de incidencias v/s ventana de tiempo...", tipo = 2, args=dictAtaques)
        print("Analisis realizado correctamente...")

            
    '''
        Parámetros:
                    fechaPrimera: string
                    fechaUltima: string
        Retorna:
                Boolean

        Toma los strings, los converte en una lista y obtiene la diferencia de tiempo entre
        día, mes y año. Luego compara con la ventana de tiempo definida en las variables globales.
        Si la ventana se cumple (diferencia de tiempo entre ataques) retorna True
        sino se cumple retorna False.

        #TODO agregar soporte a las horas (por ahora solo aguanta fechas)
    '''
    def analizarVentana(self, fechaPrimera, fechaUltima, tipoAtaque):
        listaFechaPrimera = list(map(int, fechaPrimera.split("/")))
        listaFechaUltima = list(map(int, fechaUltima.split("/")))

        #Si los ataques son en el mismo día la diferencia da 0
        #por lo tanto siempre se sumará 1 a los días para contar el mismo día inicial.

        diffDia = abs(listaFechaPrimera[0] - listaFechaUltima[0]) + 1
        diffMes = abs(listaFechaPrimera[1] - listaFechaUltima[1])
        diffAño = abs(listaFechaPrimera[2] - listaFechaUltima[2])

        tolerancia = self.__toleranciaTiempo[tipoAtaque][0]
        medida = self.__toleranciaTiempo[tipoAtaque][1]

        biciesto = self.isBiciesto(listaFechaUltima[2])
        
        meses = [31, 29 if biciesto else 28, 31, 30, 31,30,31,31,30,31,30,31] #0 enero, 11 diciembre
        
        if medida == "D": #dia
            if diffMes > 2 or diffAño > 0:
                return True
            elif diffMes == 1:
                #meses[listaFechaPrimera[1]-1]: cantidad de días que tiene el mes.
                #listaFechaPrimera[0] +1: Día del mes de la primera detección (+1 para contar el día mismo)
                #listaFechaUltima[0]: día del siguiente mes.
                #La suma de estos son la diferencia de días totales detectados.
                if (meses[listaFechaPrimera[1]-1] - listaFechaPrimera[0] +1) + listaFechaUltima[0] >= tolerancia:
                    return True
                else: return False
            elif diffMes == 0:
                if diffDia > tolerancia:
                    return True
                else: return False
            else: return False

        elif medida == "M": #mes
            if diffMes > tolerancia:
                return True
            elif diffMes == tolerancia:
                if (meses[listaFechaPrimera[1]-1] - listaFechaPrimera[0]+1) + listaFechaUltima[0] >= meses[listaFechaPrimera[1]-1]:
                    return True
                else: return False
            else:
                return False

        elif medida == "A": #año
            if diffAño == tolerancia:
                if listaFechaUltima[1] - listaFechaPrimera[1] > 0:
                    return True
                elif listaFechaUltima[1] - listaFechaPrimera[1] == 0:
                    if listaFechaUltima[0] - listaFechaPrimera[0] >= 0:
                        return True
                    else: return False
                else: return False
            elif diffAño > tolerancia:
                return True
            else:
                return False

        elif medida == "S": #semana
            if diffMes > 1:
                if diffMes/4 >= tolerancia: return True
                else: return False
            elif diffMes == 1:
                if int(((meses[listaFechaPrimera[1]-1] - listaFechaPrimera[0] +1) + listaFechaUltima[0])/7) >= tolerancia: return True
                else: return False
        
            elif diffMes == 0:
                if int(diffDia/7) >= tolerancia:
                    return True
                else: return False
            else: return False
        else: return False

    def isBiciesto(self, año):
        if año%400 == 0:
            return True
        elif año%4 == 0 and año%100 != 0:
            return True
        else:
            return False

    '''
        Parametros: no posee

        Lee archivo log del monitoring y extrae la información
        para agregarla a listaAtaque.
        
        listaAtaque es un matriz de la siguiente forma [[puerto, Ataque]]
        Puerto: [int] número de puerto
        Ataque: [Ataque]  Objeto Ataque que contiene el puerto, ataques dirigidos a ese puerto
        y la fecha en la que se generó el último ataque.
    '''
    def generateList(self):
        print("Obteniendo datos de ataques...")
        file = open(RUTA_LOG_MONITORING, "r")
        for linea in file:
            info = linea.split()
            t = (info[1], info[3], info[5], info[7], info[9]) #[0] puerto, [1] tipo, [2] fecha, [3] hora, [4] ip
            
            if t[1] == "DoS" or t[1] == "Fuzzers":
                puerto = t[4]
            else: puerto = t[0]

            #puerto = t[0] if t[1] != "DoS" or t[1] != "Fuzzers" else t[4]
            encontrado, index = self.__search(puerto)
            if encontrado: #si el puerto ya se encuentra registrado
                self.__listaAtaque[index][1].addAttack(t[1])
                self.__listaAtaque[index][1].setFecha(tipo=t[1] ,fecha=t[2])
                self.__listaAtaque[index][1].setHora(tipo=t[1], hora=t[3])
                #self.__listaAtaque[index][1].setIp(tipo=t[1], ip=t[4])
            else:
                ataque = a.Ataque(puerto)
                ataque.addAttack(t[1])
                ataque.setFecha(tipo=t[1], fecha=t[2])
                ataque.setHora(tipo=t[1], hora=t[3])
                #ataque.setIp(tipo=t[1], ip=t[4])
                self.__listaAtaque.append([puerto, ataque])

        file.close()

    '''
        Parametros:
            port: int
                Numero de puerto a buscar en la lista
        Retorna: 
                Boolean, index (int)

        Busca un puerto en listaAtaque.
        Si lo encuentra retorna True, sino False. Junto con eso retorna su índice en la lista 
    '''
    def __search(self, port):
        flag = False
        index = None
        for item in self.__listaAtaque:
            if item[0] == port:
                flag = True
            if flag: 
                index = self.__listaAtaque.index(item)
                break
        return flag, index

    '''
        Parametros:
            tipo: int
                indica que función ejecutar. 1 = Crear regristro de ataques sin procesar. 2 = Crear registro de datos procesador
            args: (solo cuando tipo = 2)
                contiene la información para escribir en un archivo.
        Parametros opcionales:
           mensaje: String
                El mensaje que se mostrará cuando se ejecute la función. 
               
    Genera un archivo csv con los puertos, ataques detectado y fecha. Este puede ser de data procesada o antes de procesarla
    las columnas son:
        puerto, tipo, cantidad, fecha primera detección, hora primera deteccion,  hora primera deteccion, hora ultima deteccion
    La información la obtiene de listaAtaque
    '''

    def writeDataCsv(self, tipo, mensaje = None, args = None):
        if mensaje: print(mensaje)

        if tipo == 1: #tipo 1: crear registro de ataques sin procesar
            port = ""
            ataques = ""
            vecesPresente = ""
            fechaPD = ""    #primeraDeteccion
            horaPD = ""     #primeraDeteccion
            fechaUD = ""    #ultimaDeteccion
            horaUD = ""     #ultimaDeteccion
            ips = ""        #ips source
            with open(self.__archivo, mode="w") as archivo:
                archivo_writer = csv.writer(archivo, delimiter =',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                
                for item in self.__listaAtaque:
                    port, tupleAux = item[1].getData()
                    #tupleAux contiene: [0]dictFecha, [1]dictHora, [2]dictAtaques, [3]dictIp (todos diccionarios)
                    #los 3 ciclos recorren estos diccionarios (consultar clase Ataque.py para ver keys y values)
                    for key, value in tupleAux[0].items():
                        fechaPD+=value[0]+";"
                        fechaUD+=value[1]+";"

                    for key, value in tupleAux[1].items():
                        horaPD+=value[0]+";"
                        horaUD+=value[1]+";"

                    for key, value in tupleAux[2].items():
                        ataques+=str(key)+";"
                        vecesPresente+=str(value)+";"
                    '''
                    for key, value in tupleAux[3].items():
                        if key == "DoS" or key == "Fuzzers":
                            ips+=key+"-"
                            for i in value:
                                ips+=str(i)+";"
                    '''

                    archivo_writer.writerow([port,ataques[:-1],vecesPresente[:-1],fechaPD[:-1], horaPD[:-1], fechaUD[:-1], horaUD[:-1]])
                    ataques=""
                    vecesPresente=""
                    fechaPD=""
                    fechaUD=""
                    horaPD=""
                    horaUD=""
                    ips=""
            archivo.close ()
        
        elif tipo == 2: #crear registro de ataques procesados
            with open(RUTA_ATAQUES_PROCESADOS, mode="w") as archivo:
                archivo_writer = csv.writer(archivo, delimiter =',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                for key, value in args.items(): #key = puerto/ip value = ataque (List)
                    archivo_writer.writerow([key,",".join(value)])
                archivo.close()
        else:
            print("Error.")

    def callPlanner(self):
        subprocess.call([sys.executable, "..\Planner\Planner.py", RUTA_ATAQUES_PROCESADOS])

                     #ONLY TEST
######################################################
######################################################     
    def setToleranciaTiempo(self, key, value):   #####  
        if key in self.__toleranciaTiempo:       #####  
            self.__toleranciaTiempo[key] = value #####     
                                                 #####  
                                                 #####  
    def setToleranciaAtaques(self, key, value):  #####  
        if key in self.__toleranciaAtaques:      #####  
            self.__toleranciaAtaques[key] = value#####
                                                 #####   
######################################################          
######################################################

if __name__ == '__main__':
    print("\n\tAnalyzer")
    an = Analyzer()
    an.generateList()
    an.writeDataCsv(tipo=1, mensaje="Generando registro de ataques...")
    an.processData()
    an.callPlanner()