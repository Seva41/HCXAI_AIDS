#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import PortManagement as p

class Actuador:
    def __init__(self, puerto):
    	self.__puerto = puerto

    def executeFunction(self, flag, ip="none"):
    	pm = p.PortManagement(self.__puerto)
    	if flag == "-c":
    		pm.ClosePort()
    	elif flag == "-o":
    		pm.openPort()
    	elif flag == "-s" and ip != "none":
    		pm.scanPort(ip)
    	elif flag == "-B":
    		pm.blockIP()
    	else:
    		self.error()
    	return flag

    def error(self):
    	return ("error")

'''
	input  	argv[1]: port/IP
			argv[2]: flag
			argv[3]: IP (solo en caso de scanear)
'''
try:
	e = Actuador(sys.argv[1])
	try:
		ip = sys.argv[3]
		e.executeFunction(sys.argv[2], ip=ip)
	except IndexError:
		e.executeFunction(sys.argv[2])
	except:
		e.error()
except IndexError:
	e = Actuador("error")
	e.error()
