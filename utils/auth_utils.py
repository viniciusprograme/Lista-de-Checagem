from functools import wraps
from flask import session, redirect, url_for, flash


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Por favor faça login', 'warning')
            return redirect(url_for('auth.login'))
        return func(*args, **kwargs)
    return wrapper


def current_user():
    if 'user_id' in session:
        return {
            'id': session.get('user_id'),
            'nome': session.get('user_nome'),
            'email': session.get('user_email'),
            'perfil': session.get('user_perfil'),
        }
    return None
