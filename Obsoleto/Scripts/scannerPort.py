#!/usr/bin/env python
# -*- coding: utf-8 -*-
import socket
import subprocess
import sys


def probarPuerto(ip, puerto):
    try:
        thisSocket.connect((ip,port))
        return True
    except:
        return False

try:
    port = int(sys.argv[1])
    ip = sys.argv[2]
    thisSocket = socket.socket(2, 1) #socket.AF_INET, socket.SOCK_STREAM

    resultado = probarPuerto(ip, port)
    if resultado == True:
        print("Puerto %d abierto." %port)
    else:
        print("Puerto %d cerrado." %port)

except ValueError:
    print('Primer argumento debe ser un numero.')

except IndexError:
    print('Ingresar [numero de puerto] [IP] como argumento.')

except KeyboardInterrupt:
    print ("Interrupcion por usuario.")
    sys.exit()

except socket.gaierror:
    print ('No se encontró el host. Cerrando')
    sys.exit()

except socket.error:
    print ("No se pudo conectar al servidor")
    sys.exit()