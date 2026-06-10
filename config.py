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

SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_FOLDER / 'db.sqlite'}"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "webp"}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10 MB

SMTP_HOST = os.getenv("SMTP_HOST", "")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587") or 587)
SMTP_USER = os.getenv("SMTP_USER", "")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "")
SMTP_USE_TLS = os.getenv("SMTP_USE_TLS", "True").lower() in ("1", "true", "yes")
