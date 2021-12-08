# Instrucciones de instalación:
	
## Windows:
- Instalar python 3.7.6 (marcar opción de agregarlo al path)

		https://www.python.org/ftp/python/3.7.6/python-3.7.6-amd64.exe

- Instalar Npcap

		https://nmap.org/npcap/windows-10.html

- Instalar la terminal de linux:

	- Activar el modo desarrollador: Settings> Update & Security > For Developers.
	- Habilitar Windows Subsystem for Linux: Control Panel > Programs > Activar o desactivar las caracteristicas de windows. Marcar opción "Subsistema de Windows para Linux"
	- Descargar terminal de Ubuntu
			
			https://www.microsoft.com/es-cl/p/ubuntu/9nblggh4msv6?activetab=pivot:overviewtab

- Instalar Argus. <i>Nota: se recomienda ejecutar los comandos uno a uno para evitar errores.</i>

	- Abrir terminal Ubuntu instalada en el paso 3
	- Ejecutar los siguientes comandos en la terminal de Ubuntu:

			sudo apt-get install build-essential
			sudo apt install flex
			sudo apt install bison
			sudo apt-get update -y
			sudo apt-get install -y libpcap-dev

	- Instalar argus server con los siguientes comandos:

			wget http://qosient.com/argus/dev/argus-3.0.8.2.tar.gz
			tar zxf argus-3.0.8.2.tar.gz
			cd argus-3.0.8.2
			sudo ./configure
			sudo make
			sudo make install
	- Instalar argus client con los siguientes comandos: 

			wget http://qosient.com/argus/dev/argus-clients-3.0.8.2.tar.gz
			tar zxf argus-clients-3.0.8.2.tar.gz
			cd argus-clients-3.0.8.2
			sudo ./configure
			sudo make
			sudo make install
	- Cerrar terminal Ubuntu
- Instalar bibliotecas de python con pip

	- En caso de no estar instalado pip 
				
			https://pypi.org/project/pip/
	- Ejecutar los siguientes comandos:

			pip install pandas
			pip install scapy
			pip install graypy
			pip install joblib
			pip install sklearn
			pip install xgboost
			pip install numpy==1.19.3

# Instrucciones de uso del módulo AIDS:
## Cliente
### Configuración

Para que el cliente funcione sin problemas es importante modificar el archivo config.ini, ubicada en la carpeta principal del AIDS Client. Deberán modificarse las rutas y el nombre de Cliente de la siguiente manera: Cliente_X donde X es un número (el cual debe ser único, vale decir, que no se repita). De está manera las rutas internas para el funcionamiento de archivos no darán problemas.

### Ejecución
- Abrir una terminal con permisos de administrador.
- Cambiar al directorio AIDS_CLIENT
- Ejecutar cliente.py
	 
	 	python cliente.py

## Server
### Ejecución
- Abrir una terminal con permisos de administrador.
- Cambiar al directorio AIDS_SERVER
- Ejecutar server.py
	 
	 	python server.py

# Funcionalidades módulo AIDS:

- Sensor.py: Analiza la red según un tiempo determinado y genera archivos pcap
- Preprocessing.py: Ejecuta argus y genera archivos .csv y .argus con información de la red
- Monitoring.py: Accede al archivo .csv con data de ataques recientes y los clasifica según su tipo
- Analyzer.py: Analiza los datos generado por Monitoring y los compara según una ventana de tiempo y cantidad de veces presente.

	- Ataque.py: Clase con atributos correspondiente a los ataques generados.

- Planner.py: En base a la información generada por Analyzer genera un plan de mitigación a los ataques detectados.

- Executer.py: Recibe un plan de mitigación desde Planner y ejecuta las acciones solicitadas

	- Actuator.py: Decodifica el plan enviado por el Planer y ejecuta las funciones
	- PortManagement.py: Contiene las funciones ejecutadas por Actuator.
	- Log.py: Modulo para registro de acciones ejecutadas.



# Instrucciones de uso de los scripts:
Estas funciones se encuentran a el directorio Obsoleto.
Se muestran las instrucciones en caso de que se quieran ejecutar, pero no es necesario para el funcionamiento del módulo AIDS

- closePort.py:

	- Windows:

		- Abrir terminal con permisos de administrador
		- Para ejecutar escribir en la terminal: 
		
				python closePort.py [puerto]


- openPort.py
	- Windows:
		- Abrir terminal con permisos de administrador
		- Para ejecutar escribir en la terminal: 
		
				python openPort.py [puerto]


- scannerPort.py
	- Windows:
		- Abrir terminal con permisos de administrador
		- Para ejecutar escribir en la terminal: 
				
				python scannerPort.py [puerto] [IP]

- blockIP.py
	- Windows:
		- Abrir terminal con permisos de administrador
		- Para ejecutar escribir en la terminal:
		
				python blockIP.py [IP]

- responseScript.py
	- Windows:
		- Abrir terminal con permisos de administrador
		- Para ejecutar los scripts se debe seguir el siguiente formato:

				Número [flags separadas por espacio]
				Número [flags separadas por espacio]; Número2 [flags separadas por espacio]

			- número: Número de 1 a 4; Cada script está asociado a un número.
				1. blockIP.py -> 1
				2. closePort.py -> 2
				3. openPort.py -> 3
				4. scannerPort.py -> 4
			- Flags: Seguido del número de script y separadas por un espacio, van las flags de cada archivo.

				- Para ejecutar varios scripts debe separarse por un ; cada linea.

						Ejemplo:
							a) 1 180.160.0.1
							b) 2 443; 4 443 www.google.com; 3 443
			- Threading: para habilitar la ejecución en paralelo se utiliza la flag -m.

					Número [flags separadas por espacio]; -m
					Número [flags separadas por espacio]; -m; Número2 [flags separadas por espacio]
					Ejemplo:
						a) 1 180.160.0.1; 2 443; -m
						b) -m; 2 443; 4 443 www.google.com; 3 443
					Nota: No importa la posición de -m.


# Instrucciones de uso de código orientado a objetos:
	
- main.py:
	- Windows:
			
		- Abrir terminal con permiso de administrador
		- Para ejecutar en la terminar: 
				
				python main.py [puerto/IP] -[flag]
		- Hay 5 flags: -h, -o, -c, -s, -B
			- -h: Muestra ayuda sobre las otras flags. 
			
					python main.py -h
			- -o: Se utiliza para abir un puerto	
			
					python main.py [puerto] -o
			- -c: Se utiliza para cerrar un puerto. 
			
					python main.py [puerto] -c
			- -s: Se utiliza para scanear un puerto 
			
					python main.py [puerto] -s [IP]
			- -B: Se utiliza para bloquear una IP. 
			
					python main.py [IP] -B

# Instrucciones de uso scripts:
## Response.py
- Windows:

	- Abrir terminal con permisos de administrador
	- Para ejecutar los scripts se debe seguir el siguiente formato:
			
			NombreFunción Puerto/IP [flags separadas por espacio]
			NombreFunción Puerto/IP [flags separadas por espacio]; NombreFunción PUERTO2/IP2 [flags separadas por espacio]

		- Puerto/IP: Puerto objetivo o IP objetivo
		- NombreFunción: Seguido del puerto o IP y separadas por un espacio, van las flags de cada funcionalidad.
			Hay 4 funciones
			- OpenPort: Se utiliza para abir un puerto.
			- ClosePort: Se utiliza para cerrar un puerto.
			- ScanPort: Se utiliza para scanear un puerto. 
						
					Ej: Puerto -s IP
			- BlockIp: Se ultiliza para bloquear una IP. 
			- Para ejecutar varias funciones debe separarse por un ; cada linea.

					ClosePort 443
					ScanPort 443 www.google.com; ClosePort 443; OpenPort 500

		- Threading: para habilitar la ejecución en paralelo se utiliza la flag -m seguido de las funciones y sus argumentos entre parentesis () y separados con una ,.
			
			
				-m (NombreFunción Puerto/IP [flags separadas por espacio], NombreFunción2 PUERTO2/IP2 [flags separadas por espacio]); NombreFunción3 PUERTO3/IP3 [flags separadas por espacio]
			<i>Nota: NombreFunción y NombreFunción2 serán ejecutadas en paralelo mientras que NombreFunción3 será ejecutada de manera secuencial.</i>
			Ejemplo:

					ClosePort 443; OpenPort 443
					-m (ClosePort 443, BlockIP 1.1.1.1); OpenPort 400
					-m (ScanPort 443 www.google.com, ClosePort 443, OpenPort 500)
	
## Funcionalidades scripts:

- closePort.py:

	Crea una regla en el Firewall que bloquea las comunicaciones salientes con el puerto dado
- openPort.py
	
	Elimina una regla previamente creada.
- scannerPort.py
	
	Escanea un puerto específico para saber si está abierto o cerrado para cierta dirección IP
- blockIP.py
	
	Bloquea un ip para que no pueda realizar conexiones con el servidor.
- responseScript.py
	
	Ejecuta por comando los scripts señalados en paralelo o secuencialmente.		
- main.py 
	
	Ejecuta las mismas funciones diferenciando por las flags.
- Response.py
	
	Recibe instrucciones para la ejecución de de las fuciones de main.py. Soporta ejecución secuencial y en paralelo.
- LogModule.py:
	
	Genera un archivo log con las funciones ejecutadas.

# Instalacion Web service

## Requerimientos

Para el funcionamiento del Web Service, este debe instalarse en una máquina con <b>Ubuntu 18</b> o superior.

Ejecutar los siguientes comandos con permisos de administrador en la terminal.
 	- apt update
	- apt install nodejs
    - apt install npm
    - npm install nodemon

## Configuración

Una vez esté todo instalado se debe inicializar el proyecto ejecutando el comando <b>npm init</b>. Luego se debe asegurar que la ruta sea la correcta. La cual deben coincidir con los nombres en donde se instaló. en el archivo <b>index.js</b>
```
5	Router.use("/",express.static("../service-MATHIAS/MDCV-WebService"))
```

## Ejecución

Para ejecutar el servicio se debe ir a la carpeta donde se encuentra descargado el repositorio, abrir una terminal e ingresar el siguente comando:
```
	nodemon .
```
De está manera comenzará a ejecutarse y estará listo para ser utilizado por el AIDS Server y Client.
