#!/usr/bin/python
#-*- coding: utf-8 -*-
import subprocess
import sys
import platform
import socket

class PortManagement:
    def __init__(self, port):
        self.thisPort = port
        self.thisSistema = platform.system()
        
    def ClosePort(self):
        if (self.thisSistema == "Windows"):
            ruleName = "ClosePort"+str(self.thisPort)
            command = 'netsh advfirewall firewall add rule name="'+ruleName+'" protocol=TCP dir=out remoteport='+str(self.thisPort)+' action=block'
            output = subprocess.Popen(command)
        else:
            pass

    def openPort(self):
        if(self.thisSistema == "Windows"):
            ruleName = "ClosePort"+str(self.thisPort)
            command = 'netsh advfirewall firewall delete rule name="'+ruleName+'"'
            output = subprocess.Popen(command)
        else:
            pass

    def probarPuerto(self, ip, puerto, thisSocket):
        try:
            thisSocket.connect((ip, puerto))
            return True
        except:
            return False

    def scanPort(self, ip):
        try:
            port = int(self.thisPort)
            thisSocket = socket.socket(2, 1) #socket.AF_INET, socket.SOCK_STREAM
            resultado = self.probarPuerto(ip, port, thisSocket)
            if resultado == True:
                print("Puerto %d abierto." %port)
            else:
                print("Puerto %d cerrado." %port)
        except:
            print("Hubo un problema :(")

    def blockIP(self):
        ip = self.thisPort
        try:
            ruleName = "BlockIP"+str(ip)
            remoteIP = str(ip)+"/32"
            command = 'netsh advfirewall firewall add rule name="'+ruleName+'" dir=in interface=any action=block remoteip='+remoteIP
            output = subprocess.Popen(command)
        except:
            print("Ok, Houston, we've had a problem here")

