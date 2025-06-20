from datetime import (  # Importa classes para manipulação de datas e fuso horário
    datetime,
    timezone,
)

from flask_login import UserMixin  # Importa classe para integração com Flask-Login

from app import (  # Importa instâncias do banco de dados e do login manager
    db,
    login_manager,
)


@login_manager.user_loader
def load_usuario(usuario_id):
    """
    Função utilizada pelo Flask-Login para carregar o usuário pelo ID.
    Parâmetros:
        usuario_id (int): ID do usuário a ser carregado.
    Retorna:
        Usuario: Instância do usuário correspondente ao ID.
    """
    return Usuario.query.get(int(usuario_id))  # Busca o usuário pelo ID no banco


class Usuario(db.Model, UserMixin):
    """
    Modelo que representa um usuário no banco de dados.
    Herda de db.Model (SQLAlchemy) e UserMixin (Flask-Login).
    """

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    username = db.Column(db.String(100), nullable=False)  # Nome de usuário
    email = db.Column(db.String(120), unique=True, nullable=False)  # E-mail único
    senha = db.Column(db.String(200), nullable=False)  # Senha (hash)
    foto_perfil = db.Column(
        db.String(200), nullable=True, default="default.jpg"
    )  # Foto de perfil
    cursos = db.Column(db.String(200), nullable=True, default="")  # Cursos do usuário
    post = db.relationship(
        "Post", backref="autor", lazy=True
    )  # Relacionamento com posts

    def contar_posts(self):
        """
        Conta a quantidade de posts criados pelo usuário.
        Retorna:
            int: Número de posts do usuário.
        """
        return Post.query.filter_by(
            usuario_id=self.id
        ).count()  # Conta posts pelo ID do usuário


class Post(db.Model):
    """
    Modelo que representa um post no banco de dados.
    """

    id = db.Column(db.Integer, primary_key=True)  # Chave primária
    titulo = db.Column(db.String(100), nullable=False)  # Título do post
    conteudo = db.Column(db.Text, nullable=False)  # Conteúdo do post
    data_postagem = db.Column(
        db.DateTime, nullable=False, default=datetime.now(timezone.utc)
    )  # Data e hora da postagem
    usuario_id = db.Column(
        db.Integer, db.ForeignKey("usuario.id"), nullable=False
    )  # ID do autor (chave estrangeira)
