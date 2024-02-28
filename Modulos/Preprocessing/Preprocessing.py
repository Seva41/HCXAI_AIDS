import pandas as pd
import subprocess, sys
import graypy
import sklearn
import socket
import os


# COMANDO_ARGUS = "ubuntu run \"argus -r snif.pcap -w snif.argus && ra -Lo -s  saddr dur smeansz sbytes ackdat sload dload dmeansz dport, -r snif.argus > casi.csv \""
COMANDO_ARGUS = 'ubuntu run "argus -r snif.pcap -w snif.argus && ra -Lo -s saddr daddr dur smeansz sbytes ackdat sload dload dmeansz dport srcip sport dstip dsport proto state dbytes sttl dttl sloss dloss spkts dpkts swin dwin stcpb dtcpb sjit djit stime ltime sintpkt dintpkt tcprtt synack label, -r snif.argus > casi.csv "'


class Preprocessing:
    def __init__(self):
        self.__comandoArgus = COMANDO_ARGUS

    def callArgus(self):
        print("Corriendo argus...")
        subprocess.call(self.__comandoArgus, shell=True)
        with open("casi.csv", "r") as inputdata:
            # Agregar features calculables

            # Sacar values
            with open("snif.csv", "w+") as outputdata:
                outputdata.write(inputdata.read().replace("*", ""))
