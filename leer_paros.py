import json

with open("paros.json", "r", encoding="utf-8") as archivo:
    datos = json.load(archivo)

lista_paros = datos["log_paros_celula"]

# Métrica 1: cantidad de paros
total_paros = len(lista_paros)

# Métrica 2: duración total
duracion_total = 0
for paro in lista_paros:
    duracion_total += paro["duracion_minutos"]

print("Total de paros registrados:", total_paros)
print("Duración total del paro:", duracion_total, "minutos")


