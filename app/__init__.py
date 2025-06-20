from flask import Flask  # Importa a classe principal do Flask
from flask_bcrypt import Bcrypt  # Importa a extensão para hash de senhas
from flask_login import LoginManager  # Importa a extensão para gerenciamento de login
from flask_sqlalchemy import (
    SQLAlchemy,  # Importa a extensão para banco de dados SQLAlchemy
)
from flask_wtf.csrf import CSRFProtect  # Importa proteção CSRF para formulários

app = Flask(__name__)  # Cria a instância principal do Flask

# Configurações da aplicação
app.config["SECRET_KEY"] = (
    "b85c99d270d663b913c678fd1565babf"  # Chave secreta para sessões e CSRF
)
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///comunidade.db"  # Caminho do banco de dados SQLite
)

db = SQLAlchemy(app)  # Inicializa o banco de dados
bcrypt = Bcrypt(app)  # Inicializa o Bcrypt para hash de senhas
login_manager = LoginManager(app)  # Inicializa o gerenciador de login
login_manager.login_view = "login_registrar"  # Define a view de login padrão
csrf = CSRFProtect(app)  # Inicializa a proteção CSRF
login_manager.login_message_category = "alert-info"  # Categoria da mensagem de login

from app import routes  # Importa as rotas da aplicação (deve ser feito
