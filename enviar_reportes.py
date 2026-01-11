import os
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime

# -----------------------------
# CONFIGURACIÓN
# -----------------------------

EMAIL_ORIGEN = "reportes.paros.planta@gmail.com"
EMAIL_DESTINO = "dquinteroh@corona.com.co"
EMAIL_PASSWORD = "Parosplanta123*"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

CARPETA_REPORTES = "reportes"

# -----------------------------
# 1. GENERAR REPORTES
# -----------------------------

print("Generando reportes...")
subprocess.run(["python", "leer_paros.py"], check=True)

# -----------------------------
# 2. CREAR CORREO
# -----------------------------

msg = EmailMessage()
fecha_hoy = datetime.now().strftime("%Y-%m-%d")

msg["From"] = EMAIL_ORIGEN
msg["To"] = EMAIL_DESTINO
msg["Subject"] = f"Reporte diario de paros – {fecha_hoy}"

msg.set_content(
    f"""
Buenos días,

Adjunto encontrarás los reportes diarios de paros generados automáticamente.

Fecha del reporte: {fecha_hoy}

Este correo fue generado automáticamente por el sistema de captura de paros.
"""
)

# -----------------------------
# 3. ADJUNTAR CSV
# -----------------------------

for archivo in os.listdir(CARPETA_REPORTES):
    if archivo.endswith(".csv"):
        ruta = os.path.join(CARPETA_REPORTES, archivo)
        with open(ruta, "rb") as f:
            msg.add_attachment(
                f.read(),
                maintype="text",
                subtype="csv",
                filename=archivo
            )

# -----------------------------
# 4. ENVIAR CORREO
# -----------------------------

print("Enviando correo...")

with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
    server.starttls()
    server.login(EMAIL_ORIGEN, EMAIL_PASSWORD)
    server.send_message(msg)

print("Correo enviado correctamente.")
