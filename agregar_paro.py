print(">>> SCRIPT EJECUTADO <<<")

import json

# 1. Leer evento nuevo desde formulario
with open("paros_formulario.json", "r", encoding="utf-8") as archivo_formulario:
    datos_formulario = json.load(archivo_formulario)

evento_nuevo = datos_formulario["log_paros_celula"][0]

# 2. Leer log existente
with open("paros.json", "r", encoding="utf-8") as archivo_log:
    datos_log = json.load(archivo_log)

# 3. Agregar evento al log
datos_log["log_paros_celula"].append(evento_nuevo)

# 4. Guardar log actualizado
with open("paros.json", "w", encoding="utf-8") as archivo_log:
    json.dump(datos_log, archivo_log, indent=4, ensure_ascii=False)

print("Evento agregado correctamente al log.")
