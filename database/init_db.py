from manutencao_checklist import create_app
from extensions import db
import os
from werkzeug.security import generate_password_hash


def create_tables():
    app = create_app()
    with app.app_context():
        # import models so tables are registered
        from models import User
        db.create_all()
        print('Database tables created.')

        # Optionally create admin from environment variables
        admin_name = os.getenv('ADMIN_NAME')
        admin_email = os.getenv('ADMIN_EMAIL')
        admin_password = os.getenv('ADMIN_PASSWORD')
        if admin_email and admin_password:
            existing = User.query.filter_by(email=admin_email).first()
            if not existing:
                user = User(nome=admin_name or 'Admin', email=admin_email, senha_hash=generate_password_hash(admin_password), perfil='administrador')
                db.session.add(user)
                db.session.commit()
                print(f'Administrador {admin_email} criado.')
            else:
                print(f'Administrador {admin_email} já existe.')


if __name__ == '__main__':
    create_tables()
