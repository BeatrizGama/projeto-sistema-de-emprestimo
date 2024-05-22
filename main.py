from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin , current_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


#import json

# Criação do app em flask
app = Flask(__name__)
app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///projeto.db.sqlite'
app.app_context().push()

# Login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Base de dados
db = SQLAlchemy()
db.init_app(app)

# Definicao da tabela de usuários na base de dados 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    department = db.Column(db.String(1000))


@login_manager.user_loader
def load_user(user_id):
    # since the email is the primary key of our user table, use it in the query for the user
    return User.query.get(int(user_id))

@app.route("/") 
def homepage():
    return render_template("homepage.html") 

@app.route("/login", methods=["GET", "POST"]) # Agora aceita tanto GET quanto POST
def login():
    if request.method == "POST":
        # Lógica de autenticação aqui
        email = request.form.get('email')
        password = request.form.get('password')

        # procura este usuario na base de dados
        # se existir, o objeto "user" será uma estrutura de dados contendo os dados do usuario que vieram da base de dados
        user = User.query.filter_by(email=email).first()

        # verifica se usuario existe
        # pega a senha fornecida, calcula o hash e compara com o hash guardado no banco de dados
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for('login')) # if user doesn't exist or password is wrong, reload the page

        # se chegou aqui, o usuário é valido
        login_user(user)
        return redirect(url_for('usuarios', nome_usuario=user.email))  # Redireciona para a página inicial após o login

    return render_template("login.html") 


@app.route("/usuarios/<nome_usuario>")
@login_required
def usuarios(nome_usuario):
    user = User.query.filter_by(email=nome_usuario).first_or_404()
    # Equipamentos disponíveis (não alugados)
    available_equipments = Equipment.query.all()
    #print(available_equipments)
    # Equipamentos reservados pelo usuário atual
    #reserved_equipments = Equipment.query.filter_by(user_id=user.id).all()
    return render_template("usuarios.html", 
                           nome_usuario=nome_usuario,available_equipments =available_equipments )

@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        department = request.form["department"]

        user = User.query.filter_by(email=username).first() # if this returns a user, then the email already exists in database

        if user: # if a user is found, we want to redirect back to signup page so user can try again  
            return redirect(url_for('cadastro'))

        # create new user with the form data. Hash the password so plaintext version isn't saved.
        new_user = User(email=username, password=generate_password_hash(password, method='pbkdf2'), department=department)
        #new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'), admin=admin)

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        #usuario = {'username': username, 'password': password, 'department': department}
        #salvar_usuario(usuario)
        #return "Usuário cadastrado com sucesso!"

        return redirect(url_for("login"))

    return render_template("cadastro.html") 

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

#---------------------------------------------------------------------------------------------------------------

# Definicao da tabela de equipamentos na base de dados 
class Equipment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10), nullable=False)  # Exemplo de formato: "2024-05-22"
    horario = db.Column(db.String(5), nullable=False)  # Exemplo de formato: "15:30"
    equipment_id = db.Column(db.Integer, db.ForeignKey('equipment.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    equipment = db.relationship('Equipment', backref=db.backref('agendamentos', lazy=True))
    user = db.relationship('User', backref=db.backref('agendamentos', lazy=True))


@app.route("/add_equipment", methods=["GET", "POST"])
#@login_required
def add_equipment():
    if request.method == "POST":
        name = request.form["name"]
        description = request.form["description"]

        # Adicionar novo equipamento ao banco de dados
        new_equipment = Equipment(name=name, description=description)
        db.session.add(new_equipment)
        db.session.commit()

        return redirect(url_for('add_equipament'))


    return render_template("add_equipment.html")



@app.route("/add_agendamento", methods=["GET", "POST"])
def add_agendamento():
    if request.method == "POST":
        data = request.form["data"]
        horario = request.form["horario"]
        equipment_id = request.form["equipment_id"]
        user_id = current_user.id  # Supondo que o usuário atual está logado

        # Combine a data e o horário em um formato de data e hora completo
        data_hora_str = f"{data} {horario}"
        data_hora = datetime.strptime(data_hora_str, "%Y-%m-%d %H:%M")

        # Adicionar novo agendamento ao banco de dados
        new_agendamento = Agendamento(
            data=data_hora.strftime("%Y-%m-%d"),  # Armazena apenas a data
            horario=data_hora.strftime("%H:%M"),  # Armazena apenas o horário
            equipment_id=equipment_id,
            user_id=user_id
        )
        db.session.add(new_agendamento)
        db.session.commit()

        return redirect(url_for('homepage'))

    # Obtém todos os equipamentos disponíveis para exibir no formulário
    available_equipments = Equipment.query.all()

    return render_template("add_agendamento.html", available_equipments =available_equipments)

@app.route('/reserve_equipment', methods=['POST'])
@login_required
def reserve_equipment():
    data = request.get_json()
    equipment_id = data.get('equipment_id')
    equipment = Equipment.query.get(equipment_id)

    if equipment and equipment.user_id is None:
        equipment.user_id = current_user.id
        db.session.commit()
        return jsonify({'success': True})

    return jsonify({'success': False, 'message': 'Equipamento não encontrado ou já reservado'})



if __name__ == "__main__":

    # Inicializar/atualizar base de dados antes de iniciar a aplicacao
    db.create_all()

    # Inicia a aplicacao
    app.run(debug=True)
