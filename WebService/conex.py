import psycopg2, psycopg2.extras
import urllib2
import json

# Conexion a Base de datos de Nacion Original
conn = psycopg2.connect(database='nacion',user='postgres',password='23462', host='localhost')
cur = conn.cursor()

query = """ UPDATE public.codProv SET como='A' where id='1'; """
cur.execute(query)

# class ConexNacion():
#     conn = True
#     cur = True
#     def Conex(self):
#         print ("CONECTANDO A BASE DE DATOS DE NACION...")
#         self.conn = psycopg2.connect(database='Nacion',user='postgres',password='23462', host='localhost')
#         try:
#             self.cur = self.conn.cursor()
#         except psycopg2.DatabaseError as e:
#             pass
#             print ((e.pgerror))
#         if self.cur:
#             print ("Conexion Correcta a Base de Datos de Nacion")
#             print("--------//----------------//----------------//--------")
#         else:
#             print ("Error de Conexion a Base de Datos de Nacion")
#             print("--------//----------------//----------------//--------")
#         return True
#
#
#
# class ConexBackUp():
#     conn2 = True
#     cur2 = True
#     def ConexBack(self):
#         print ("CONECTANDO A BASE DE DATOS DE BACKUP DE NACION...")
#         self.conn2 = psycopg2.connect(database='BackUpJujuy', user='postgres', password = '23462', host='localhost')
#         try:
#             self.cur2 = self.conn2.cursor()
#         except psycopg2.DatabaseError as e:
#             pass
#             print((e.pgerror))
#         if self.cur2:
#             print("Conexion Correcta a Base de Datos de BackUp")
#             print("--------//----------------//----------------//--------")
#         else:
#             print("Error de Conexion a Base de Datos de BackUp")
#             print("--------//----------------//----------------//--------")
#         return True
#
# # y = ConexBackUp()
# # y.ConexBack()
