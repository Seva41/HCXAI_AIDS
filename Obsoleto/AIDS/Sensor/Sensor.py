from scapy.all import * #sniff y wrpcap | docs: https://scapy.readthedocs.io/en/latest/usage.html
import subprocess

SNIFF_TIME= 10
FILE_SOURCE = "\"C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Sensor\\snif.pcap\""
RUTA_DESTINO = "\"C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Pre-processing\\snif.pcap\""
COMANDO_COPY = "xcopy "+FILE_SOURCE+" "+RUTA_DESTINO+"* /Y"

class Sensor:
    def __init__(self):
        self.__sniffTime = SNIFF_TIME

    def sniff(self):
        print("Realizando sniff a la red. TIEMPO: {}...".format(self.__sniffTime))
        snif = sniff(timeout = self.__sniffTime)
        print("Generando archivo pcap...")
        wrpcap('snif.pcap', snif)
        self.__copySniff()

    def __copySniff(self):
        print("Enviando pcap a Pre-processing...")
        subprocess.Popen(COMANDO_COPY)

if __name__ == '__main__':
    print("\n\tSensor")
    s = Sensor()
    s.sniff()
    subprocess.call([sys.executable, "..\Pre-processing\Preprocessing.py"])
