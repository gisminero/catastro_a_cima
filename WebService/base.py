#PRECONDICIONES DE INSTALACION EN EL SO
#$ pip install numpy
#$ pip install geos
#Shapely pide instalar geos
#$ pip install shapely
#FIN PRECONDICIONES

import psycopg2, psycopg2.extras
import urllib2
import json
import re
# import timer
#import numpy as np
import geojson
from shapely.geometry import shape
from json import dumps
# from main import *


from jsonwsp.client import ServiceConnection
# Conexion a Base de datos de Nacion Original
#conn = psycopg2.connect(database='Nacion',user='postgres',password='123456', host='localhost')




## EliminaDatos()
## Selecciona()
class base(object):
    cursor = False
    conn = False
    def __init__(self):
        print ("CONECTANDO/--....")
        self.conn = psycopg2.connect(dbname='datarecep', user='postgres', password='qwer1234', host='localhost')
        #self.conn = psycopg2.connect(dbname='nacion',user='postgres',password='23462', host='192.168.159.1')
        try:
            self.cursor = self.conn.cursor()
        except psycopg2.DatabaseError as e:
            pass
            print ((e.pgerror))
        if self.cursor:
            print ("conexion correcta")
        else:
            print ("error de conexion")
        #return self

    def _desconectar(self, cnx):
        cnx.close()

    def insert_multipolig(self, wkt, mutipoligon):
        print (("HOLA: "+str(wkt)))
        #self._conectar()
        try:
            self.cursor.execute("""insert into MultiPolygon_Sample(geom, polig_text) VALUES ( ST_GeogFromText('%s') , '%s')""" % (str(wkt), mutipoligon))
        except psycopg2.Error as e:
            pass
            print ((e.pgerror))
        self.conn.commit()
        self.conn.close()

    def getDataWebService(self, url_ws):
        req = urllib2.Request(url_ws)
        opener = urllib2.build_opener()
        f = opener.open(req)
        json_local = json.loads(f.read())
        return json_local

    #Convierte la informacion de Multipoligono mediante Json en formato WKT,
    # en un tipo Geografico apto para ser guardado en PostGis (Tipo geographics)
    def _convMultiGeog(self, cordenadas_multipo):
        #NUEVA LIBRERIA
        # https://pypi.org/project/Shapely/1.4.0/
        s = dumps(cordenadas_multipo)
        # Convert to geojson.geometry.Polygon
        #https://pypi.org/project/geojson/
        g1 = geojson.loads(s)
        # Feed to shape() to convert to shapely.geometry.polygon.Polygon
        # This will invoke its __geo_interface__ (https://gist.github.com/sgillies/2217756)
        #http://toblerity.org/shapely/manual.html#polygons
        g2 = shape(g1)
        # Now it's very easy to get a WKT/WKB representation
        return g2.wkt
        #g2.wkb
        #FIN NUEVA LIBRERIA

    # Elimina datos de la tabla Cateos de BackUp
    def EliminaDatos(self, tabla, cod_prov):
        try:
            queryDelete = """ DELETE FROM  """ + tabla + """ WHERE codprov = %s """
            self.cursor.execute(queryDelete % cod_prov)
            self.conn.commit()
            rows_deleted = self.cursor.rowcount
            print "Se eliminaron ", rows_deleted, " registros de la Base de la tabla: "+tabla
        except Exception as e:
            raise

    def bucleEliminaDatos(self):
        self.EliminaDatos('canteras', 1)
        self.EliminaDatos('cateos', 1)
        self.EliminaDatos('manifestaciones', 1)
        self.EliminaDatos('minas', 1)
        self.EliminaDatos('vacantes', 1)
        self.EliminaDatos('servidumbres', 1)
        self.EliminaDatos('manifestaciones', 1)
        return True

    def creaDiccTabla(self):
        #15-05-2019: Esta funcion tiene que crear un diccionario estatico para traducir el contenido
        #del campo rg_tipo obtenido por la publicacion WFS de Jujuy, con el fin de
        #traducir a que tabla corresponde.
        diccTablaJujuy = {'AREA DE RESERVA' : '', 'CANTERA' : 'canteras',
            'CANTERA1' : 'canteras', 'CATEO': 'cateos', 'CATEO1' : 'cateos',
            'SOLICITUD DE MINA' : 'manifestaciones', 'SOLICITUD DE MINA1' : 'manifestaciones',
            'MINA CONCEDIDA' : 'minas', 'GRUPO MINERO' : '',
            'MINA VACANTE PUBLICADA' : 'vacantes', 'SERVIDUMBRE' : 'servidumbres'}
        return diccTablaJujuy

# Inserta los registros traidos del WebService de la provincia de Jujuy
    def InsertCateos(self, tabla, json_local):
        #print(("INSERTANDO DATOS DE CANTERAS"))
        # Recorre el JSON segun el totalFeatures almacena en variables e inserta en tabla Cateos
        diccTabla = self.creaDiccTabla()
        for i in range(0,int(json_local['totalFeatures'])):
            expediente = json_local['features'][i]['properties']['expediente']
            nombre = json_local['features'][i]['properties']['nombre']
            titular = json_local['features'][i]['properties']['titular_ac']
            mineral = json_local['features'][i]['properties']['tipo_miner']
            estado = json_local['features'][i]['properties']['estado']
            tipo = json_local['features'][i]['properties']['rg_tipo']
            #A continuacion obtener la parte del Json que contiene el poligono
            #tipo de poligono y puntos en formato WKT
            cordenadas_multipo = json_local['features'][i]['geometry']
            #Solicitar conversion
            poligGeo = self._convMultiGeog(cordenadas_multipo)
            codProv = "1"
            tabla = diccTabla[tipo]
            if tabla != '':
                print (("CARGANDO EXPTE " +expediente + " TIPO ORIGINAL: "+ tipo+ " TIPO TRANSFORMADO: " +tabla))
                query = """ INSERT INTO public."""+tabla+""" ("geom", "expediente", "nombre", "titular", "mineral", "codprov", "estado_legal")
                        VALUES(ST_GeogFromText(%s),%s,%s,%s,%s,%s,%s); """
                data = (str(poligGeo), expediente,nombre,titular,mineral,codProv, estado)
                self.cursor.execute(query,data)
                self.conn.commit()
        query1 = """ SELECT "expediente", "nombre", "titular", "mineral", "codprov" FROM public."""+tabla+"""; """
        self.cursor.execute(query1)
        row = self.cursor.rowcount
        print "Se Insertaron", row ," registros nuevos en la tabla "+tabla+" ..."
        return True

        ########CLIENTE WEB SERVICE -- CASO "B" ################
#####################################################
    def insertDataClientB(self, tabla, wkt, expte, nombre, titular, mineral, codprov, estado_legal):
        try:
            self.cursor.execute("""INSERT INTO %s (geom, expediente, nombre, titular, mineral, codprov, estado_legal) VALUES ( ST_GeogFromText('%s') , '%s', '%s', '%s', '%s', '%s', '%s')""" % (tabla, str(wkt), expte, nombre, titular, mineral, codprov, estado_legal))
        except psycopg2.Error as e:
            pass
            print ((e.pgerror))
        self.conn.commit()
        #self.conn.close()

    def getDataWebServiceB(self, url_ws, table):
        connection = ServiceConnection(url_ws, 8049, '/gisminero')
        connection.initialize()
        servicio = connection.get_method('publica')
        r = servicio(table)
        #print (str(json.loads(r)))
        return r

    def recorreDataWebServiceB(self, json_local, tabla, cod_prov):
        # Recorre el JSON segun el totalFeatures almacena en variables e inserta en tabla Cateos
        #pu = base()
        for dato in json_local:
            #print (( 'Insert Expte.:' + str(dato['expediente'])))
            resp = self.insertDataClientB( tabla, dato['geom'], dato['expediente'], dato['nombre'], dato['titular'], dato['mineral'], cod_prov)
            #expediente = json_local['features'][i]['properties']['expediente']
        #self.desconectar()

    # Selecciona de la Base de Datos de Nacion e Inserta  la Base de Datos de BackUp
    def Save(self):
        x = self.Selecciona()
        print (("INSERTANDO CATEOR DARIO"))
        for value in x:
            query = """ INSERT INTO public.vacantes("expediente", "nombre", "titular", "mineral", "codprov") VALUES(%s,%s,%s,%s,%s); """
            data = (value['expediente'],value['nombre'],value['titular'],value['mineral'],value['codprov'])
            self.cursor.execute(query,data)
            pass
        pass
    # Inserta y Desconecta de la Base de Datos de BackUp

    def Selecciona(self):
        query1 = """ SELECT "expediente","nombre","titular","mineral","codprov" FROM public.vacantes; """
        x = self.cursor.execute(query1)
        c = self.cursor.rowcount
        print ("Numero de Row Seleccionados: ", c)
        row = self.cursor.fetchone()
        columns = [column[0] for column in cur.description]
        results = []
        for row in self.cursor.fetchall():
            results.append(dict(zip(columns, row)))
        return results

    def Desconect(self):
        self.conn.commit()
        self.conn.close()
        pass



# base()






#EJEMPLO:
#http://www.codedirection.com/convert-multipolygon-geometry/
# multipolig_string : Es una variable que sirve para cargar el multipoligono en formato WKT, ver:
#http://www.postgis.net/docs/PostGIS_Special_Functions_Index.html
