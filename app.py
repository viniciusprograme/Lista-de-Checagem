import os
from flask import Flask, redirect, url_for
import config
from extensions import db


def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")
    app.config.from_object(config)
    db.init_app(app)

    # Ensure upload/report folders exist
    for folder in (config.UPLOAD_FOLDER, config.SIGNATURE_FOLDER, config.IMAGE_FOLDER, config.PDF_FOLDER, config.EXCEL_FOLDER):
        os.makedirs(folder, exist_ok=True)

    # Register blueprints if available
    try:
        from routes.auth import auth_bp
        from routes.checklist_routes import checklist_bp
        app.register_blueprint(auth_bp)
        app.register_blueprint(checklist_bp)
    except Exception:
        pass

    @app.route('/')
    def index():
        return redirect(url_for('auth.login'))

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
