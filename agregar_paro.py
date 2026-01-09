import json
import os
import uuid
from datetime import datetime

ARCHIVO_LOG = "paros.json"
ARCHIVO_ENTRADA = "paros_formulario.json"

# 1. Obtener evento de entrada (robusto)
if os.path.exists(ARCHIVO_ENTRADA):
    with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
        datos_entrada = json.load(f)
    evento = datos_entrada["log_paros_celula"][0]
else:
    # Evento mínimo de prueba (fallback consciente)
    evento = {
        "celula": 0,
        "tipo_evento": "sistema",
        "causa": "Inicialización automática",
        "duracion_minutos": 0,
        "estado": "cerrado"
    }

# 2. Identidad del evento
evento["id_evento"] = str(uuid.uuid4())
evento["timestamp"] = datetime.now().isoformat(timespec="seconds")

# 3. Asegurar log
if os.path.exists(ARCHIVO_LOG):
    with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
        datos_log = json.load(f)
        if "log_paros_celula" not in datos_log:
            datos_log = {"log_paros_celula": []}
else:
    datos_log = {"log_paros_celula": []}

# 4. Agregar evento
datos_log["log_paros_celula"].append(evento)

# 5. Guardar
with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
    json.dump(datos_log, f, indent=4, ensure_ascii=False)

print("Evento agregado correctamente. Total eventos:", len(datos_log["log_paros_celula"]))
