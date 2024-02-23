from scapy.all import * #sniff y wrpcap | docs: https://scapy.readthedocs.io/en/latest/usage.html
import subprocess
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

SNIFF_TIME = int(config['SENSOR']['SNIFF_TIME'])


class Sensor:
    def __init__(self):
        self.__sniffTime = SNIFF_TIME

    def sniff(self):
        print("Realizando sniff a la red. TIEMPO: {}...".format(self.__sniffTime))
        snif = sniff(timeout = self.__sniffTime)
        print("Generando archivo pcap...")
        wrpcap('snif.pcap', snif)