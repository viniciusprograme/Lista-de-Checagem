from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from extensions import db
from models import User
from werkzeug.security import generate_password_hash, check_password_hash

auth_bp = Blueprint('auth', __name__, template_folder='../templates')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.senha_hash, senha):
            session['user_id'] = user.id
            session['user_nome'] = user.nome
            session['user_perfil'] = user.perfil
            session['user_email'] = user.email
            return redirect(url_for('checklist.dashboard'))
        else:
            flash('Credenciais inválidas', 'danger')
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    # Apenas para scaffolding; em produção restrinja a administradores
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        perfil = request.form.get('perfil', 'inspetor')
        if User.query.filter_by(email=email).first():
            flash('E-mail já cadastrado', 'warning')
            return redirect(url_for('auth.register'))
        user = User(nome=nome, email=email, senha_hash=generate_password_hash(senha), perfil=perfil)
        db.session.add(user)
        db.session.commit()
        flash('Usuário cadastrado', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html')
