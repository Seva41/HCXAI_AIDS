#!/usr/bin/python
#-*- coding: utf-8 -*-
import sys
import Modulos.Executer.PortManagement as p


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
	
	def error(self):
		return ("error")

