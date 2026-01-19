import os
import subprocess
import smtplib
from email.message import EmailMessage
from datetime import datetime
import sys

# -----------------------------
# CONFIGURACIÓN SMTP OFFICE 365
# -----------------------------

SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587

SMTP_USER = os.getenv("SMTP_USER")        # correo corporativo
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

EMAIL_ORIGEN = SMTP_USER                 # obligatorio en O365
EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

CARPETA_REPORTES = "reportes"

# -----------------------------
# 1. GENERAR REPORTES
# -----------------------------

print("Generando reportes...")
try:
    subprocess.run([sys.executable, "leer_paros.py"], check=True)
except Exception as e:
    print(f"Error generando reportes: {e}")
    sys.exit(1)

# -----------------------------
# 2. CREAR CORREO
# -----------------------------

msg = EmailMessage()
fecha_hoy = datetime.now().strftime("%Y-%m-%d")

msg["From"] = EMAIL_ORIGEN
msg["To"] = EMAIL_DESTINO
msg["Subject"] = f"Reporte diario de paros – {fecha_hoy}"

msg.set_content(
    f"""Buenos días,

Adjunto encontrarás los reportes diarios de paros generados automáticamente.

Fecha del reporte: {fecha_hoy}

Este correo fue generado automáticamente por el sistema de captura de paros.
"""
)

# -----------------------------
# 3. ADJUNTAR CSV
# -----------------------------

try:
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
except Exception as e:
    print(f"Error adjuntando archivos: {e}")
    sys.exit(1)

# -----------------------------
# 4. ENVIAR CORREO
# -----------------------------

print("Enviando correo...")

try:
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=20) as server:
        server.starttls()
        server.login(SMTP_USER, SMTP_PASSWORD)
        server.send_message(msg)

    print("Correo enviado correctamente.")

except Exception as e:
    print(f"Error enviando correo: {e}")
    sys.exit(1)
