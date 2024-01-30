class DataAtaque:
    def __init__(self):
        self.__puerto = None #puerto/ip
        self.__cantidadAtaques = {} #dict: key=ataque, value=cantidad ataques en ese puerto
        self.__fecha = {}    #Fecha Primera Detección key=ataque, value=(primera deteccion, ultima detección) 
        self.__hora = {}    #Fecha Última Detección key=ataque, value=(primera deteccion, ultima detección)
        #self.__ips = None

    def setPuerto(self, puerto):
        self.__puerto = puerto

    def setCantidadAtaques(self, key, value):
        if len(key) == len(value):
            for i in range(0,len(key)):
                self.__cantidadAtaques[key[i]] = value[i]
        else:
            print("Error. No se puede continuar. Datos no coinciden...")


    def setHora(self, key, horaPrimera, horaUltima):
        if len(key) == len(horaPrimera) == len(horaUltima):
            for i in range(0,len(key)):
                self.__hora[key[i]] = (horaPrimera[i], horaUltima[i])
        else:
            print("Error. No se puede continuar. Datos no coinciden...")
            
    def setFecha(self, key, fechaPrimera, fechaUltima):
        if len(key) == len(fechaPrimera) == len(fechaUltima):
            for i in range(0,len(key)):
                self.__fecha[key[i]] = (fechaPrimera[i], fechaUltima[i])
        else:
            print("Error. No se puede continuar. Datos no coinciden...")

    def setIp(self, ip):
        self.__ip = ip

    def getData(self):
        #Retorna de lo siguiente:
        #1) puerto o ip
        #2) diccionario con ataques y veces detectados. key: Ataque, Value: veces detectado
        #3) diccionario con tipo de ataque y sus fechas de la primera detección y ultima
        #4) diccionario con tipo de ataque y sus horas de la primera detección y ultima
        #5) ip source
        return self.__puerto, self.__cantidadAtaques, self.__fecha, self.__hora
