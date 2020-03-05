# -*- coding: utf-8 -*-
#from ssh.catssh import catssh
#from base import base
from timer import InfiniteTimer
import os
import time

import psycopg2, psycopg2.extras
import ConfigParser
import logging
#import datetime
#from poligon.concat import concat
from datetime import datetime as dt
from datetime import timedelta


def delLogs():
    days_to_subtract = 10
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    i = 0
    listaQueda = []
    while i < days_to_subtract:
        da = dt.today() - timedelta(days=i)
        logfile = thisfolder + '/log/client' + da.strftime("%Y-%m-%d") + '.log'
        listaQueda.append(logfile)
        i += 1
    ########################3
    thisfolder = os.path.dirname(os.path.abspath(__file__))
    cant = 0
    for file in os.listdir(thisfolder + '/log'):
        if file.endswith(".log"):
            cant = cant + 1
            fileovpn = os.path.join(thisfolder + '/log', file)
            if fileovpn in listaQueda:
                print(("NO BORRAR: "+fileovpn))
            else:
                os.remove(fileovpn)
                print (('BORRANDO!: '+fileovpn))
    return True

delLogs()

da = dt.today().strftime("%Y-%m-%d")
thisfolder = os.path.dirname(os.path.abspath(__file__))
logfile = thisfolder + '/log/client' + da + '.log'
print (('LOG FILE:' + logfile))

def tick():
    actualTime = dt.now().strftime("%H:%M")
    if actualTime != horaEnvio:
        print (("NOOOO ES LA MISMA " + actualTime + " = "+ horaEnvio))
        return
    #INICIO DE CONCATENACION DE DATOS
    os.system('reboot')


thisfolder = os.path.dirname(os.path.abspath(__file__))
initfile = os.path.join(thisfolder, 'config.ini')


configMain = ConfigParser.ConfigParser()
configMain.read(initfile)

horaEnvio = configMain.get('Publicacion', 'horaReinicio')



tiempo = 60
t = InfiniteTimer(tiempo, tick)
t.start()

#tick()