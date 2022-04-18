# -*- coding: utf-8 -*-



from base import *

class casos_prov(base):
    def __init__(self):
        super(casos_prov, self).__init__()
    # conexion a base de datos BackUp
        print (("creando ABM Cateos"))

    def control_caso_a(self, link, procedimiento, cod_prov):
        #print ((procedimiento.upper()))
        #print(("DETALLE: ", link, procedimiento))
        self.EliminaDatos(procedimiento, cod_prov)
        jsl = self.getDataWebService(link)
        if jsl is False:
            return False
            pass
        else:
            self.InsertCateos(procedimiento, jsl)


    def control_caso_b(self, link, tablaActualiza, cod_prov):
        re = self.getDataWebServiceB(link, tablaActualiza)
        os = json.loads(re)
        self.recorreDataWebServiceB(os, tablaActualiza, cod_prov)
