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

service1 = Service('Servicios Web Gis Mineros','/gisminero')

@service1.params(str)
@service1.rtype(list)
def publica(selec):
    pu = base()
    resp = pu.Selecciona(selec)
    return resp

@service1.params(int, str, str)
@service1.rtype(bool)
def reception(cod, tabla, lista):
    #print (("CODIGO DE PROV..." + str(cod)))
    #print (("TABLA ..." + str(tabla)))
    listaTabla = pu.transformaTextoEnLista(lista)
    pu.EliminaDatos(tabla ,cod )
    pu.insertListaToTabla(cod, tabla, listaTabla)
    #listaExtraida = json.loads(lista)
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



