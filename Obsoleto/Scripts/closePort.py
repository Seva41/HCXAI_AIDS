#!/usr/bin/env python
# -*- coding: utf-8 -*-

import subprocess
import sys
import platform

'''
Por ahora solo funciona en Windows
TODO: Mac y Linux
'''

try:
	sistema = platform.system()
	if(sistema == "Windows"):
		port = int(sys.argv[1])
		ruleName="ClosePort"+str(port)
		command = 'netsh advfirewall firewall add rule name="'+ruleName+'" protocol=TCP dir=out remoteport='+str(port)+' action=block'
		output = subprocess.Popen(command)
	elif(sistema == "Linux"):
		import pyufw as ufw #https://pypi.org/project/pyufw/
		port = int(sys.argv[1])
		
		if (ufw.status()["status"] == "inactive"):
			ufw.enable()
		ufw.add("deny "+str(port))
		ufw.reload()
	elif(sistema == "Darwin"):
		pass
		#cerrar los puertos
	else:
		print("Se esperaba Windows o Linux. Se recibió "+sistema)
	
except ValueError:
    print('Primer argumento debe ser un numero.')
except IndexError:
    print('Ingresar numero de puerto como argumento.')

