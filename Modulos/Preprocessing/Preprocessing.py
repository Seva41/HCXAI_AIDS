import pandas as pd
import subprocess, sys
import graypy
import sklearn
import socket
import os
import re


# COMANDO_ARGUS = "ubuntu run \"argus -r snif.pcap -w snif.argus && ra -Lo -s  SrcAddr dur smeansz sbytes ackdat sload dload dmeansz Dport, -r snif.argus > casi.csv \""
COMANDO_ARGUS = 'ubuntu run "argus -r snif.pcap -w snif.argus && ra -Lo -s saddr daddr dur smeansz sbytes ackdat sload dload dmeansz dport SrcAddr sport DstAddr Dport proto state dbytes sttl dttl sloss dloss spkts dpkts swin dwin stcpb dtcpb sjit djit stime ltime sintpkt dintpkt tcprtt synack label, -r snif.argus > casi.csv "'


class Preprocessing:
    def __init__(self):
        self.__comandoArgus = COMANDO_ARGUS

    def callArgus(self):
        print("Corriendo argus...")
        subprocess.call(self.__comandoArgus, shell=True)
        with open("casi.csv", "r") as inputdata:
            df = pd.read_csv(inputdata, sep="\s+")

            df.columns = [re.sub(r'\s+', ' ', col) for col in df.columns]
            df.columns = df.columns.str.strip()

            df["is_sm_ips_ports"] = (df["SrcAddr"] == df["DstAddr"]) & (df["Sport"] == df["Dport"])
            df["ct_dst_ltm"] = df.groupby("DstAddr")["DstAddr"].transform("count")
            df["ct_src_ltm"] = df.groupby("SrcAddr")["SrcAddr"].transform("count")
            df["ct_src_Dport_ltm"] = df.groupby(["SrcAddr", "Dport"])["SrcAddr"].transform("count")
            df["ct_dst_Sport_ltm"] = df.groupby(["DstAddr", "Sport"])["DstAddr"].transform("count")
            df["ct_dst_src_ltm"] = df.groupby(["SrcAddr", "DstAddr"])["SrcAddr"].transform("count")

            with open("casi2.csv", "w+") as middata:
                middata.write(df.to_csv(index=False))
                middata.close()
            with open("casi2.csv", "r") as middata:
                with open("snif.csv", "w+") as outputdata:
                    outputdata.write(middata.read().replace("*", ""))

