from flask import Flask, render_template, jsonify, request
import json
import os
from datetime import datetime


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


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/registrar_inspeccion", methods=["POST"])
def registrar_inspeccion():
    data = request.get_json()

    inspeccion = {
        "fecha": data["fecha"],
        "turno": data["turno"],
        "inspector": data["inspector"],
        "timestamp": datetime.now().isoformat(),
        "condiciones": []
    }

    for c in data["condiciones"]:
        inspeccion["condiciones"].append({
            "nombre": c["nombre"],
            "valor": c["valor"],
            "celulas": c.get("celulas", [])
        })

    inspecciones = cargar_inspecciones()
    inspecciones.append(inspeccion)
    guardar_inspecciones(inspecciones)

    return jsonify({
        "status": "ok",
        "mensaje": "Inspección guardada correctamente"
    })



if __name__ == "__main__":
    app.run(debug=True)
