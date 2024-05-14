import pandas as pd
import subprocess, sys
import graypy
import sklearn
import socket
import os
import re


# COMANDO_ARGUS = "ubuntu run \"argus -r snif.pcap -w snif.argus && ra -Lo -s  SrcAddr dur smeansz sbytes ackdat sload dload dmeansz Dport, -r snif.argus > casi.csv \""
COMANDO_ARGUS = 'ubuntu run "argus -r snif.pcap -w snif.argus && ra -Lo -s saddr daddr dur smeansz sbytes ackdat sload dload dmeansz dsport SrcAddr sport DstAddr Dport proto state dbytes sttl dttl sloss dloss spkts dpkts swin dwin stcpb dtcpb sjit djit stime ltime sintpkt dintpkt tcprtt synack label, -r snif.argus > casi.csv "'


class Preprocessing:
    def __init__(self):
        self.__comandoArgus = COMANDO_ARGUS

    def callArgus(self):
        print("Corriendo argus...")
        subprocess.call(self.__comandoArgus, shell=True)
        with open("casi.csv", "r") as inputdata:
            df = pd.read_csv(inputdata, sep="\s+")

            df.columns = [re.sub(r"\s+", " ", col) for col in df.columns]
            df.columns = df.columns.str.strip()

            df["is_sm_ips_ports"] = (df["SrcAddr"] == df["DstAddr"]) & (
                df["Sport"] == df["Dport"]
            )
            df["ct_dst_ltm"] = df.groupby("DstAddr")["DstAddr"].transform("count")
            df["ct_src_ltm"] = df.groupby("SrcAddr")["SrcAddr"].transform("count")
            df["ct_src_Dport_ltm"] = df.groupby(["SrcAddr", "Dport"])[
                "SrcAddr"
            ].transform("count")
            df["ct_dst_Sport_ltm"] = df.groupby(["DstAddr", "Sport"])[
                "DstAddr"
            ].transform("count")
            df["ct_dst_src_ltm"] = df.groupby(["SrcAddr", "DstAddr"])[
                "SrcAddr"
            ].transform("count")
            """
            http = 80
            ftp = 21
            smtp = 25, 587, 465
            ssh = 22, 135
            dns = 53
            ftp_data = 20
            irc = 6660-6669 and 7000
            no = '-'

            ports = [20, 21, 22, 25, 53, 80, 135, 465, 587, 6660, 6661, 6662, 6663, 6664, 6665, 6666, 6667, 6668, 6669, 7000,]
            """

            mapp = {
                20: "ftp_data",
                21: "ftp",
                22: "ssh",
                25: "smtp",
                53: "dns",
                80: "http",
                135: "ssh",
                465: "smtp",
                587: "smtp",
                6660: "irc",
                6661: "irc",
                6662: "irc",
                6663: "irc",
                6664: "irc",
                6665: "irc",
                6666: "irc",
                6667: "irc",
                6668: "irc",
                6669: "irc",
                7000: "irc",
                "-": "-",
            }
            df["service"] = df["Sport"].map(mapp)

            with open("casi2.csv", "w+") as middata:
                middata.write(df.to_csv(index=False))
                middata.close()
            with open("casi2.csv", "r") as middata:
                with open("snif.csv", "w+") as outputdata:
                    outputdata.write(middata.read().replace("*", ""))
