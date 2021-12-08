import pandas as pd  
import subprocess, sys
import graypy
import sklearn
import socket
import os


COMANDO_ARGUS = "ubuntu run \"argus -r snif.pcap -w snif.argus && ra -Lo -s  saddr dur smeansz sbytes ackdat sload dload dmeansz dport, -r snif.argus > snif.csv \""


class Preprocessing:
    def __init__(self):
        self.__comandoArgus = COMANDO_ARGUS

    def callArgus(self):
        print("Corriendo argus...")
        subprocess.call(self.__comandoArgus, shell=True)

