import json
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, current_app, send_file, send_from_directory
from extensions import db
from models import Checklist, Pergunta, Resposta, Assinatura, EnviosEmail
from services.upload_service import save_images, save_signature
from services.pdf_service import generate_checklist_pdf
from services.email_service import send_email_with_attachment
from services.excel_service import export_checklists_excel
from utils.auth_utils import login_required, current_user
import config

checklist_bp = Blueprint('checklist', __name__, url_prefix='/checklists', template_folder='../templates')


@checklist_bp.route('/dashboard')
@login_required
def dashboard():
    perfil = session.get('user_perfil')
    if perfil == 'administrador':
        checks = Checklist.query.order_by(Checklist.data.desc()).all()
    else:
        # Para scaffolding, mostramos todos
        checks = Checklist.query.order_by(Checklist.data.desc()).all()
    return render_template('dashboard.html', checklists=checks)


@checklist_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_checklist():
    if request.method == 'POST':
        equipamento = request.form.get('equipamento')
        local = request.form.get('local')
        tecnico = session.get('user_nome') or request.form.get('tecnico')
        latitude = request.form.get('latitude')
        longitude = request.form.get('longitude')
        checklist = Checklist(equipamento=equipamento, local=local, tecnico=tecnico)
        if latitude:
            try:
                checklist.latitude = float(latitude)
            except Exception:
                pass
        if longitude:
            try:
                checklist.longitude = float(longitude)
            except Exception:
                pass
        db.session.add(checklist)
        db.session.commit()

        # Perguntas/Respostas via JSON
        questions_json = request.form.get('questions')
        if questions_json:
            try:
                questions = json.loads(questions_json)
                for q in questions:
                    p = Pergunta(checklist_id=checklist.id, pergunta=q.get('pergunta'), tipo=q.get('tipo'))
                    db.session.add(p)
                    db.session.flush()
                    r = Resposta(pergunta_id=p.id, resposta=q.get('resposta'))
                    db.session.add(r)
            except Exception as e:
                current_app.logger.exception(e)

        # Imagens
        images = request.files.getlist('images')
        save_images(images, checklist.id)

        # Assinatura
        signature_data = request.form.get('signature_data')
        if signature_data:
            sig_path = save_signature(signature_data, checklist.id)
            assinatura = Assinatura(checklist_id=checklist.id, arquivo=str(sig_path))
            db.session.add(assinatura)

        db.session.commit()

        # Gerar PDF
        pdf_path = generate_checklist_pdf(checklist.id)

        # Enviar e-mail opcional
        send_to = request.form.get('send_to')
        if send_to:
            recipients = [e.strip() for e in send_to.split(',') if e.strip()]
            subject = f"Checklist Concluído - {checklist.equipamento} - {checklist.data.date()}"
            body = f"Segue em anexo o relatório do checklist {checklist.id}."
            success, error = send_email_with_attachment(recipients, subject, body, pdf_path)
            envio = EnviosEmail(checklist_id=checklist.id, destinatarios=','.join(recipients), arquivo_pdf=str(pdf_path), status='enviado' if success else 'falhou', erro=error)
            db.session.add(envio)
            db.session.commit()

        flash('Checklist salvo com sucesso', 'success')
        return redirect(url_for('checklist.dashboard'))

    sample_questions = [
        {"pergunta": "Extintor está presente?", "tipo": "sim_nao"},
        {"pergunta": "Estado do equipamento", "tipo": "multipla", "opcoes": ["Ótimo", "Bom", "Regular", "Ruim"]},
        {"pergunta": "Observações", "tipo": "texto"}
    ]
    return render_template('checklist.html', questions=sample_questions)


@checklist_bp.route('/<int:checklist_id>/pdf')
@login_required
def download_pdf(checklist_id):
    pdf_path = generate_checklist_pdf(checklist_id)
    if not pdf_path or not os.path.exists(pdf_path):
        flash('PDF não encontrado', 'warning')
        return redirect(url_for('checklist.dashboard'))
    return send_file(pdf_path, as_attachment=True)


@checklist_bp.route('/export/excel')
@login_required
def export_excel():
    path = export_checklists_excel()
    if not path or not os.path.exists(path):
        flash('Erro ao gerar Excel', 'warning')
        return redirect(url_for('checklist.dashboard'))
    return send_file(path, as_attachment=True)


@checklist_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Serve uploaded files (images/assinaturas)
    base = os.path.abspath(config.UPLOAD_FOLDER)
    return send_from_directory(base, filename)


@checklist_bp.route('/<int:checklist_id>')
@login_required
def view_checklist(checklist_id):
    checklist = Checklist.query.get_or_404(checklist_id)
    # images folder
    images_dir = os.path.join(config.UPLOAD_FOLDER, f'checklist_{checklist_id}')
    images = []
    if os.path.exists(images_dir):
        for f in os.listdir(images_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')):
                images.append(f)
    signature_file = None
    sig_path = os.path.join(config.SIGNATURE_FOLDER, f'assinatura_{checklist_id}.png')
    if os.path.exists(sig_path):
        signature_file = os.path.basename(sig_path)
    return render_template('view_checklist.html', checklist=checklist, images=images, signature=signature_file)
