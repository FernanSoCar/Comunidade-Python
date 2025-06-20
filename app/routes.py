import os  # Importa módulo para manipulação de caminhos e diretórios
import secrets  # Importa módulo para geração de tokens seguros

from flask import (  # Importa funções do Flask
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import (  # Importa funções de autenticação do Flask-Login
    current_user,
    login_required,
    login_user,
    logout_user,
)
from PIL import Image  # Importa biblioteca para manipulação de imagens
from werkzeug.utils import (
    secure_filename,  # Importa função para nomes de arquivos seguros
)

from app import app, bcrypt, db  # Importa instâncias do app, bcrypt e banco de dados
from app.forms import (  # Importa formulários
    CriarPostForm,
    EditarPerfilForm,
    LoginForm,
    RegistrarForm,
)
from app.models import Post, Usuario  # Importa modelos do banco de dados


@app.route("/")
def home():
    """
    Renderiza a página inicial com a lista de posts.
    Consulta todos os posts do banco de dados, ordenados do mais recente para o mais antigo,
    e passa para o template 'home.html' junto com o usuário atual.
    Retorna:
        Response: Página HTML renderizada para a rota inicial.
    """
    posts = Post.query.order_by(
        Post.id.desc()
    )  # Busca todos os posts ordenados do mais novo para o mais antigo
    return render_template(
        "home.html", posts=posts, usuario=current_user
    )  # Renderiza o template passando os posts e o usuário


@app.route("/contato")
def contato():
    """
    Renderiza a página de contato.
    Retorna:
        str: Template HTML renderizado para a página de contato.
    """
    return render_template("contato.html")  # Renderiza o template de contato


@app.route("/usuarios")
@login_required  # Exige que o usuário esteja logado para acessar
def usuarios():
    """
    Exibe todos os usuários cadastrados.
    Consulta todos os usuários do banco de dados e renderiza o template 'usuarios.html',
    passando a lista de usuários como 'lista_usuarios'.
    Retorna:
        Response: Página HTML renderizada com a lista de usuários.
    """
    lista_usuarios = Usuario.query.all()  # Busca todos os usuários cadastrados
    return render_template(
        "usuarios.html", lista_usuarios=lista_usuarios
    )  # Renderiza o template com a lista


@app.route("/login-registrar", methods=["GET", "POST"])
def login_registrar():
    """
    Gerencia o login e o registro de usuários.
    Processa os formulários de login e registro. Se o login for bem-sucedido, autentica o usuário.
    Se o registro for bem-sucedido, cria uma nova conta de usuário.
    Retorna:
        Response: Página HTML renderizada para login/registro ou redireciona em caso de sucesso.
    """
    form_login = LoginForm()  # Instancia o formulário de login
    form_registrar = RegistrarForm()  # Instancia o formulário de registro

    # Verifica se o formulário de login foi submetido e é válido
    if form_login.validate_on_submit() and "submit_login" in request.form:
        usuario = Usuario.query.filter_by(
            email=form_login.email.data
        ).first()  # Busca usuário pelo e-mail
        # Verifica se o usuário existe e se a senha está correta usando bcrypt
        if usuario and bcrypt.check_password_hash(usuario.senha, form_login.senha.data):
            login_user(
                usuario, remember=form_login.lembrar_me.data
            )  # Realiza login do usuário
            flash(
                f"Login realizado com sucesso para {form_login.email.data}!",
                "alert-success",
            )
            params_next = request.args.get(
                "next"
            )  # Verifica se há uma página para redirecionar após login
            if params_next:
                return redirect(params_next)
            else:
                return redirect(url_for("home"))
        else:
            flash("Email ou senha incorretos. Tente novamente.", "alert-danger")
    # Verifica se o formulário de registro foi submetido e é válido
    if form_registrar.validate_on_submit() and "submit_registrar" in request.form:
        senha_hash = bcrypt.generate_password_hash(form_registrar.senha.data).decode(
            "utf-8"
        )  # Gera hash da senha
        usuario = Usuario(
            username=form_registrar.username.data,
            email=form_registrar.email.data,
            senha=senha_hash,
            cursos="",
        )  # Cria novo usuário
        db.session.add(usuario)  # Adiciona usuário ao banco
        db.session.commit()  # Salva no banco
        flash(
            f"Conta criada com sucesso para {form_registrar.email.data}!",
            "alert-success",
        )
        return redirect(url_for("home"))
    # Renderiza a página de login/registro com os formulários
    return render_template(
        "login_registrar.html", form_login=form_login, form_registrar=form_registrar
    )


@app.route("/sair")
def sair():
    """
    Faz logout do usuário atual e redireciona para a página inicial.
    Retorna:
        Response: Redirecionamento para a página inicial após logout.
    """
    logout_user()  # Realiza logout
    flash("Você saiu com sucesso.", "alert-success")  # Mensagem de sucesso
    return redirect(url_for("home"))  # Redireciona para home


@app.route("/perfil")
@login_required
def perfil():
    """
    Renderiza a página de perfil do usuário atual.
    Retorna:
        Response: Página HTML renderizada do perfil do usuário.
    """
    foto_perfil = url_for(
        "static", filename=f"imagens/{current_user.foto_perfil}"
    )  # Monta o caminho da foto de perfil
    return render_template(
        "perfil.html", foto_perfil=foto_perfil, usuario=current_user
    )  # Renderiza o perfil


@app.route("/post/criar", methods=["GET", "POST"])
@login_required
def criar_post():
    """
    Gerencia a criação de um novo post.
    Se o formulário for enviado e válido, salva o post no banco de dados.
    Retorna:
        Response: Página HTML renderizada para criação de post ou redireciona em caso de sucesso.
    """
    form = CriarPostForm()  # Instancia o formulário de criação de post
    if form.validate_on_submit():  # Verifica se o formulário foi submetido e é válido
        post = Post(
            titulo=form.titulo.data,
            conteudo=form.conteudo.data,
            autor=current_user,
        )  # Cria novo post
        db.session.add(post)  # Adiciona ao banco
        db.session.commit()  # Salva no banco
        flash("Post criado com sucesso!", "alert-success")
        return redirect(url_for("home"))  # Redireciona para home
    return render_template(
        "criar_post.html", form=form, usuario=current_user
    )  # Renderiza o formulário


def salvar_imagem(imagem):
    """
    Salva uma imagem enviada pelo usuário na pasta static/imagens após redimensionar.
    Parâmetros:
        imagem (FileStorage): Arquivo de imagem enviado pelo usuário.
    Retorna:
        str: Nome do arquivo da imagem salva.
    """
    # Gera um nome seguro para o arquivo e uma string aleatória para evitar conflitos
    nome_seguro = secure_filename(imagem.filename)
    extensao = nome_seguro.rsplit(".", 1)[1].lower()
    nome_arquivo = f"{secrets.token_hex(8)}.{extensao}"  # Gera nome único
    caminho_pasta = os.path.join(
        current_app.root_path, "static/imagens"
    )  # Caminho da pasta de imagens
    tamanho_maximo = (400, 400)  # Define tamanho máximo
    imagem = Image.open(imagem)  # Abre a imagem
    imagem.thumbnail(tamanho_maximo)  # Redimensiona a imagem para no máximo 400x400
    caminho_arquivo = os.path.join(
        caminho_pasta, nome_arquivo
    )  # Caminho completo do arquivo
    os.makedirs(caminho_pasta, exist_ok=True)  # Garante que a pasta existe
    imagem.save(caminho_arquivo)  # Salva a imagem
    return nome_arquivo  # Retorna o nome do arquivo salvo


def atualizar_cursos(form):
    """
    Atualiza os cursos do usuário com base nos campos do formulário enviados.
    Parâmetros:
        form (FlaskForm): Formulário contendo os campos de cursos.
    Retorna:
        str: String com os cursos selecionados separados por ponto e vírgula.
    """
    lista_cursos = []
    # Percorre todos os campos do formulário e verifica se o campo é de curso e está selecionado
    for campo in form:
        if "curso_" in campo.name:
            if campo.data:
                lista_cursos.append(
                    campo.label.text
                )  # Adiciona o nome do curso selecionado
    return ";".join(lista_cursos)  # Retorna os cursos separados por ponto e vírgula


@app.route("/perfil/editar/", methods=["GET", "POST"])
@login_required
def editar_perfil():
    """
    Gerencia a edição do perfil do usuário.
    Atualiza nome de usuário, email, foto de perfil e cursos.
    Retorna:
        Response: Página HTML renderizada para edição do perfil ou redireciona em caso de sucesso.
    """
    form = EditarPerfilForm()  # Instancia o formulário de edição de perfil
    if form.validate_on_submit():  # Se o formulário foi submetido e é válido
        current_user.username = form.username.data  # Atualiza nome de usuário
        current_user.email = form.email.data  # Atualiza email
        if form.foto_perfil.data:  # Se foi enviada nova foto de perfil
            current_user.foto_perfil = salvar_imagem(
                form.foto_perfil.data
            )  # Salva a imagem e atualiza o campo
        db.session.commit()  # Salva alterações no banco
        current_user.cursos = atualizar_cursos(form)  # Atualiza cursos selecionados
        db.session.commit()  # Salva novamente
        flash("Perfil atualizado com sucesso!", "alert-success")
        return redirect(url_for("perfil"))  # Redireciona para o perfil
    elif request.method == "GET":
        # Preenche o formulário com os dados atuais do usuário
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.foto_perfil.data = current_user.foto_perfil
        # Marca os cursos já selecionados pelo usuário
        for campo in form:
            for curso in current_user.cursos.split(";"):
                if curso == campo.label.text:
                    campo.data = True
    foto_perfil = url_for(
        "static", filename=f"imagens/{current_user.foto_perfil}"
    )  # Caminho da foto de perfil
    return render_template(
        "editar_perfil.html", foto_perfil=foto_perfil, form=form, usuario=current_user
    )  # Renderiza o formulário


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
@login_required
def post(post_id):
    """
    Exibe e permite a edição de um post específico pelo autor.
    Parâmetros:
        post_id (int): ID do post a ser exibido/editado.
    Retorna:
        Response: Página HTML renderizada do post.
    """
    post = Post.query.get(post_id)  # Busca o post pelo ID
    # Permite edição apenas se o usuário atual for o autor do post
    if current_user == post.autor:
        form = CriarPostForm()  # Instancia o formulário de edição de post
        if request.method == "GET":
            form.titulo.data = post.titulo  # Preenche o campo título
            form.conteudo.data = post.conteudo  # Preenche o campo conteúdo
        elif form.validate_on_submit():
            post.titulo = form.titulo.data  # Atualiza título
            post.conteudo = form.conteudo.data  # Atualiza conteúdo
            db.session.commit()  # Salva alterações
            flash("Post atualizado com sucesso!", "alert-success")
            return redirect(url_for("home"))
    else:
        form = None  # Usuário não é autor, não pode editar
    return render_template(
        "post.html", post=post, usuario=current_user, form=form
    )  # Renderiza o post


@app.route("/post/<int:post_id>/deletar", methods=["GET", "POST"])
@login_required
def deletar_post(post_id):
    """
    Deleta um post específico se o usuário atual for o autor.
    Parâmetros:
        post_id (int): ID do post a ser deletado.
    Retorna:
        Response: Redireciona para a página inicial após a exclusão ou retorna erro 403.
    """
    post = Post.query.get(post_id)  # Busca o post pelo ID
    # Só permite deletar se o usuário for o autor do post
    if current_user == post.autor:
        db.session.delete(post)  # Deleta o post
        db.session.commit()  # Salva no banco
        flash("Post deletado com sucesso!", "alert-danger")
        return redirect(url_for("home"))
    else:
        abort(403)  # Retorna erro 403 se não for o autor
