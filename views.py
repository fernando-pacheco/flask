from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import app, db
from utils import recuperar_imagem, deletar_arquivo
import time

# ROTAS
@app.route('/')
def index():
    lista = Jogos.query.order_by(Jogos.id)
    return render_template('lista.html', titulo="Jogos", jogos=lista)

@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    else:
        return render_template('novo.html', titulo="Cadastrar novo jogo")
    
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    capa_jogo = recuperar_imagem(id)
    return render_template('editar.html', titulo="Editando jogo", jogo=jogo, capa_jogo=capa_jogo)

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogos.query.filter_by(nome=nome).first()

    if jogo:
        flash('Jogo já existente!')
        return redirect(url_for('index'))
    else:
        novo_jogo = Jogos(nome=nome, categoria=categoria, console=console)
        db.session.add(novo_jogo)
        db.session.commit()

        arquivo = request.files['arquivo']
        upload_path = app.config['UPLOAD_PATH']
        timestamp = time.time()
        arquivo.save(f'{upload_path}/capa_{novo_jogo.id}_{novo_jogo.nome}-{timestamp}.jpg')

        flash('Jogo criado com sucesso!')
        return redirect(url_for('index'))
    
@app.route('/atualizar', methods=['POST'])
def atualizar():
    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = request.form['nome']
    jogo.categoria = request.form['categoria']
    jogo.console = request.form['console']
    db.session.add(jogo)
    db.session.commit()

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    timestamp = time.time()
    deletar_arquivo(jogo.id)
    arquivo.save(f'{upload_path}/capa_{jogo.id}_{jogo.nome}-{timestamp}.jpg')

    flash('Jogo atualizado com sucesso!')
    return redirect(url_for('index'))
    
@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login", proxima=proxima)

@app.route('/autenticar', methods=['POST'])
def autenticar():
    usuario = Usuarios.query.filter_by(nickname=request.form['usuario']).first()
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.nickname
            flash(usuario.nickname + ' logado com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect('novo')
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

@app.route('/deletar/<int:id>')
def deletar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('deletar')))
    jogo = Jogos.query.filter_by(id=id).first()
    db.session.delete(jogo)
    db.session.commit()
    flash('Jogo removido com sucesso!')
    return redirect(url_for('index'))

@app.route('/uploads/<nome_arquivo>')
def imagem(nome_arquivo):
    return send_from_directory('uploads', nome_arquivo)

