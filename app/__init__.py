from flask import Flask
import os
from dotenv import load_dotenv
from groq import Groq
from app.db.db import init_db

# Cargar variables de entorno
load_dotenv()

# Inicializar cliente Groq
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def create_app():
    app = Flask(__name__)

    with app.app_context():
        init_db()

    # Registrar rutas
    from app.routes import bp
    app.register_blueprint(bp)

    return app