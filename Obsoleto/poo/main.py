#!/usr/bin/env python
# -*- coding: utf-8 -*-
from PortManagement import *
import sys

def error():
	print("Error de ingreso. \nUsar el flag -h para ayuda.")

try:
	pm = PortManagement(sys.argv[1])

	if (sys.argv[1] == "-h"):
		print("[-o] Abrir puerto. Ej: main.py [número de puerto] -o\n[-c] Cerrar puerto: Ej: main.py [número de puerto] -c\n[-s] Escanear puerto. Ej: main.py [número de puerto] -s [IP]\n[-B] Bloquear una IP: Ej. main.py [número de ip] -B")

	elif (sys.argv[2] == "-o"):
		try:
			pm.openPort()
		except:
			error()

	elif(sys.argv[2] == "-c"):
		try:
			pm.closePort()
		except:
			error()

	elif(sys.argv[2] == "-s"):
		try:
			pm.scanPort(sys.argv[3])
		except IndexError:
			error()
		except KeyboardInterrupt:
		    print ("Interrupcion por usuario.")
		    sys.exit()

		except socket.gaierror:
		    print ('No se encontró el host. Cerrando')
		    sys.exit()

		except socket.error:
		    print ("No se pudo conectar al servidor")
		    sys.exit()
	elif(sys.argv[2] == "-B"):
		try:
			pm.blockIP()
		except ValueError:
			print("Error Ingrese una ip válida")
		except IndexError:
			print("Error de formato. Ingresar ip como primer argumento")
	else:
		error()

except ValueError:
	print("value error")
	error()
except IndexError:
	print("index error")
	error()


