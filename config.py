import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DATABASE_FOLDER = BASE_DIR / "database"
UPLOAD_FOLDER = BASE_DIR / "uploads"
SIGNATURE_FOLDER = UPLOAD_FOLDER / "assinaturas"
IMAGE_FOLDER = UPLOAD_FOLDER / "imagens"
REPORTS_FOLDER = BASE_DIR / "reports"
PDF_FOLDER = REPORTS_FOLDER / "pdf"
EXCEL_FOLDER = REPORTS_FOLDER / "excel"

# Ensure folders exist
for folder in (DATABASE_FOLDER, UPLOAD_FOLDER, SIGNATURE_FOLDER, IMAGE_FOLDER, PDF_FOLDER, EXCEL_FOLDER):
    os.makedirs(folder, exist_ok=True)


def env_bool(name, default=False):
    v = os.getenv(name)
    if v is None:
        return bool(default)
    return str(v).lower() in ("1", "true", "yes", "y", "on")


def env_int(name, default):
    try:
        return int(os.getenv(name, default))
    except Exception:
        return default


# Database configuration: prefer DATABASE_URL when provided
DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL:
    db_url = DATABASE_URL
    # some platforms provide the deprecated postgres:// scheme — SQLAlchemy prefers postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = db_url
else:
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FOLDER / 'db.sqlite'}"

SQLALCHEMY_TRACK_MODIFICATIONS = False


# Redis configuration: prefer REDIS_URL, fall back to components
REDIS_URL = os.getenv("REDIS_URL")
if not REDIS_URL:
    redis_host = os.getenv("REDIS_HOST")
    if redis_host:
        redis_password = os.getenv("REDIS_PASSWORD")
        redis_port = os.getenv("REDIS_PORT", "6379")
        if redis_password:
            REDIS_URL = f"redis://:{redis_password}@{redis_host}:{redis_port}/0"
        else:
            REDIS_URL = f"redis://{redis_host}:{redis_port}/0"
REDIS_URL = REDIS_URL or ""


# Network / runtime
PORT = int(os.getenv("PORT", os.getenv("FLASK_RUN_PORT", "8000")))


# Secrets
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
JWT_SECRET = os.getenv("JWT_SECRET", "dev-jwt-secret")


# Uploads and limits
MAX_CONTENT_LENGTH = env_int("MAX_UPLOAD_SIZE", 16 * 1024 * 1024)
ALLOWED_IMAGE_EXTENSIONS = set(ext.strip() for ext in os.getenv("ALLOWED_IMAGE_EXTENSIONS", "jpg,jpeg,png,webp").split(",") if ext.strip())
MAX_IMAGE_SIZE = env_int("MAX_IMAGE_SIZE", 10 * 1024 * 1024)  # 10 MB


# SMTP
SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = env_int("SMTP_PORT", 587)
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = env_bool("SMTP_USE_TLS") or env_bool("SMTP_TLS")


# Monitoring / logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
SENTRY_DSN = os.getenv("SENTRY_DSN", "")

APP_ENV = os.getenv("APP_ENV", "production")
PROMETHEUS_ENABLED = env_bool("PROMETHEUS_ENABLED", False)
