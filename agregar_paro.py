import json
import os
import uuid
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_LOG = os.path.join(BASE_DIR, "paros.json")

def agregar_evento(evento):
    """
    Agrega un evento al histórico de paros de forma robusta.
    """

    # 1. Identidad del evento
    evento["id_evento"] = str(uuid.uuid4())
    evento["timestamp"] = datetime.now().isoformat(timespec="seconds")

    # 2. Asegurar log
    if os.path.exists(ARCHIVO_LOG):
        with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
            datos_log = json.load(f)
            if "log_paros_celula" not in datos_log:
                datos_log = {"log_paros_celula": []}
    else:
        datos_log = {"log_paros_celula": []}

    # 3. Agregar evento
    datos_log["log_paros_celula"].append(evento)

    # 4. Guardar
    print(">>> ESCRIBIENDO HISTORICO EN:")
    print(ARCHIVO_LOG)
    with open(ARCHIVO_LOG, "w", encoding="utf-8") as f:
        json.dump(datos_log, f, indent=4, ensure_ascii=False)

    return len(datos_log["log_paros_celula"])


# 👉 Permite seguir usándolo como script (opcional)
if __name__ == "__main__":
    ARCHIVO_ENTRADA = os.path.join(BASE_DIR, "paros_formulario.json")

    if os.path.exists(ARCHIVO_ENTRADA):
        with open(ARCHIVO_ENTRADA, "r", encoding="utf-8") as f:
            datos_entrada = json.load(f)
        evento = datos_entrada["log_paros_celula"][0]
    else:
        evento = {
            "celula": 0,
            "tipo_evento": "sistema",
            "causa": "Inicialización automática",
            "duracion_minutos": 0,
            "estado": "cerrado"
        }

    total = agregar_evento(evento)
    print("Evento agregado correctamente. Total eventos:", total)
