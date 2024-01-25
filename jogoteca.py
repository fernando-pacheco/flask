from flask import Flask, render_template, request, redirect, session, flash, url_for

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

class Usuario:
    def __init__(self, nickname, nome, senha):
        self.nickname = nickname
        self.nome = nome
        self.senha = senha

# USUÁRIO
usuario1 = Usuario('fulano', 'Fulano de tal', '123')
usuario2 = Usuario('beltrano', 'Beltrano de tal', '456')
usuario3 = Usuario('ciclano', 'Ciclano de tal', '789')

usuarios = {
    usuario1.nickname: usuario1,
    usuario2.nickname: usuario2,
    usuario3.nickname: usuario3
}

# JOGO
jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GB')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
jogo4 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo5 = Jogo('Football Manager', 'Futebol', 'Xbox')
lista =[jogo1, jogo2, jogo3, jogo4, jogo5]

# CONFIGURAÇÃO
app = Flask(__name__)
app.secret_key = 'estudoflask'

# ROTAS
@app.route('/')
def index():
    return render_template('lista.html', titulo="Jogos", jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo="Cadastrar novo jogo")

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return redirect(url_for('index'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login", proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    if request.form['usuario'] in usuarios:
        usuario = usuarios[request.form['usuario']]
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))


    if '123' == request.form['senha']:
        session['usuario_logado'] = request.form['usuario']
        flash(f"{request.form['usuario']} logado com sucesso!")
        proxima_pagina = request.form['proxima']
        return redirect(proxima_pagina)
    else:
        flash('Usuário ou senha inválidos!')
        return redirect(url_for('login'))
    
@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('login'))

# INICIANDO A APLICAÇÃO
app.run(debug=True)