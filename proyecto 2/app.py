from flask import Flask, request, jsonify
import json
import os
from datetime import datetime

print(request.form)


app = Flask(__name__)

DATA_PATH = "data/inspecciones.json"


def cargar_inspecciones():
    if not os.path.exists(DATA_PATH):
        return []
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_inspecciones(data):
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


@app.route("/registrar_inspeccion", methods=["POST"])
def registrar_inspeccion():
    inspeccion = {
        "fecha": request.form.get("fecha"),
        "turno": request.form.get("turno"),
        "inspector": request.form.get("inspector"),
        "timestamp": datetime.now().isoformat(),
        "condiciones": []
    }

    # Aquí luego leeremos todas las condiciones
    # (en el siguiente paso)

    inspecciones = cargar_inspecciones()
    inspecciones.append(inspeccion)
    guardar_inspecciones(inspecciones)

    return jsonify({
        "status": "ok",
        "mensaje": "Inspección registrada correctamente"
    })


if __name__ == "__main__":
    app.run(debug=True)
