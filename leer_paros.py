import json

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
