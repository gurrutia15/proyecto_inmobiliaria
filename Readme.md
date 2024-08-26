consulta_inmuebles.py
consulta_regiones.py
load_inmuebles.py
load_users

==========  INGRESO ARCHIVOS A BD   =========

Para ingresar archivos .json:
    En terminal py manage.py loaddata nombre_archivo


Para ingresar archivos .csv:
- crea carpeta data a nivel de proyecto para que no esté dentro de la app
- crea secuencia de carpetas management/commands ==> carpeta para crear un ejecutable. 
- crea archivo que puede tener cualquier nombre (load_users.py load_inmuebles.py)

    Dentro del archivo:
    Importaciones:

import csv
from django.core.management.base import BaseCommand  ==> indica al proyecto que se va a tratar de un BaseCommand
from .models import Nombre_modelo

- debe crearse la clase Command(BaseCommand) con los argumentos def handle(self, *args, **kwargs): y bajo esto el código

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        archivo = open('data/users.csv', 'r')       #r => significa read (sólo lectura)
        reader = csv.reader(archivo, delimiter=';')
        next(reader) # Se salta la primera linea (son los títulos)
        for fila in reader:
            crear_user(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6])

    ==> filas corresponden a las columnas que vienen en el archivo con su índice para llamar las que interesan y en el orden que se requiera

Ingreso de datos del archivo .csv:
- Para ejecutar en la terminal:
    py manage.py nombre_archivo


----------- QUERYS  ---------------------------------
- Crear querys o consultas para llamar la información
    Debe tener formato standard de los commands:

import csv
from django.core.management.base import BaseCommand
from app_inmobiliaria.models import Comuna
class Command(BaseCommand):
    def handle(self, *args, **kwargs):

Ejecucion del archivo en terminal
    py manage.py nombre_archivo

- para hacer consulta crear una función en services.py

LIBRERIA Q ==> para consultas agrupadas
    debe importarse:
        from django.db.models import Q
        __iconstain  ==> quiere decir que contiene y la i inicial dice acepta minýusculas y mayúsculas

En terminal uso:
    py manage.py nombre_archivo -f dato_a_consultar