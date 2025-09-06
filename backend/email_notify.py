import smtplib
import ssl
import cv2
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from config import SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASS
from datetime import datetime

def send_alert_email(to_email: str, empresa_nombre: str, camera_name: str, face_image=None):
    """
    Envía alerta de persona desconocida detectada
    """
    if not to_email:
        print("[EMAIL] No se envió porque no hay destinatario configurado")
        return

    subject = f"🚨 ALERTA DE SEGURIDAD - {empresa_nombre}"
    
    body = f"""
    SISTEMA DE DETECCIÓN FACIAL - ALERTA DE SEGURIDAD
    
    Se ha detectado una PERSONA DESCONOCIDA en las instalaciones de {empresa_nombre}.
    
    Detalles del evento:
    • Fecha y hora: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
    • Cámara: {camera_name}
    • Estado: PERSONA NO REGISTRADA EN EL SISTEMA
    
    Por favor, revise el sistema de seguridad y tome las medidas necesarias.
    
    ---
    Sistema Automático de Detección Facial
    {empresa_nombre}
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if face_image is not None:
        try:
            # Convertir imagen a bytes
            ret, buffer = cv2.imencode('.jpg', face_image)
            if ret:
                part = MIMEBase("application", "octet-stream")
                part.set_payload(buffer.tobytes())
                encoders.encode_base64(part)
                part.add_header(
                    "Content-Disposition", 
                    f"attachment; filename=persona_desconocida_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                )
                msg.attach(part)
        except Exception as e:
            print(f"[EMAIL] Error adjuntando imagen: {e}")

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls(context=ssl.create_default_context())
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"[EMAIL] Alerta enviada a {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] {e}")
        return False

def send_welcome_email(to_email: str, empresa_nombre: str, password: str):
    """
    Envía email de bienvenida al registrar nueva empresa
    """
    subject = f"Bienvenido al Sistema de Detección Facial - {empresa_nombre}"
    
    body = f"""
    ¡Bienvenido al Sistema de Detección Facial!
    
    Su cuenta ha sido creada exitosamente:
    
    Empresa: {empresa_nombre}
    Email: {to_email}
    Contraseña temporal: {password}
    
    Por favor, cambie su contraseña después del primer inicio de sesión.
    
    Puede acceder al sistema en: http://localhost:5000
    
    ---
    Sistema de Detección Facial
    """

    msg = MIMEMultipart()
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP(SMTP_HOST, SMTP_PORT)
        server.starttls(context=ssl.create_default_context())
        server.login(SMTP_USER, SMTP_PASS)
        server.sendmail(SMTP_USER, to_email, msg.as_string())
        server.quit()
        print(f"[EMAIL] Email de bienvenida enviado a {to_email}")
        return True
    except Exception as e:
        print(f"[EMAIL ERROR] Error enviando bienvenida: {e}")
        return False
