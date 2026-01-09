import json
import os
print("Leyendo paros.json desde:", os.getcwd())


ARCHIVO_LOG = "paros.json"

# Leer log de paros
with open(ARCHIVO_LOG, "r", encoding="utf-8") as f:
    datos_log = json.load(f)

eventos = datos_log.get("log_paros_celula", [])

print("Total de paros registrados:", len(eventos))

# Mostrar últimos paros (máx 5)
print("\nÚltimos paros:")
for evento in eventos[-5:]:
    print(
        f"- Célula {evento['celula']} | "
        f"{evento['tipo_evento']} | "
        f"{evento['causa']} | "
        f"{evento['duracion_minutos']} min"
    )
# ---- C1: Tiempo total detenido ----

tiempo_total = sum(
    evento["duracion_minutos"]
    for evento in eventos
)

print("\nTiempo total detenido:", tiempo_total, "minutos")

# ---- C2: Tiempo detenido por célula ----

tiempo_por_celula = {}

for evento in eventos:
    celula = evento["celula"]
    tiempo_por_celula[celula] = tiempo_por_celula.get(celula, 0) + evento["duracion_minutos"]

print("\nTiempo detenido por célula:")
for celula, tiempo in sorted(tiempo_por_celula.items()):
    print(f"- Célula {celula}: {tiempo} minutos")

# ---- C3: Tiempo detenido por causa ----

tiempo_por_causa = {}

for evento in eventos:
    causa = evento["causa"]
    tiempo_por_causa[causa] = tiempo_por_causa.get(causa, 0) + evento["duracion_minutos"]

print("\nTiempo detenido por causa:")
for causa, tiempo in sorted(tiempo_por_causa.items(), key=lambda x: x[1], reverse=True):
    print(f"- {causa}: {tiempo} minutos")

# ---- C4: Top 3 causas por tiempo detenido ----

top_n = 3
top_causas = sorted(
    tiempo_por_causa.items(),
    key=lambda x: x[1],
    reverse=True
)[:top_n]

print(f"\nTop {top_n} causas por tiempo detenido:")
for causa, tiempo in top_causas:
    print(f"- {causa}: {tiempo} minutos")

# ---- C5: Exportar resumen por causa a CSV ----

import csv

with open("resumen_por_causa.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["causa", "tiempo_minutos"])
    for causa, tiempo in tiempo_por_causa.items():
        writer.writerow([causa, tiempo])

print("\nArchivo 'resumen_por_causa.csv' generado.")

# ---- C6.1: Número de paros por causa ----

conteo_por_causa = {}

for evento in eventos:
    causa = evento["causa"]
    conteo_por_causa[causa] = conteo_por_causa.get(causa, 0) + 1

print("\nNúmero de paros por causa:")
for causa, cantidad in sorted(conteo_por_causa.items(), key=lambda x: x[1], reverse=True):
    print(f"- {causa}: {cantidad} paros")

# ---- C6.2: Número de paros por célula ----

conteo_por_celula = {}

for evento in eventos:
    celula = evento["celula"]
    conteo_por_celula[celula] = conteo_por_celula.get(celula, 0) + 1

print("\nNúmero de paros por célula:")
for celula, cantidad in sorted(conteo_por_celula.items()):
    print(f"- Célula {celula}: {cantidad} paros")

# =====================================================
# D1 — Exportación estable a CSV
# =====================================================

import csv

# ---- CSV 1: Tiempo total por causa ----

with open("resumen_tiempo_por_causa.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["causa", "tiempo_total_minutos"])
    for causa, tiempo in sorted(tiempo_por_causa.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([causa, tiempo])

print("\nArchivo generado: resumen_tiempo_por_causa.csv")

# ---- CSV 2: Frecuencia de eventos por causa ----

with open("resumen_frecuencia_por_causa.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["causa", "numero_eventos"])
    for causa, cantidad in sorted(conteo_por_causa.items(), key=lambda x: x[1], reverse=True):
        writer.writerow([causa, cantidad])

print("Archivo generado: resumen_frecuencia_por_causa.csv")

