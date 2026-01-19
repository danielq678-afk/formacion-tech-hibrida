import json
import os
from datetime import datetime, timedelta
from collections import defaultdict
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_HISTORICO = os.path.join(BASE_DIR, "paros.json")
CARPETA_REPORTES = os.path.join(BASE_DIR, "reportes")

# -----------------------------
# Utilidades de fechas
# -----------------------------

def semana_actual():
    hoy = datetime.now()
    inicio = hoy - timedelta(days=hoy.weekday())  # lunes
    fin = inicio + timedelta(days=6)               # domingo
    return inicio.date(), fin.date()

def en_semana_actual(timestamp_str, inicio, fin):
    fecha_evento = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S").date()
    return inicio <= fecha_evento <= fin

# -----------------------------
# Cargar histórico
# -----------------------------

if not os.path.exists(ARCHIVO_HISTORICO):
    print("No existe paros.json")
    exit()

with open(ARCHIVO_HISTORICO, "r", encoding="utf-8") as f:
    data = json.load(f)

eventos = data.get("log_paros_celula", [])

if not eventos:
    print("No hay eventos registrados en el histórico.")
    exit()

# -----------------------------
# Filtrar semana actual
# -----------------------------

inicio_semana, fin_semana = semana_actual()

eventos_semana = [
    e for e in eventos
    if e.get("estado") == "cerrado"
    and "timestamp" in e
    and en_semana_actual(e["timestamp"], inicio_semana, fin_semana)
]

if not eventos_semana:
    print("No hay eventos en la semana actual.")
    exit()

# -----------------------------
# Preparar carpeta reportes
# -----------------------------

os.makedirs(CARPETA_REPORTES, exist_ok=True)

rango_semana = f"{inicio_semana}_a_{fin_semana}"

# -----------------------------
# 1️⃣ Impacto por causa
# -----------------------------

tiempo_por_causa = defaultdict(int)
total_tiempo = 0

for e in eventos_semana:
    tiempo_por_causa[e["causa"]] += e["duracion_minutos"]
    total_tiempo += e["duracion_minutos"]

impacto_path = os.path.join(
    CARPETA_REPORTES,
    f"impacto_por_causa_semana_{rango_semana}.csv"
)

with open(impacto_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["causa", "tiempo_total_minutos", "porcentaje_del_total", "ranking_impacto"])

    ranking = sorted(tiempo_por_causa.items(), key=lambda x: x[1], reverse=True)

    for i, (causa, tiempo) in enumerate(ranking, start=1):
        porcentaje = round((tiempo / total_tiempo) * 100, 2)
        writer.writerow([causa, tiempo, porcentaje, i])

# -----------------------------
# 2️⃣ Frecuencia vs impacto
# -----------------------------

frecuencia = defaultdict(int)
tiempo_total = defaultdict(int)

for e in eventos_semana:
    frecuencia[e["]()]()
