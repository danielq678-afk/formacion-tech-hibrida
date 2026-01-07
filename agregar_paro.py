import json
import os

ARCHIVO_LOG = "paros.json"
ARCHIVO_ENTRADA = "paros_formulario.json"

# 1. Leer evento nuevo
with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
    datos_entrada = json.load(f)

evento_nuevo = datos_entrada["log_paros_celula"][0]

# 2. Asegurar que el log exista
if not os.path.exists(ARCHIVO_LOG):
    datos_log = {"log_paros_celula": []}
else:
    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        datos_log = json.load(f)

        # Protección básica de estructura
        if "log_paros_celula" not in datos_log:
            datos_log = {"log_paros_celula": []}

# 3. Agregar evento
datos_log["log_paros_celula"].append(evento_nuevo)

# 4. Guardar log actualizado
with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
    json.dump(datos_log, f, indent=4, ensure_ascii=False)

print("Evento agregado correctamente. Total eventos:", len(datos_log["log_paros_celula"]))
