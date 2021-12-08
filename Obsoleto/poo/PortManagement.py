#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import platform
import socket

class PortManagement:

	def __init__(self, port):
		self.thisPort = port
		self.thisSistema = platform.system()

	def openPort(self):
		if(self.thisSistema == "Windows"):
			ruleName="ClosePort"+str(self.thisPort)
			command = 'netsh advfirewall firewall delete rule name="'+ruleName+'"'
			output = subprocess.Popen(command)

		elif(thisSistema == "Linux"):
			import pyufw as ufw #https://pypi.org/project/pyufw/
			if (ufw.status()["status"] == "inactive"):
				ufw.enable()
			ufw.add("delete deny "+str(self.thisPort))
			ufw.reload()
		else:
			print("Se esperaba Windows o Linux. Se recibió"+self.thisSistema)

	def closePort(self):
		if(self.thisSistema == "Windows"):
			ruleName="ClosePort"+str(self.thisPort)
			command = 'netsh advfirewall firewall add rule name="'+ruleName+'" protocol=TCP dir=out remoteport='+str(self.thisPort)+' action=block'
			output = subprocess.Popen(command)
		elif(thisSistema == "Linux"):
			import pyufw as ufw #https://pypi.org/project/pyufw/
			if (ufw.status()["status"] == "inactive"):
				ufw.enable()
			ufw.add("deny "+str(self.thisPort))
			ufw.reload()
		elif(thisSistema == "Darwin"):
			pass
			#cerrar los puertos
		else:
			print("Se esperaba Windows o Linux. Se recibió "+self.thisSistema)

	def probarPuerto(self, ip, puerto, thisSocket):
	    try:
	        thisSocket.connect((ip, puerto))
	        return True
	    except:
	        return False

	def scanPort(self, ip):
		port = int(self.thisPort)
		try:
		    thisSocket = socket.socket(2, 1) #socket.AF_INET, socket.SOCK_STREAM
		    resultado = self.probarPuerto(ip, port, thisSocket)
		    if resultado == True:
		        print("Puerto %d abierto." %port)
		    else:
		        print("Puerto %d cerrado." %port)

		except KeyboardInterrupt:
		    print ("Interrupcion por usuario.")
		    sys.exit()

		except socket.gaierror:
		    print ('No se encontró el host. Cerrando')
		    sys.exit()

		except socket.error:
		    print ("No se pudo conectar al servidor")
		    sys.exit()

	def blockIP(self):
		ip = self.thisPort
		if(self.thisSistema== "Windows"):
			try:
				ruleName ="BlockIP"+str(ip)
				remoteIP = str(ip)+"/32" 
				command = 'netsh advfirewall firewall add rule name="'+ruleName+'" dir=in interface=any action=block remoteip='+remoteIP
				output = subprocess.Popen(command)
			except ValueError:
				print("Error Ingrese una ip válida")
			except IndexError:
				print("Error de formato. Ingresar ip como primer argumento")
		else:
			pass