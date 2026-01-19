import json
import os
import csv
from collections import defaultdict
from datetime import datetime, timedelta

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARCHIVO_HISTORICO = os.path.join(BASE_DIR, "paros.json")
CARPETA_REPORTES = os.path.join(BASE_DIR, "reportes")

os.makedirs(CARPETA_REPORTES, exist_ok=True)

# -----------------------------
# 1. Cargar histórico
# -----------------------------
with open(ARCHIVO_HISTORICO, "r", encoding="utf-8") as f:
    datos = json.load(f)["log_paros_celula"]

if not datos:
    print("No hay datos para procesar")
    exit()

# -----------------------------
# 2. Filtrar última semana
# -----------------------------
fin_semana = datetime.now()
inicio_semana = fin_semana - timedelta(days=7)

def en_semana(ts):
    fecha = datetime.fromisoformat(ts)
    return inicio_semana <= fecha <= fin_semana

eventos = [e for e in datos if en_semana(e["timestamp"])]

if not eventos:
    print("No hay eventos en la última semana")
    exit()

# -----------------------------
# 3. Impacto por causa
# -----------------------------
tiempo_por_causa = defaultdict(int)

for e in eventos:
    tiempo_por_causa[e["causa"]] += e["duracion_minutos"]

total_minutos = sum(tiempo_por_causa.values())

impacto = sorted(tiempo_por_causa.items(), key=lambda x: x[1], reverse=True)

ruta_impacto = os.path.join(
    CARPETA_REPORTES,
    f"impacto_por_causa_semana_{inicio_semana.date()}_a_{fin_semana.date()}.csv"
)

acumulado = 0
with open(ruta_impacto, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "ranking",
        "causa",
        "tiempo_total_minutos",
        "porcentaje_tiempo",
        "porcentaje_acumulado",
        "prioridad"
    ])

    for i, (causa, tiempo) in enumerate(impacto, start=1):
        pct = round(tiempo / total_minutos * 100, 1)
        acumulado = round(acumulado + pct, 1)

        if acumulado <= 80:
            prioridad = "CRÍTICA"
        elif acumulado <= 95:
            prioridad = "ALTA"
        else:
            prioridad = "MEDIA"

        writer.writerow([i, causa, tiempo, pct, acumulado, prioridad])

# -----------------------------
# 4. Frecuencia vs impacto
# -----------------------------
frecuencia = defaultdict(lambda: {"eventos": 0, "tiempo": 0})

for e in eventos:
    frecuencia[e["causa"]]["eventos"] += 1
    frecuencia[e["causa"]]["tiempo"] += e["duracion_minutos"]

ruta_frecuencia = os.path.join(
    CARPETA_REPORTES,
    f"frecuencia_vs_impacto_semana_{inicio_semana.date()}_a_{fin_semana.date()}.csv"
)

with open(ruta_frecuencia, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "causa",
        "cantidad_eventos",
        "tiempo_total_minutos",
        "tiempo_promedio_minutos",
        "porcentaje_tiempo",
        "tipo_problema"
    ])

    for causa, info in frecuencia.items():
        promedio = round(info["tiempo"] / info["eventos"], 1)
        pct = round(info["tiempo"] / total_minutos * 100, 1)

        tipo = "REPETITIVO" if info["eventos"] >= 3 else "EVENTO CRÍTICO"

        writer.writerow([
            causa,
            info["eventos"],
            info["tiempo"],
            promedio,
            pct,
            tipo
        ])

# -----------------------------
# 5. Paros por célula (ordenado + prioridad)
# -----------------------------
celulas = defaultdict(lambda: {
    "paros": 0,
    "tiempo": 0,
    "causas": defaultdict(int)
})

for e in eventos:
    c = e["celula"]
    celulas[c]["paros"] += 1
    celulas[c]["tiempo"] += e["duracion_minutos"]
    celulas[c]["causas"][e["causa"]] += e["duracion_minutos"]

# Construir estructura con porcentaje
resumen_celulas = []

for celula, info in celulas.items():
    pct = round(info["tiempo"] / total_minutos * 100, 1)

    if pct >= 50:
        prioridad = "ALTA"
    elif pct >= 20:
        prioridad = "MEDIA"
    else:
        prioridad = "BAJA"

    causa_principal = max(info["causas"], key=info["causas"].get)

    resumen_celulas.append({
        "celula": celula,
        "cantidad_paros": info["paros"],
        "tiempo_total": info["tiempo"],
        "porcentaje": pct,
        "prioridad": prioridad,
        "causa_principal": causa_principal
    })

# Ordenar por porcentaje descendente
resumen_celulas.sort(key=lambda x: x["porcentaje"], reverse=True)

ruta_celulas = os.path.join(
    CARPETA_REPORTES,
    f"paros_por_celula_semana_{inicio_semana.date()}_a_{fin_semana.date()}.csv"
)

with open(ruta_celulas, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.writer(f, delimiter=";")
    writer.writerow([
        "celula",
        "cantidad_paros",
        "tiempo_total_minutos",
        "porcentaje_tiempo",
        "prioridad",
        "causa_principal"
    ])

    for r in resumen_celulas:
        writer.writerow([
            r["celula"],
            r["cantidad_paros"],
            r["tiempo_total"],
            r["porcentaje"],
            r["prioridad"],
            r["causa_principal"]
        ])
