cd /opt
#INSTALAR EL ENTORNO VIRTUAL
sudo apt-get install virtualenv python-virtualenv
virtualenv ~/.virtualenvs
#ACTIVAR EL entorno virtual antes de instalar las librerias
cd /opt
cd ~/.virtualenvs
source env/bin/activate
#COMENZAR a instalar las librerias en el entorno virtual
python -m pip install timer
python -m pip install logging
python -m pip install datetime
python -m pip install ConfigParser
python -m pip install time
python -m pip install shapely
python -m pip install geos
python -m pip install numpy
python -m pip install setuptools
sudo apt-get install python-dev
python -m pip install psycopg2
python -m pip install geojson
python -m pip install Tkinter
apt-get install python-tk
source env/bin/deactivate
