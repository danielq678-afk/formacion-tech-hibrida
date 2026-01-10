from flask import Flask, request, redirect, url_for
import json
import subprocess
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_FORMULARIO = os.path.join(BASE_DIR, "paros_formulario.json")

@app.route("/")
def index():
    return open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8").read()

@app.route("/registrar_paro", methods=["POST"])
def registrar_paro():
    evento = {
        "celula": int(request.form["celula"]),
        "tipo_evento": request.form["tipo_evento"],
        "causa": request.form["causa"],
        "duracion_minutos": int(request.form["duracion_minutos"]),
        "estado": "cerrado"
    }

    with open(ARCHIVO_FORMULARIO, "w", encoding="utf-8") as f:
        json.dump({"log_paros_celula": [evento]}, f, ensure_ascii=False, indent=2)

    subprocess.run(["python", "agregar_paro.py"], cwd=BASE_DIR)

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
