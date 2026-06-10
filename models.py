from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    perfil = db.Column(db.String(20), nullable=False, default='inspetor')


class Checklist(db.Model):
    __tablename__ = 'checklists'
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.DateTime, default=datetime.utcnow)
    tecnico = db.Column(db.String(120))
    equipamento = db.Column(db.String(120))
    local = db.Column(db.String(200))
    status = db.Column(db.String(20), default='aberto')
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    perguntas = db.relationship('Pergunta', backref='checklist', cascade='all, delete-orphan')
    assinatura = db.relationship('Assinatura', backref='checklist', uselist=False)


class Pergunta(db.Model):
    __tablename__ = 'perguntas'
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'))
    pergunta = db.Column(db.Text)
    tipo = db.Column(db.String(20))


class Resposta(db.Model):
    __tablename__ = 'respostas'
    id = db.Column(db.Integer, primary_key=True)
    pergunta_id = db.Column(db.Integer, db.ForeignKey('perguntas.id'))
    resposta = db.Column(db.Text)
    imagem = db.Column(db.String(255))


class Assinatura(db.Model):
    __tablename__ = 'assinaturas'
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'))
    arquivo = db.Column(db.String(255))
    data_assinatura = db.Column(db.DateTime, default=datetime.utcnow)


class EnviosEmail(db.Model):
    __tablename__ = 'envios_email'
    id = db.Column(db.Integer, primary_key=True)
    checklist_id = db.Column(db.Integer, db.ForeignKey('checklists.id'))
    data_envio = db.Column(db.DateTime, default=datetime.utcnow)
    destinatarios = db.Column(db.Text)
    arquivo_pdf = db.Column(db.String(255))
    status = db.Column(db.String(20))
    erro = db.Column(db.Text)
