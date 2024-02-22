import pandas as pd
import subprocess, sys
import graypy
import sklearn
import socket
import os


COMANDO_ARGUS = 'ubuntu run "argus -r snif.pcap -w snif.argus && ra -Lo -s  srcip sport dstip dsport proto state dur sbytes dbytes sttl dttl sloss dloss sload dload spkts dpkts swin dwin stcpb dtcpb smeansz dmeansz sjit djit stime ltime sintpkt dintpkt tcprtt synack ackdat label, -r snif.argus > snif.csv "'


class Preprocessing:
    def __init__(self):
        self.__comandoArgus = COMANDO_ARGUS

    def callArgus(self):
        print("Corriendo argus...")
        subprocess.call(self.__comandoArgus, shell=True)

    def callMonitoring(self):
        subprocess.call([sys.executable, "..\Monitoring\Monitoring.py"])


#############
if __name__ == "__main__":
    print("\n\tPre-processing")
    pp = Preprocessing()
    pp.callArgus()
    pp.callMonitoring()
