from flask import Flask, render_template, url_for
from flask import request, session, redirect
from flask_pymongo import PyMongo
from flask_bcrypt import Bcrypt, check_password_hash, generate_password_hash
import random

# setup
app = Flask(__name__)
app.config['MONGO_URI'] = 'mongodb://localhost:8027/flaskDB'
app.secret_key = "Um4 s3nh4 qualquer!"
bcrypt = Bcrypt(app)
mongo = PyMongo(app)

# home
@app.route('/')
def index():
    entries = mongo.db.produtos.find()
    return render_template('index.html', entries = entries)

# produtos por categoria
@app.route('/<page>/<np>', methods=['GET'])
def homeNavega(page=None, np=None):
    try:
        print(page)
        if page=='cat':
            if int(np):
                entries = mongo.db.produtos.find({"id_categoria": int(np)})
                return render_template('index.html', local=page, entries=entries, np=np)
            else: 
                return render_template('index.html')
            return render_template('login.html', form='login')
    except: 
        return render_template('index.html')

# insert aleatorio de 1000 produtos
@app.route('/xyz15')
def xyz15():
    produtos = ('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    cat = 1
    for x in range(0, 1000):
        prdAleatorio = produtos[random.randint(0, len(produtos)-1)]
        produto = {
            "nome": f'Produto {prdAleatorio}',
            "descricao": f'Mini texto sobre o produto {prdAleatorio}',
            "id_categoria": cat,
            "estoque": random.randint(10, 100),
            "valor": random.randint(10, 150),
            "imagem": f'{random.randint(1, 10)}.jpg',
            "status": 1
        }
        mongo.db.produtos.insert_one(produto)
        if cat < 20:
            cat += 1
        else:
            cat = 1
    return redirect(url_for('index'))

# efetuar autenticacao
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        # print(request.method)
        form = request.form
        email = form.get('email')
        senha = form.get('senha')
        # print(email, senha)
        ok = 0
        msg = ''
        qtdLogin = mongo.db.usuarios.count_documents({"email": email})
        print(qtdLogin)
        if qtdLogin == 0: # mongo.db.usuarios.count_documents({"email": email}) == 0:
                msg = 'Usuário não existe.'
                # print(msg)
        elif qtdLogin==1:
            try:
                check = mongo.db.usuarios.find_one_or_404({"email": email})
                print(f"LOGIN: {check['email']}\nSENHA: {check['senha']}\nQTD: {qtdLogin}")
                
                if not check_password_hash(check['senha'], senha): # mongo.db.usuarios.count_documents({"email": email, "senha": BinData(0, senha_crypt)}) == 0:
                    msg = 'Senha incorreta'
                    # print(f"SENHA: {check['senha']}\nFORM: {senha}")
                    # print(msg)
                else:
                    session.clear()
                    ok=1
                    senha_crypt = generate_password_hash(senha, 10)
                    session['s_nome'] = check['nome']
                    session['s_email'] = check['email']
                    session['s_logado'] = 1
                    msg = "Usuário conectado"
                    print(session['s_email'], session['s_logado'])
            except Exception as e:
                msg = f'Erro: {e}'
        if ok==1:
            return render_template('login.html', form='autenticado', msg=msg, ok=ok)
        else:
            return render_template('login.html', form='login', msg=msg, ok=ok)
    else:
        return render_template('login.html', form='login')

# cadastro de usuario
@app.route('/registro', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        form = request.form
        usuario = mongo.db.usuarios
        email = form.get('email')
        existe = usuario.find_one({'email': email})
        if existe is None:
            nome = form.get('nome')
            senha = form.get('senha')
            senha_crypt = generate_password_hash(senha, 10)
            usuario.insert_one({'nome': nome, 'email': email, 'senha': senha_crypt})
            session['email'] = request.form['email']
            return render_template('login.html', form='login', msg='Cadastro realizado!', ok=1)  
        else:
            return render_template('login.html', form='registro', msg='Usuario existente!', ok=2)   
    else:
        return render_template('login.html', form='registro')

# minha conta
@app.route('/minha-conta')
def minhaconta():
    return render_template('login.html', form='autenticado')

# lembrete de senha
@app.route('/esqueci', methods=['POST', 'GET'])
def esqueceu():
    return render_template('login.html', form='esqueci')

# efetuar logout
@app.route('/logout')
def logout():
    try:
        session.clear()
    except:
        pass
    return render_template('login.html', form='login')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=9090)