import os
import base64
from pathlib import Path
from werkzeug.utils import secure_filename
import config
from extensions import db
from models import Imagem


ALLOWED_EXT = config.ALLOWED_IMAGE_EXTENSIONS


def allowed_file(filename):
    if not filename:
        return False
    ext = filename.rsplit('.', 1)[-1].lower()
    return ext in ALLOWED_EXT


def _check_size(content_bytes):
    return len(content_bytes) <= config.MAX_IMAGE_SIZE


def save_images(files, checklist_id):
    saved = []
    dest = Path(config.UPLOAD_FOLDER) / f"checklist_{checklist_id}"
    dest.mkdir(parents=True, exist_ok=True)
    for f in files:
        if not f:
            continue
        filename = secure_filename(f.filename)
        if not allowed_file(filename):
            continue
        data = f.read()
        if not _check_size(data):
            continue
        path = dest / filename
        with open(path, 'wb') as out:
            out.write(data)
        saved.append(str(path))
        try:
            # create DB record for image
            img = Imagem(checklist_id=checklist_id, arquivo=str(path))
            db.session.add(img)
            db.session.commit()
        except Exception:
            # avoid failing on DB errors during file save
            db.session.rollback()
    return saved


def save_signature(data_url, checklist_id):
    # data_url should be like 'data:image/png;base64,...'
    if not data_url or ',' not in data_url:
        return None
    header, b64 = data_url.split(',', 1)
    ext = 'png'
    if 'image/' in header:
        ext = header.split('image/')[1].split(';')[0]
    data = base64.b64decode(b64)
    if not _check_size(data):
        return None
    dest = Path(config.SIGNATURE_FOLDER)
    dest.mkdir(parents=True, exist_ok=True)
    filename = f"assinatura_{checklist_id}.png"
    path = dest / filename
    with open(path, 'wb') as f:
        f.write(data)
    return str(path)
