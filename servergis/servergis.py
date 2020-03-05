###LIBRERIAS DE WEB SERVICES
from wsgiref.simple_server import make_server
from jsonwsp import application
from jsonwsp import Service
## FIN LIBRERIAS WEB SERVICES
import ConfigParser

import psycopg2, psycopg2.extras
import urllib2
import json
from base import base


class baseELIMINAR(object):
    cursor = False
    conn = False
    def __init__(self):
        nameDB = "prueba" #config.get('DB', 'nameDB')
        userDB = "servergis" #config.get('DB', 'userDB')
        passDB = "q1w2e3r4" #config.get('DB', 'passDB')
        hostDB = "localhost" #config.get('DB', 'hostDB')
        try:
            self.conn = psycopg2.connect(dbname=nameDB, user=userDB, password=passDB, host=hostDB)
            self.cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            pass
            print ((e.pgerror))
        if self.cursor:
            print ("conexion correcta")
        else:
            print ("error de conexion")

    def _desconectar(self, cnx):
        cnx.close()

    def Selecciona(self, tabla):
        query1 = """ SELECT "expediente","nombre","titular","mineral","codprov", ST_AsText("geom") FROM public.%s; """
        x = self.cursor.execute(query1 % tabla)
        c = self.cursor.rowcount
        #print ("Numero de Row Seleccionados: ", c)
        results = []
        for row in self.cursor.fetchall():
            results.append({'expediente' : row[0], 'nombre' : row[1], 'titular' : row[2], 'mineral' : row[3], 'codprov' : row[4], 'geom' : row[5]})
        jsresult = json.dumps(results)
        return jsresult

service1 = Service('Servicios Web Gis Mineros','/gisminero')

@service1.params(str)
@service1.rtype(list)
def publica(selec):
    pu = base()
    resp = pu.Selecciona(selec)
    return resp

#@service1.params(list)
@service1.params(int, str, str)
@service1.rtype(bool)
#def reception(lista):
def reception(cod, tabla, lista):
    print (("CODIGO DE PROV..." + str(cod)))
    print (("TABLA ..." + str(tabla)))
    #print (("QUE RECIBO ..." + str(lista)))
    listaTabla = pu.transformaTextoEnLista(lista)
    pu.EliminaDatos(tabla ,cod )
    pu.insertListaToTabla(cod, tabla, listaTabla)
    #listaExtraida = json.loads(lista)
    print (("LISTA  EXTRAIDA ..."))
    #print (("LISTA  EXTRAIDA ..." + str(listaExtraida)))
    #resp = pu.recorreDataWebServiceB(listaExtraida, 'minas', 2)
    #jsresult = json.dumps('hola')
    return True

pu = base()
#config = ConfigParser.ConfigParser()
#config.read('config.ini')
#port = int(config.get('Publicacion', 'port'))
port = 8049

httpd = make_server('0.0.0.0', port, application)
httpd.serve_forever()



