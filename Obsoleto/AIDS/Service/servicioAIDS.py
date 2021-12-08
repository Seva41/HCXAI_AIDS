import win32serviceutil
import win32service
import win32event
import servicemanager
import socket
import time as t
import datetime as dt
import logging
import sys, subprocess
logging.basicConfig(filename="C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\log_service.log", level=logging.DEBUG)

class ServicioAIDS(win32serviceutil.ServiceFramework):
    _svc_name_ = "AIDS-service"
    _svc_display_name_ = "Servicio Sensor AIDS"
    _svc_description_ = "Servicio para el funcionamiento del AIDS. Ejecuta el Sensor según un tiempo determinado."

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.waitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcDoRun(self):
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.waitStop)

    def main(self):
        time = 120 #segundos
        self.log("AIDS iniciado.")
        while True:
            self.log("Llamando Sensor.")
            #subprocess.call([sys.executable, "C:\\Users\\mcabr\\Desktop\\PT\\AIDS\\AIDS\\Sensor\\Sensor.py"], shell=True)
            subprocess.call([sys.executable, "..\AIDS\Sensor\Sensor.py"])
            #subprocess.call('start /wait python C:\\Users\mcabr\Desktop\PT\AIDS\AIDS\Sensor\Sensor.py')
            self.log("Sensor Ejecutado.")
            self.log("Esperando... TIEMPO: {}".format(time))
            t.sleep(time)

    def log(self, text):
        now = dt.datetime.today()
        fecha = str(now.day)+"/"+str(now.month)+"/"+str(now.year)
        hora = now.strftime("%H:%M:%S")
        logging.info("{} \tFecha: {} Hora: {}".format(text, fecha, hora))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        servicemanager.Initialize()
        servicemanager.PrepareToHostSingle(ServicioAIDS)
        servicemanager.StartServiceCtrlDispatcher()
    else:
        win32serviceutil.HandleCommandLine(ServicioAIDS)