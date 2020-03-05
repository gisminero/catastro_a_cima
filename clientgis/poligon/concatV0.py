# -*- coding: utf-8 -*-
from base import base
import logging
import datetime
import os
import psycopg2, psycopg2.extras

da = datetime.date.today().strftime("%Y-%m-%d")
thisfolder = os.path.dirname(os.path.abspath(__file__))
logfile = thisfolder + '/log' + da + '.log'
print (('LOG FILE:' + logfile))

logging.basicConfig(filename = logfile, level=logging.INFO)
dati = datetime.datetime.now().strftime("%Y-%b-%d %H:%M:%S")
logging.info(dati + ' - Inicio de envio  ')

control = base(logging)
    #control = base()
codigoprov = control.codprov
print (("PROVINCIA: ", codigoprov))

##################33CONSULTA NORMAL DE UNION CON IGUAL#################  ;
provincia = control.cursor.execute("""DROP TABLE IF EXISTS minas_temp""")
provincia = control.cursor.execute("""SELECT setval('salta_minas_temp_gid_seq', 0)""")
provincia = control.cursor.execute("""CREATE TABLE minas_temp (
                        gid         integer CONSTRAINT firstkey PRIMARY KEY DEFAULT nextval('salta_minas_temp_gid_seq'),
                        expediente  varchar(254) NOT NULL,
                        nombre      varchar(254),
                        titular     varchar(254),
                        mineral     varchar(254),
                        geom        geography)""")
#############################################################################
provincia = control.cursor.execute("""INSERT INTO minas_temp (expediente, nombre, titular, mineral, geom)
                                    SELECT expediente, descripcio, descripcio, descripcio, geom FROM salta_minas_p2
                                    WHERE salta_minas_p2.expediente <> '';""")
provincia = control.cursor.execute("""INSERT INTO minas_temp (expediente, nombre, titular, mineral, geom)
                                    SELECT expediente, descripcio, descripcio, descripcio, geom FROM salta_minas_p3
                                    WHERE salta_minas_p3.expediente <> '';""")
##################UNION CON EXPTE TRUNCADO BASE : saltaTresFunion #################

control.Desconect()

#A CONTINUACION UN SELECT TOTAL PARA PROBAR
"""
SELECT *
FROM salta_minas_p2
INNER JOIN salta_minas_p3
ON salta_minas_p2.expediente = salta_minas_p3.expediente
INNER JOIN salta_minas_p4
ON salta_minas_p3.expediente = salta_minas_p4.expediente;
"""
