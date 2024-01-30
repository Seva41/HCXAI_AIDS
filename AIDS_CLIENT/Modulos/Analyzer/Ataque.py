import datetime as d

class Ataque:
    def __init__(self, port):
        self.__port = port
        self.__dictAtaques = {} #key=tipo de ataque; value=cantidad de veces
        self.__dictFecha = {}   #key=tipo de ataque; value=[fechaPrimeraDeteccion, fechaUltimaDeteccion]
        self.__dictHora = {}    #key=tipo de ataque; value=[horaPrimeraDeteccion, horaUltimaDeteccion]
        self.__ips = {}         #key=tipo de ataque; value=[ip source]

    def addAttack(self, tipoAtaque):
        if tipoAtaque in self.__dictAtaques:
            self.__dictAtaques[tipoAtaque]+=1
        else:
            self.__dictAtaques[tipoAtaque] = 1

    def setFecha(self, tipo, fecha):
        if tipo in self.__dictFecha:
            self.__dictFecha[tipo][1] = fecha
        else:
            self.__dictFecha[tipo] = []
            self.__dictFecha[tipo].append(fecha)
            self.__dictFecha[tipo].append(fecha)

    def setHora(self, tipo, hora):
        if tipo in self.__dictHora:
            self.__dictHora[tipo][1] = hora
        else:
            self.__dictHora[tipo] = []
            self.__dictHora[tipo].append(hora)
            self.__dictHora[tipo].append(hora)
    
    def setIp(self, ip, tipo):
        if tipo in self.__ips:
            if ip not in self.__ips[tipo]:
                self.__ips[tipo].append(ip)
        else:
            self.__ips[tipo] = []
            self.__ips[tipo].append(ip)

    def getData(self):
        return self.__port, (self.__dictFecha, self.__dictHora, self.__dictAtaques, self.__ips)
