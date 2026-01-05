import json
import os

ruta_base = os.path.dirname(__file__)
ruta_json = os.path.join(ruta_base, "paros.json")

with open(ruta_json, "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

print(datos)
