# -*- coding: utf-8 -*-
from base import base
from timer import InfiniteTimer

from controladores import casos_prov
import psycopg2, psycopg2.extras

#conexion = psycopg2.connect(dbname='nacion',user='postgres',password='23462', host='localhost')
#cursor = conexion.cursor()
#if cursor:
    #print "Conexion correcta"
    #pass

############### Inicio Funcion CASOS ###############
def get_prov_activas(cursor1):
    print (("OBTENIENDO PROV ACTIVAS"))
    cursor1.execute(""" SELECT * FROM public.codprov WHERE activo=true""")
    prov_act = cursor1.fetchall()
    return prov_act

def tick():
    print (("ENTRANDO A TIK"))
    control = casos_prov()
    prov_activas = get_prov_activas(control.cursor)
    for xy in prov_activas:
        if xy[3] == 'A':
            print "Caso: ", xy[2],xy[3]
            #from casoA import *
            codigoprov = xy[1]
            print (("PROVINCIA: ", xy[0], xy[2], xy[3]))
            provincia = control.cursor.execute(""" SELECT * FROM public.codprov_conex WHERE
            activo=true AND codigoprov=%s """ % codigoprov)
            prov_conex = control.cursor.fetchall()
            for info_conex in prov_conex:
                control.control_caso_a(info_conex[2], info_conex[3], info_conex[1])
            #casos = casos_prov()
            pass
        elif xy[3] == 'B':
            print "caso B: ", xy[3]
            codigoprov = xy[1]
            print (("PROVINCIA CASO B: ", xy[0], xy[2], xy[3]))
            provincia = control.cursor.execute(""" SELECT * FROM public.codprov_conex WHERE
            activo=true AND codigoprov=%s """ % codigoprov)
            prov_conex = control.cursor.fetchall()
            for info_conex in prov_conex:
                control.control_caso_b(info_conex[2], info_conex[3], info_conex[1])
            pass
        pass
    control.Desconect()
    del control


#def tick():
    #print('Llamando a main')
    #os.system('python main.py')

# Tiempo en segundos, actualmente 2 minutos (120 segundos)
# 43200 seg son 12 horas
t = InfiniteTimer(120, tick)
t.start()
#tick()
