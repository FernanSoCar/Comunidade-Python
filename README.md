# Comunidade Python - Projeto Flask Completo

Este projeto é um site de comunidade desenvolvido do zero utilizando o framework Flask, com funcionalidades de autenticação de usuários, criação e edição de posts, upload de fotos de perfil, seleção de cursos e muito mais. O objetivo é servir como material educacional para quem deseja aprender a construir aplicações web completas com Python e Flask.

## Tecnologias Utilizadas

- **Python 3**
- **Flask** (framework web)
- **Flask-WTF** (formulários e proteção CSRF)
- **Flask-Login** (autenticação de usuários)
- **Flask-Bcrypt** (hash de senhas)
- **Flask-SQLAlchemy** (ORM para banco de dados)
- **SQLite** (banco de dados)
- **Pillow** (manipulação de imagens)
- **HTML/CSS** (templates e estilização)
- **Bootstrap** (opcional, para layout responsivo)

## Funcionalidades

- Cadastro e login de usuários
- Edição de perfil com upload de foto e seleção de cursos
- Criação, edição e exclusão de posts
- Listagem de usuários e posts
- Proteção CSRF em formulários
- Hash de senhas com Bcrypt
- Banco de dados SQLite com SQLAlchemy

## Como rodar o projeto

1. Clone este repositório:
   ```bash
   git clone https://github.com/seu-usuario/seu-repo.git
   ```
2. Instale as dependências:
   ```bash
   uv pip install
   ```
3. Configure a variável de ambiente para a chave secreta (NUNCA coloque a chave secreta diretamente no código):
   ```bash
   export SECRET_KEY='sua_chave_secreta_segura'
   ```
   Ou crie um arquivo `.env` e utilize uma biblioteca como `python-dotenv` para carregar as variáveis de ambiente.
4. Execute a aplicação:
   ```bash
   flask run
   ```

## Aviso Importante

> **Este projeto tem finalidade exclusivamente educacional.**
>
> **Não utilize dados pessoais reais para testar a aplicação.**
>
> A chave secreta (`SECRET_KEY`) utilizada no exemplo é pública e não deve ser usada em produção. Para projetos reais, sempre armazene a chave secreta em um arquivo separado ou em variáveis de ambiente, nunca diretamente no código-fonte.

## Deploy

Você pode acessar uma versão de demonstração do projeto através deste link:

[https://seu-dominio-ou-dploy-link.com](https://seu-dominio-ou-dploy-link.com)

---

Desenvolvido para fins de aprendizado com Python e Flask.