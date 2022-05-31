#!/bin/bash
echo "Bienvenido!"
#read -p "Introduce el nombre del entorno virtual: " ENV
cd /opt
cd ~/.virtualenvs
source env/bin/activate
python /opt/clientgis/main.py
