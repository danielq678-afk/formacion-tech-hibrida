from flask import Flask, request, redirect, url_for
import json
import os
import uuid
from datetime import datetime

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_FORMULARIO = os.path.join(BASE_DIR, "paros_formulario.json")
ARCHIVO_HISTORICO = os.path.join(BASE_DIR, "paros.json")

@app.route("/")
def index():
    return open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8").read()

def agregar_evento(evento):
    """Agrega un evento al histórico de paros"""

    evento["id_evento"] = str(uuid.uuid4())
    evento["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if os.path.exists(ARCHIVO_HISTORICO):
        with open(ARCHIVO_HISTORICO, "r", encoding="utf-8") as f:
            data = json.load(f)
            if "log_paros_celula" not in data:
                data = {"log_paros_celula": []}
    else:
        data = {"log_paros_celula": []}

    data["log_paros_celula"].append(evento)

    with open(ARCHIVO_HISTORICO, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(">>> HISTORICO GUARDADO EN:", ARCHIVO_HISTORICO)
    print(">>> TOTAL EVENTOS:", len(data["log_paros_celula"]))

@app.route("/registrar_paro", methods=["POST"])
def registrar_paro():
    evento = {
        "celula": int(request.form["celula"]),
        "tipo_evento": request.form["tipo_evento"],
        "causa": request.form["causa"],
        "duracion_minutos": int(request.form["duracion_minutos"]),
        "estado": "cerrado"
    }

    # Guardar último evento
    with open(ARCHIVO_FORMULARIO, "w", encoding="utf-8") as f:
        json.dump({"log_paros_celula": [evento]}, f, ensure_ascii=False, indent=2)

    # Guardar en histórico (MISMO ARCHIVO, MISMO CONTEXTO)
    agregar_evento(evento)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run()
