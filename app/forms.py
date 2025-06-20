from flask_wtf import FlaskForm  # Importa a classe base para formulários Flask
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField  # Importa campos de formulário
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError  # Importa validadores
from app.models import Usuario  # Importa o modelo de usuário
from flask_login import current_user  # Importa o usuário atual logado
from flask_wtf.file import FileField, FileAllowed  # Importa campos e validadores para upload de arquivos


class RegistrarForm(FlaskForm):
    """
    Formulário para registro de novos usuários.
    """
    username = StringField(
        "Nome de Usuário",
        validators=[DataRequired(message="O nome de usuário é obrigatório")],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="O email é obrigatório"),
            Email(message="Email inválido"),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="A senha é obrigatória"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres"),
        ],
    )
    confirmar_senha = PasswordField(
        "Confirmar Senha",
        validators=[
            DataRequired(message="A confirmação da senha é obrigatória"),
            EqualTo("senha", message="As senhas não coincidem"),
        ],
    )
    submit_registrar = SubmitField("Criar Conta")

    def validate_email(self, email):
        """
        Valida se o email já está cadastrado no banco de dados.
        Parâmetros:
            email (Field): Campo de email do formulário.
        Levanta:
            ValidationError: Se o email já estiver em uso.
        """
        usuario = Usuario.query.filter_by(email=email.data).first()  # Busca usuário pelo email
        if usuario:
            raise ValidationError(
                "Já existe uma conta com esse email. Por favor, escolha outro."
            )


class LoginForm(FlaskForm):
    """
    Formulário para login de usuários.
    """
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="O email é obrigatório"),
            Email(message="Email inválido"),
        ],
    )
    senha = PasswordField(
        "Senha",
        validators=[
            DataRequired(message="A senha é obrigatória"),
            Length(min=6, message="A senha deve ter pelo menos 6 caracteres"),
        ],
    )
    lembrar_me = BooleanField("Lembrar-me")
    submit_login = SubmitField("Fazer Login")


class EditarPerfilForm(FlaskForm):
    """
    Formulário para edição do perfil do usuário.
    Permite alterar nome, email, cursos e foto de perfil.
    """
    username = StringField(
        "Nome de Usuário",
        validators=[DataRequired(message="O nome de usuário é obrigatório")],
    )
    email = StringField(
        "Email",
        validators=[
            DataRequired(message="O email é obrigatório"),
            Email(message="Email inválido"),
        ],
    )

    # Campos booleanos para seleção de cursos
    curso_iniciante = BooleanField("Python para Iniciantes")
    curso_data_science = BooleanField("Python para Ciência de Dados")
    curso_desenvolvimento_web = BooleanField("Python para Desenvolvimento Web")
    curso_machine_learning = BooleanField("Python para Machine Learning")
    curso_inteligencia_artificial = BooleanField("Python para Inteligência Artificial")
    curso_automacao = BooleanField("Python para Automação")
    curso_jogos = BooleanField("Python para Desenvolvimento de Jogos")
    curso_devops = BooleanField("Python para DevOps")
    curso_ciberseguranca = BooleanField("Python para Cibersegurança")
    curso_financas = BooleanField("Python para Finanças e Mercado Financeiro")

    foto_perfil = FileField(
        "Alterar Foto de Perfil",
        validators=[
            FileAllowed(["jpg", "png"], "Somente imagens JPG e PNG são permitidas.")
        ],
    )
    submit_editar = SubmitField("Salvar Alterações")

    def validate_email(self, email):
        """
        Valida se o novo email já está cadastrado no banco de dados, exceto para o próprio usuário.
        Parâmetros:
            email (Field): Campo de email do formulário.
        Levanta:
            ValidationError: Se o email já estiver em uso por outro usuário.
        """
        usuario = Usuario.query.filter_by(email=email.data).first()  # Busca usuário pelo email
        if current_user.email != email.data and usuario:
            raise ValidationError(
                "Já existe uma conta com esse email. Por favor, escolha outro."
            )


class CriarPostForm(FlaskForm):
    """
    Formulário para criação de novos posts.
    """
    titulo = StringField(
        "Título",
        validators=[DataRequired(message="O título é obrigatório")],
    )
    conteudo = TextAreaField(
        "Escreva seu post aqui",
        validators=[DataRequired(message="O conteúdo é obrigatório")],
    )
    submit_criar_post = SubmitField("Criar Post")