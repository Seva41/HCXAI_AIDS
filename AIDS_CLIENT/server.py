import datetime as dt
import logging
import socket
import threading
from urllib import request
import requests
import configparser

# local_ipv4 = socket.gethostbyname(socket.gethostname())

config = configparser.ConfigParser()
config.read("config.ini")

RUTA_REGISTRO_ATAQUES = config["ANALYZER"]["RUTA_ATAQUES_PROCESADOS"]
RUTA_DATAINFO = config["SERVER"]["RUTA_DATA_INFO"]
SERVER_LOG = config["SERVER"]["SERVER_LOG"]

# server_address = ("localhost", 5555)
url = [
    f"tcp://localhost:5555",
    f"http://localhost:5555/pushserverdone",
    f"http://localhost:5555/plkpjhbx/",
    f"http://localhost:5555/filaclientes/fila_clientes.txt",
    f"http://localhost:5555/pushplan",
]


def log(componente, func):
    now = dt.datetime.today()
    fecha = str(now.day) + "/" + str(now.month) + "/" + str(now.year)
    hora = now.strftime("%H:%M:%S")

    logger = logging.getLogger("CLI")
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(SERVER_LOG)
    logger.addHandler(handler)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(handler)

    logger.info(
        "Componente: {} \t Funcion: {} \t Fecha: {} \t Hora: {}".format(
            componente, func, fecha, hora
        )
    )


def log2(port, aType, date, hora, ip, veces):
    if veces == 0:
        f = open(RUTA_DATAINFO, "w")
    else:
        f = open(RUTA_DATAINFO, "a")
    f.write(
        "Port: {} \t Tipo: {} \t Fecha: {} \t Hora: {} \t IP: {}\n".format(
            port, aType, date, hora, ip
        )
    )
    f.close()


def writeFile(data):
    cont = 0
    if "" in data:
        data.remove("")

    for d in data:
        l = d.split()
        log2(l[1], l[3], l[5], l[7], l[9], cont)
        cont += 1


def consumirServicio(tipo, url, text="x"):
    try:
        # tipo 1: POST
        # tipo 2: GET
        if tipo == 1:
            payload = text
            headers = {"Content-type": "application/json", "Accept": "text/plain"}
            r = requests.post(url, data=payload, headers=headers)
            return r.text
        elif tipo == 2:
            response = request.urlopen(url)
            return response.read().decode("utf-8").split("\n")
        else:
            return "Error"
    except:
        print("Se cayó el servicio")


def postServer(url, data):
    headers = {"Content-type": "application/json", "Accept": "text/plain"}
    r = requests.post(url, data=data, headers=headers)
    return r.text


def manejar_cliente(client_socket, addr):
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Datos recibidos: {data.decode()}")
            # ...
            client_socket.sendall(b"Datos recibidos correctamente")
        except Exception as e:
            print(f"Error al manejar cliente {addr}: {e}")
            break
    client_socket.close()


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind(server_address)
    server_socket.listen()

    print(f"Servidor escuchando en {server_address}")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Conexión aceptada de {addr}")

        # hilo para manejar al cliente
        client_thread = threading.Thread(
            target=manejar_cliente, args=(client_socket, addr)
        )
        client_thread.start()
