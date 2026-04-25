from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

#Firmando que aqui é o arquivo principal da aplicação
app = Flask(__name__)

#Configurações do banco de dados e chave secreta para sessões
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///usuarios.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'ImagineUMAChaveSecretaAqui' #Chave secreta para sessões

#Passo: 1 - Criar o banco de dados e a tabela de usuários
db = SQLAlchemy(app)
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    senha = db.Column(db.String(15), nullable=False)

    with app.app_context():
        db.create_all() #Criar as tabelas no banco de dados
    
    #Passo: 2 - Criar um usuário admin padrão se ele não existir
    if not Usuario.query.filter_by(username='admin').first():
        hash_senha = generate_password_hash('1234') #Gerar hash da senha
        novo_usuario = Usuario(username='admin', senha=hash_senha) #Criar usuário
        db.session.add(novo_usuario) #Adicionar ao banco de dados
        db.session.commit()

#Passo: 3 - Criar a rota de login para autenticar os usuários
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_form = request.form['usuario']
        senha_form = request.form['senha']
        usuario_db = Usuario.query.filter_by(username=username_form).first()
        if usuario_db and check_password_hash(usuario_db.senha, senha_form):
            session['id'] = usuario_db.id
            return redirect(url_for('autenticado'))
        else:
            return render_template('login.html', erro='Usuário ou senha incorretos')
    return render_template('login.html')