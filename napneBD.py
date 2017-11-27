from flask import Flask, render_template, request, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import flask_login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///napne.sqlite3'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresl://postgres:teste@localhost/postgres'
bd = SQLAlchemy(app)
app.secret_key = 'super secret string'

login_manager = flask_login.LoginManager()

login_manager.init_app(app)

users = {'teste@teste.com': {'password': 'secret'}}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        if request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return redirect(url_for('protected'))

        flash('Usuário e/ou Senha incorreto(s)')
        return redirect(url_for('login'))

    return render_template('login.html')


@app.route('/protected')
@flask_login.login_required
def protected():
    flash('Olá {}, seu Login foi feito com sucesso!'.format(flask_login.current_user.id))
    return redirect(url_for('index'))

@app.route('/')
@flask_login.login_required
def index():
    return render_template('index.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Por favor, faça Login')
    return redirect(url_for('login'))

@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


@app.route('/formPessoa')
def formPessoa():
    return render_template('formPessoa.html')

@app.route('/formAluno')
def formAluno():
    return render_template('formAluno.html')

@app.route('/formAtendimento')
def formAtendimento():
    return render_template('formAtendimento.html')

@app.route('/gravarpessoa')
def gravarpessoa():
    pessoa = Pessoa()
    pessoa.nome = request.values.get('nome')
    bd.session.add(pessoa)
    bd.session.commit()
    return 'O USUARIO NAPNE FOI CADASTRADO COM SUCESSO!'

@app.route('/gravaraluno')
def gravaraluno():
    aluno = Aluno()
    aluno.nome = request.values.get('nome')
    bd.session.add(aluno)
    bd.session.commit()
    return 'O ALUNO FOI CADASTRADO COM SUCESSO!'

@app.route('/gravaratendimento')
def gravaratendimento():
    atendimento = Atendimento()
    atendimento.nome = request.values.get('nome')
    bd.session.add(atendimento)
    bd.session.commit()

    return 'O ATENDIMENTO FOI REGISTRADO COM SUCESSO!'


@app.route('/listarPessoa')
def listarPessoa():
    return render_template('listarPessoa.html',pessoas=Pessoa.query.all())

@app.route('/listarAluno')
def listarAluno():
    return render_template('listarAluno.html',alunos=Pessoa.query.all())

@app.route('/listarAtendimento')
def listarAtendimento():
    return render_template('listarAtendimento.html',atendimentos=Pessoa.query.all())

#########################
class User(flask_login.UserMixin):
    pass


@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return

    user = User()
    user.id = email
    return user


@login_manager.request_loader
def request_loader(request):
    email = request.form.get('email')
    if email not in users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    # user = User(request.form['username'] , request.form['password'],request.form['email'])
    users[request.form['username']] = {'password': request.form['password']}
    flash('USUARIO REGISTRADO COM SUCESSO!')
    return redirect(url_for('login'))

########################

class Aluno(bd.Model):
    codigo=bd.Column('codigo_aluno', bd.Integer, primary_key=True)
    nome=bd.Column(bd.String(100))
    turma=bd.Column(bd.String(20))
    turno=bd.Column(bd.String(10))
    periodo=bd.Column(bd.Integer)
    curso=bd.Column(bd.String(100))
    deficiencia=bd.Column(bd.String(200))
    cpf=bd.Column(bd.String(20))
    rg=bd.Column(bd.String(10))
    endereco=bd.Column(bd.String(200))
    telefone=bd.Column(bd.String(50))
    email=bd.Column(bd.String(100))
    dataNasc=bd.Column(bd.Date)
    nomePai=bd.Column(bd.String(200))
    nomeMae=bd.Column(bd.String(200))
    inss=bd.Column(bd.String(200))
    auxRecebido=bd.Column(bd.String(200))
    laudo=bd.Column(bd.LargeBinary)
    medicamento=bd.Column(bd.Boolean)
    acompMedico=bd.Column(bd.Boolean)
    medico=bd.Column(bd.String(200))
    atendimentoEspecifico=bd.Column(bd.Boolean)
    ledorTranscritor=bd.Column(bd.Boolean)
    materialBraille=bd.Column(bd.Boolean)
    tradutorInterpLingSinais=bd.Column(bd.Boolean)
    cuidador=bd.Column(bd.Boolean)
    lupas=bd.Column(bd.Boolean)
    interpRepetidorOralizador=bd.Column(bd.Boolean)
    materialDidatTextoAmpl=bd.Column(bd.Boolean)
    profApoio=bd.Column(bd.Boolean)
    muletaBengala=bd.Column(bd.Boolean)
    guiaInterpretador=bd.Column(bd.Boolean)
    outrasCondRecursosEspNec=bd.Column(bd.String(200))
    qualAcompanhamentoMedico=bd.Column(bd.String(250))


class Pessoa(bd.Model):
    codigo=bd.Column('codigo_pessoa', bd.Integer, primary_key=True)
    nome=bd.Column(bd.String(200))
    cpf=bd.Column(bd.String(20))
    rg=bd.Column(bd.String(10))
    endereco=bd.Column(bd.String(200))
    telefone=bd.Column(bd.String(50))
    profissao=bd.Column(bd.String(100))
    senha=bd.Column(bd.String(15))
    def login(self):
        pass

class Atendimento(bd.Model):
    codigo=bd.Column('codigo_aluno', bd.Integer, primary_key=True)
    nome=bd.Column(bd.String(100))
    #profissional=bd.Column('codigo_Pessoa', bd.Integer, bd.ForeignKey('user.codigo'), nullable=False)
    #aluno=bd.Column('codigo_Aluno', bd.Integer, bd.ForeignKey('user.codigo'), nullable=False)
    data=bd.Column(bd.Date)
    numero=bd.Column(bd.Integer)
    hora=bd.Column(bd.String(10))
    relato=bd.Column(bd.String(300))
    acaoArquitetonica=bd.Column(bd.String(100))
    acaoPedagogica=bd.Column(bd.String(100))
    acaoAtitudianl=bd.Column(bd.String(100))
    acaoTecnologica=bd.Column(bd.String(100))
    acaoComunicacional=bd.Column(bd.String(100))
    profissionaisEnvolv=bd.Column(bd.String(100))
    equipMatApoioDidatPedag=bd.Column(bd.String(200))
    atividDesenvNapne=bd.Column(bd.String(100))
    parceriasNecesDesenvAtivid=bd.Column(bd.String(200))


if __name__ == '__main__':
    bd.create_all()
    app.run(debug=True)
