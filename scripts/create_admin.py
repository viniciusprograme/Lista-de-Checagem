import os
import sys
from getpass import getpass

from manutencao_checklist import create_app
from extensions import db
from models import User
from werkzeug.security import generate_password_hash


def create_admin_interactive(name=None, email=None, password=None):
    app = create_app()
    with app.app_context():
        if not name:
            name = input('Nome do administrador: ').strip()
        if not email:
            email = input('E-mail do administrador: ').strip()
        if User.query.filter_by(email=email).first():
            print('E-mail já cadastrado')
            return
        if not password:
            password = getpass('Senha: ')
            password2 = getpass('Confirme a senha: ')
            if password != password2:
                print('Senhas não conferem')
                return
        user = User(nome=name, email=email, senha_hash=generate_password_hash(password), perfil='administrador')
        db.session.add(user)
        db.session.commit()
        print('Administrador criado com sucesso')


if __name__ == '__main__':
    # Allow passing args: name email password (password optional)
    args = sys.argv[1:]
    name = args[0] if len(args) >= 1 else None
    email = args[1] if len(args) >= 2 else None
    password = args[2] if len(args) >= 3 else None
    create_admin_interactive(name, email, password)
