import os
from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from PIL import Image
import config
from extensions import db
from models import Checklist


def generate_checklist_pdf(checklist_id):
    checklist = Checklist.query.get(checklist_id)
    if not checklist:
        return None
    pdf_dir = Path(config.PDF_FOLDER)
    pdf_dir.mkdir(parents=True, exist_ok=True)
    filename = f"checklist_{checklist_id}.pdf"
    pdf_path = pdf_dir / filename

    c = canvas.Canvas(str(pdf_path), pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin

    # Header
    c.setFont('Helvetica-Bold', 14)
    c.drawString(margin, y, 'Relatório de Checklist')
    y -= 20
    c.setFont('Helvetica', 10)
    c.drawString(margin, y, f'ID: {checklist.id}    Data: {checklist.data}')
    y -= 15
    c.drawString(margin, y, f'Técnico: {checklist.tecnico}    Equipamento: {checklist.equipamento}    Local: {checklist.local}')
    y -= 25

    # Simple text area for perguntas/respostas
    c.setFont('Helvetica-Bold', 11)
    c.drawString(margin, y, 'Respostas:')
    y -= 18
    c.setFont('Helvetica', 10)
    # Try to fetch perguntas
    try:
        for p in checklist.perguntas:
            if y < 120:
                c.showPage()
                y = height - margin
            c.drawString(margin, y, f'- {p.pergunta} ({p.tipo})')
            y -= 14
    except Exception:
        pass

    # Images
    images_folder = Path(config.UPLOAD_FOLDER) / f'checklist_{checklist_id}'
    if images_folder.exists():
        for img_name in sorted(images_folder.iterdir()):
            if img_name.suffix.lower() not in ('.jpg', '.jpeg', '.png', '.webp'):
                continue
            try:
                img = Image.open(img_name)
                img_w, img_h = img.size
                # scale to fit
                max_w = width - 2*margin
                max_h = (height / 2)
                ratio = min(max_w / img_w, max_h / img_h, 1)
                draw_w = img_w * ratio
                draw_h = img_h * ratio
                if y - draw_h < margin:
                    c.showPage()
                    y = height - margin
                c.drawImage(ImageReader(img), margin, y - draw_h, width=draw_w, height=draw_h)
                y -= (draw_h + 12)
            except Exception:
                continue

    # Signature
    sig_path = Path(config.SIGNATURE_FOLDER) / f'assinatura_{checklist_id}.png'
    if sig_path.exists():
        try:
            sig = Image.open(sig_path)
            sig_w, sig_h = sig.size
            max_w = 200
            ratio = min(max_w / sig_w, 1)
            draw_w = sig_w * ratio
            draw_h = sig_h * ratio
            if y - draw_h < margin:
                c.showPage()
                y = height - margin
            c.drawImage(ImageReader(sig), margin, y - draw_h, width=draw_w, height=draw_h)
            y -= (draw_h + 12)
        except Exception:
            pass

    c.showPage()
    c.save()
    return str(pdf_path)
