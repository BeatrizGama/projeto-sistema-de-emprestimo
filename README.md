
**Data de Início:** 03/24
**Data de Encerramento:** 06/24
Aqui está um exemplo de README.md no estilo típico de projetos de código, destacando as bibliotecas necessárias e instruções de instalação:

# Sistema de Gestão de Equipamentos Acadêmicos

Este repositório contém o código para um Sistema de Gestão de Equipamentos Acadêmicos, desenvolvido para facilitar o gerenciamento e a utilização de equipamentos por professores da Universidade Federal Rural do Rio de Janeiro (UFRRJ).

(images/tela_usuario.png)

## Autores

- Beatriz Fernandes Gama de Lima
- Julia da Silva Borges
- Bruna de Andrade da Silva
- Bruna Luísa Costa Reis dos Santos

## Descrição

Este projeto foi criado para solucionar problemas na distribuição e agendamento de equipamentos acadêmicos. O sistema permite que professores e secretários realizem reservas, gerenciem equipamentos, visualizem agendamentos e muito mais, tudo de forma intuitiva e eficiente.

## Instalação

### Pré-requisitos

Certifique-se de ter o Python 3.x e o pip instalados em seu ambiente. Além disso, será necessário o gerenciador de pacotes `virtualenv`.

### Passos para Instalação

1. **Clone o Repositório:**

   ```bash
   git clone https://github.com/seu-usuario/sistema-gestao-equipamentos.git
   cd sistema-gestao-equipamentos
   ```

2. **Crie e Ative um Ambiente Virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows use `venv\Scripts\activate`
   ```

3. **Instale as Dependências:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o Banco de Dados:**

   ```bash
   flask db init
   flask db migrate
   flask db upgrade
   ```

5. **Execute a Aplicação:**

   ```bash
   flask run
   ```

### Bibliotecas Utilizadas

- **Flask:** Framework web leve para Python.
- **Flask-Login:** Gerenciamento de sessões de login de usuário.
- **Flask-SQLAlchemy:** Integração do SQLAlchemy com o Flask.
- **Flask-Migrate:** Gerenciamento de migrações de banco de dados para SQLAlchemy.
- **Werkzeug:** Utilitários para WSGI e aplicações web.

## Uso

Após seguir os passos de instalação, a aplicação estará disponível em `http://127.0.0.1:5000/`. A partir daí, você pode acessar as diversas funcionalidades do sistema, como cadastro, login, agendamento de equipamentos, entre outros.

### Páginas Principais

- `/`: Redireciona para a página de login.
- `/login`: Página de login.
- `/usuarios/<email>`: Dashboard para usuários.
- `/secretarios/<email>`: Dashboard para secretários.
- `/cadastro`: Página de cadastro de novos usuários.
- `/add_equipamento`: Formulário para adicionar novos equipamentos.
- `/add_agendamento`: Formulário para agendar equipamentos.

