#!/usr/bin/env python
# -*- coding: utf-8 -*-
import subprocess
import sys
import platform

sistema = platform.system()
try:
	if(sistema == "Windows"):
		ip = (sys.argv[1])
		ruleName ="BlockIP"+str(ip)
		remoteIP = str(ip)+"/32" 
		command = 'netsh advfirewall firewall add rule name="'+ruleName+'" dir=in interface=any action=block remoteip='+remoteIP
		output = subprocess.Popen(command)
except ValueError:
	print("Error Ingrese una ip válida")
except IndexError:
	print("Error de formato. Ingresar ip como primer argumento")