import logging 
import joblib #docs: https://joblib.readthedocs.io/en/latest/generated/joblib.load.html
import pandas as pd #docs: https://pandas.pydata.org/docs/
import threading
import subprocess, sys
import datetime as d

RUTA_SNIFF = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Sensor\\"
RUTA_LOG = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Monitoring\\log.txt"    
RUTA_MODELS = "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Pre-processing\\"

class Monitoring:
    def __init__(self):
        self.__rutaSniff = RUTA_SNIFF
        self.__rutaModels = RUTA_MODELS
        self.__rutaLog = RUTA_LOG
        self.__model = None
        self.__modelo = None
        self.__df = None

    def classifyData(self):
        print("Clasificando data...")
        for i in range(len(self.__df)):
            df2 = self.__df.drop(columns =['port', 'source_ip'])
            a = df2.iloc[[i]]
            if self.__model.predict(a)[0] == 1:
                multival = self.__modelo.predict(a)[0]
                if multival == 0:
                    multival = "Analysis"
                elif multival == 1:
                    multival = "Backdoor"
                elif multival == 2: 
                    multival = 'DoS'
                elif multival == 3:
                    multival = 'Exploits'
                elif multival == 4:
                    multival = "Fuzzers"
                elif multival == 5:
                    multival = "Generic"
                elif multival == 7:
                    multival = "Reconnaissance"
                elif multival == 8:
                    multival = "Shellcode"
                elif multival == 9:
                    multival == "Worms"
                threading.current_thread().name = multival
                fecha, hora = self.__generateDate()
                self.__log(self.__df['port'].iloc[[i]].tolist()[0], multival, fecha, hora, self.__df['source_ip'].iloc[[i]].tolist()[0])
        print("Archivo Log generado...")

    def generateModels(self):
        print("Generando modelos...")
        self.__model = joblib.load(self.__rutaModels+"multiclass.pkl")
        self.__modelo = joblib.load(self.__rutaModels+"modelmulti.pkl")

    def readFile(self):
        print("Leyendo archivos...")
        self.__df = pd.read_csv(self.__rutaSniff+"snif.csv", sep = '\s+')
        self.__df.columns = ('source_ip','dur','smean','sbytes','ackdat','sload','dload','dmean','port')
        
        self.__df = self.__df.dropna()
        
        self.__df['sload'] = pd.to_numeric(self.__df['sload'].str.rstrip('*'))
        self.__df['dload'] = pd.to_numeric(self.__df['dload'].str.rstrip('*'))
        self.__df = self.__df[self.__df.dur != 0]

    def __log(self, port, aType, date, hora, ip):
        logger = logging.getLogger('localhost')
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.__rutaLog)
        logger.addHandler(handler)
        if (logger.hasHandlers()):
            logger.handlers.clear()
        logger.addHandler(handler)
        logger.debug('Port: {} \t Tipo: {} \t Fecha: {} \t Hora: {} \t IP: {}'.format(port, aType, date, hora, ip))

    def callAnalyzer(self):
        #subprocess.call([sys.executable, "..\Analyzer\Analyzer.py"]) <-ORIGINAL
        subprocess.call([sys.executable, "..\Analyzer\Analyzer.py"])

    def __generateDate(self):
        now = d.datetime.today()
        fecha = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        hora = now.strftime("%H:%M:%S")
        return fecha, hora


###############
if __name__ == '__main__':
    print("\n\tMonitoring")
    m = Monitoring()
    m.generateModels()
    m.readFile()
    m.classifyData()
    m.callAnalyzer()