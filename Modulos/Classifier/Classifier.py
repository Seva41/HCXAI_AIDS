import logging
import joblib  # docs: https://joblib.readthedocs.io/en/latest/generated/joblib.load.html
import pandas as pd  # docs: https://pandas.pydata.org/docs/
import threading
import subprocess, sys
import datetime as d

import os
import json, requests
from urllib import request
import configparser

config = configparser.ConfigParser()
config.read("config.ini")
RUTA_SNIFF = config["CLASSIFIER"]["RUTA_SNIFF"]
RUTA_LOG = config["CLASSIFIER"]["RUTA_LOG"]
RUTA_MODELS = config["CLASSIFIER"]["RUTA_MODELS"]

url = [
    "http://192.168.0.103:5555/pushdatanew",
    "http://192.168.0.103:5555/pushdataappend",
]


class Classifier:
    def __init__(self, maquina):
        self.__maquina = maquina
        self.__rutaSniff = RUTA_SNIFF
        self.__rutaModels = RUTA_MODELS
        self.__rutaLog = RUTA_LOG
        self.__model = None
        self.__modelo = None
        self.__df = None

    def classifyData(self):
        try:
            os.remove(self.__rutaLog)
        except:
            pass

        print("Clasificando data... Esto podría demorar un tiempo...")
        cont = 1
        for i in range(len(self.__df)):
            df2 = self.__df.drop(columns=["port", "source_ip"])
            a = df2.iloc[[i]]
            if self.__model.predict(a)[0] == 1:
                multival = self.__modelo.predict(a)[0]
                if multival == 0:
                    multival = "Analysis"
                elif multival == 1:
                    multival = "Backdoor"
                elif multival == 2:
                    multival = "DoS"
                elif multival == 3:
                    multival = "Exploits"
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
                self.__logWebService(
                    self.__df["port"].iloc[[i]].tolist()[0],
                    multival,
                    fecha,
                    hora,
                    self.__df["source_ip"].iloc[[i]].tolist()[0],
                    cont,
                )
                cont = 2 if cont == 1 else 2
                self.__log(
                    self.__df["port"].iloc[[i]].tolist()[0],
                    multival,
                    fecha,
                    hora,
                    self.__df["source_ip"].iloc[[i]].tolist()[0],
                )
        print("La data ha sido clasificada y respaldada en el servidor...")

    def generateModels(self):
        print("Generando modelos...")
        self.__model = joblib.load(self.__rutaModels + "multiclass.pkl")
        self.__modelo = joblib.load(self.__rutaModels + "modelmulti.pkl")

    def readFile(self):
        print("Leyendo archivos...")
        self.__df = pd.read_csv(self.__rutaSniff + "snif.csv", sep="\s+")
        self.__df.columns = (
            "src_addr",  # 1
            "dst_addr",  # 3
            "dur",  # 7
            "sMeanPktSz",  # 23
            "src_bytes",  # 8
            "ackdat",  # 35
            "src_load",  # 15
            "dst_load",  # 16
            "dMeanPktSz",  # 24
            "dst_port",  # 4
            "src_port",  # 2
            "proto",  # 5
            "state",  # 6
            "dst_bytes",  # 9
            "src_ttl",  # 10
            "dest_ttl",  # 11
            "src_loss",  # 12
            "dest_loss",  # 13
            "src_pkts",  # 17
            "dest_pkts",  # 18
            "src_win",  # 19
            "dest_win",  # 20
            "src_tcp_base",  # 21
            "dest_tcp_base",  # 22
            "src_jit",  # 27
            "dest_jit",  # 28
            "start_time",  # 29
            "last_time",  # 30
            "src_int_pkt",  # 31
            "dest_int_pkt",  # 32
            "tcp_rtt",  # 33
            "synack",  # 34
            "label",  # 49
            # Nuevas
            "is_sm_ips_ports",  # 36
            # "ct_state_ttl",  # 37
            # "ct_flw_http_mthd",  # 38
            # "ct_ftp_cmd",  # 40
            # "ct_srv_src",  # 41
            # "ct_srv_dst",  # 42
            "ct_dst_ltm",  # 43
            "ct_src_ltm",  # 44
            "ct_src_dport_ltm",  # 45
            "ct_dst_sport_ltm",  # 46
            "ct_dst_src_ltm",  # 47
        )
        a = len(self.__df.columns)

        #print("Número de columnas: ", a)
        self.__df.dropna(inplace=True)

        # Cambiar a numerico
        self.__df["src_load"] = pd.to_numeric(self.__df["src_load"])  # 15
        self.__df["dst_load"] = pd.to_numeric(self.__df["dst_load"])  # 16

        # Calculate is_sm_ips_ports
        self.__df["is_sm_ips_ports"] = (
            (self.__df["src_addr"] == self.__df["dst_addr"])
            & (self.__df["src_port"] == self.__df["dst_port"])
        ).astype(
            int
        )  # 36

        # Leer ultimos 100 registros basados en last_time (30)
        self.__df_last = self.__df.sort_values(by="last_time", ascending=False).head(100)

        self.__df["ct_dst_ltm"] = self.__df.apply(
            lambda row: self.__df_last[
                (self.__df_last["dst_addr"] == row["dst_addr"])
            ].shape[0],
            axis=1,
        )  # 43

        self.__df["ct_src_ltm"] = self.__df.apply(
            lambda row: self.__df_last[
                (self.__df_last["src_addr"] == row["src_addr"])
            ].shape[0],
            axis=1,
        )  # 44

        self.__df["ct_src_dport_ltm"] = self.__df.apply(
            lambda row: self.__df_last[
                (self.__df_last["src_addr"] == row["src_addr"])
                & (self.__df_last["dst_port"] == row["dst_port"])
            ].shape[0],
            axis=1,
        )  # 45

        self.__df["ct_dst_sport_ltm"] = self.__df.apply(
            lambda row: self.__df_last[
                (self.__df_last["dst_addr"] == row["dst_addr"])
                & (self.__df_last["src_port"] == row["src_port"])
            ].shape[0],
            axis=1,
        )  # 46

        self.__df["ct_dst_src_ltm"] = self.__df.apply(
            lambda row: self.__df_last[
                (self.__df_last["src_addr"] == row["src_addr"])
                & (self.__df_last["dst_addr"] == row["dst_addr"])
            ].shape[0],
            axis=1,
        )  # 47

        self.__df = self.__df[self.__df.dur != 0]

    def __log(self, port, aType, date, hora, ip):
        logger = logging.getLogger("localhost")
        logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler(self.__rutaLog)
        logger.addHandler(handler)
        if logger.hasHandlers():
            logger.handlers.clear()
        logger.addHandler(handler)
        logger.debug(
            "Port: {} \t Tipo: {} \t Fecha: {} \t Hora: {} \t IP: {}".format(
                port, aType, date, hora, ip
            )
        )

    def __logWebService(self, port, aType, date, hora, ip, mode):
        # mode = 1: cuando es la primera vez que se ejecuta la función
        # mode = 2: cuando no es la primera vez que se ejecuta
        data = []
        data.append({"maquina": self.__maquina})
        dic = {"Port": port, "Tipo": aType, "Fecha": date, "Hora": hora, "IP": ip}
        data.append(dic)
        payload = json.dumps(data)
        headers = {"Content-type": "application/json", "Accept": "text/plain"}
        if mode == 1:
            r = requests.post(url[0], data=payload, headers=headers)
            print(r.text)
        elif mode >= 2:
            r = requests.post(url[1], data=payload, headers=headers)
            print(r.text)
        else:
            pass

    def __generateDate(self):
        now = d.datetime.today()
        fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
        hora = now.strftime("%H:%M:%S")
        return fecha, hora
