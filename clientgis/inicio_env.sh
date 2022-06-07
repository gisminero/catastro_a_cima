#!/bin/bash
echo "Bienvenido!"
#read -p "Introduce el nombre del entorno virtual: " ENV
cd /opt
cd ~/.virtualenvs
source env/bin/activate
#python /opt/api3/clientgis/main.py
python /opt/registro_catastral_minero/clientgis/main.py
