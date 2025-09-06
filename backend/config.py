# backend/config.py
import os
from dotenv import load_dotenv
load_dotenv()

MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
MYSQL_PORT = int(os.getenv('MYSQL_PORT', 3306))
MYSQL_USER = os.getenv('MYSQL_USER', 'root')
MYSQL_PASS = os.getenv('MYSQL_PASS', '')
MYSQL_DB   = os.getenv('MYSQL_DB', 'seguridad_facial')

SQLALCHEMY_DATABASE_URI = (
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASS}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    f"?charset=utf8mb4&autocommit=true&connect_timeout=60&read_timeout=60&write_timeout=60"
)

SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
    'pool_timeout': 20,
    'max_overflow': 0,
    'echo': False
}

SECRET_KEY = os.getenv('SECRET_KEY', 'cambiar_esta_clave')

# Fuente de la cámara
CAMERA_SOURCE = os.getenv('CAMERA_SOURCE', '0')  # '0' para webcam por defecto

# Modelo de embeddings faciales
EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'Facenet512')

# Umbral de similitud para reconocer conocidos
SIMILARITY_THRESHOLD = float(os.getenv('SIMILARITY_THRESHOLD', 0.6))

# Email SMTP (para enviar alertas)
SMTP_HOST = os.getenv('SMTP_HOST', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USER = os.getenv('SMTP_USER', 'tu_correo@gmail.com')
SMTP_PASS = os.getenv('SMTP_PASS', 'clave_app')

# Email por defecto si la empresa no tiene configurado uno
ALERT_EMAIL_TO = os.getenv('ALERT_EMAIL_TO', 'alertas@tuapp.com')

# Alias para compatibilidad con detection.py
DEFAULT_ALERT_EMAIL = ALERT_EMAIL_TO
