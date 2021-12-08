import sys
import subprocess
import time as t 
from threading import Thread
import LogModule

FILES=["blockIP.py", "closePort.py", "openPort.py", "scannerPort.py"]

def exec(scriptNumber, args):
	try:
		if(scriptNumber == 1) or (scriptNumber == 2) or (scriptNumber == 3):
			subprocess.call([sys.executable, FILES[scriptNumber-1], args[0]])
			LogModule.log(FILES[scriptNumber-1])
		elif(scriptNumber == 4):
			subprocess.call([sys.executable, FILES[scriptNumber-1], args[0], args[1]])
			LogModule.log(FILES[scriptNumber-1])
		else:
			pass		
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
#idScript arg1 arg2 arg3; idScript arg1 arg2 arg3; id script arg1
def manejarIngreso(comando):
	listaComando=[]
	for item in comando:
		listaComando.append(item.strip().split())

	#Si comando viene con la flag -m se habilita la ejecución
	#en paralelo. Sino se ejecuta de manera secuencial
	if True in ["-m" in i for i in listaComando]:
		listaComando.remove(["-m"])
		generarThreads(listaComando)
	else:
		for item in listaComando:
			try:
				scriptNumber = int(item[0])
				exec(scriptNumber, item[1:])
			except ValueError:
				("Error de forma.")
			except:
				("Error.")

def generarThreads(listaComando):
	for item in listaComando:
		scriptNumber = int(item[0])
		lista = item[1:]
		Thread(target = exec, args = (scriptNumber, lista)).start()

#main
comando = []
while(1):
	entrada=input() #simular la escucha de informacion desde el planner
	if ("salir" not in entrada):
		comando = entrada.split(";")
		manejarIngreso(comando)
	elif(entrada=="salir"):
		break
	else:
		pass
