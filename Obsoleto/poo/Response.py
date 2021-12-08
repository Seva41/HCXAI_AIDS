import sys
import subprocess
from threading import Thread
import LogModule

def log(name):
	LogModule.log(name)

def getFlag(name):
	if(name=="ScanPort"):
		return "-s"
	elif(name == "ClosePort"):
		return "-c"
	elif(name == "OpenPort"):
		return "-o"
	elif(name == "BlockIp"):
		return "-B"
	else:
		return "Error"

def exec(name, args):
	flag = getFlag(name)
	if(flag != "Error"):
		try:
			if(flag == "-s"):
				subprocess.call([sys.executable, "main.py", args[0], flag, args[1]])
			else:
				subprocess.call([sys.executable, "main.py", args[0], flag]) #puerto, flags
			log(name)
		except ValueError:
			print("Error de forma.")
		except IndexError:
			print("Opcion equivocada.")
		except:
			print("no se pudo bro.")
		
#comando es un string que representa el comando a ejecutar
#La funcion maneja y le da formato al string y lo divide en una lista 
#para manejarlo y ejecutar los scripts necesarios.
#La entrada es de la sigueinte forma:
#NombreFuncion puerto
def manejarEntrada(string):
	comandos = []
	lista = string.strip().split(";")
	listaComando = []
	aux = []
	aux2 = [] 

	for item in lista:
		if("-m" in item):
			aux = item.strip("() ").split("(")

			for i in aux:
				aux2.append(i.strip().split(","))
			aux.clear()
			aux.append(aux2[0])

			for item in aux2[1:]:
				for i in item:
					aux.append(i.strip().split())
			comandos.append(aux)		
		else:
			listaComando = (item.strip().split())
			comandos.append(listaComando)

	for item in comandos:
		
		if(["-m"] in item):
			try:
				generarThreads(item[1:])
			except:
				pass
		else:
			try:
				exec(item[0], item[1:])
			except:
				pass

def generarThreads(listaComando):
	print("Generar threads:",listaComando)
	for item in listaComando:
		try:
			name = item[0]
			lista = item[1:]
			#print(name, lista)
			Thread(target = exec, args = (name, lista)).start()
		except ValueError:
			("Error de forma.")
		except:
			("Error.")

comando = []
while(1):
	entrada=input() #simular la escucha de informacion desde el planner
	if ("salir" not in entrada):
		manejarEntrada(entrada)
	elif(entrada=="salir"):
		break
	else:
		pass