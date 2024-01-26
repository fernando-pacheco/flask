from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from models import Jogos, Usuarios
from jogoteca import app, db
from utils import recuperar_imagem, deletar_arquivo, JogoForm, UserForm
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
    
    form = JogoForm()
    return render_template('novo.html', titulo="Cadastrar novo jogo", form=form)
    
@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    jogo = Jogos.query.filter_by(id=id).first()
    form = JogoForm()
    form.nome.data = jogo.nome
    form.categoria.data = jogo.categoria
    form.console.data = jogo.console
    capa_jogo = recuperar_imagem(id)
    return render_template('editar.html', titulo="Editando jogo", id=id, capa_jogo=capa_jogo, form=form)

@app.route('/criar', methods=['POST'])
def criar():
    form = JogoForm(request.form)

    if not form.validate_on_submit():
        return redirect(url_for('novo'))

    nome = form.nome.data
    categoria = form.categoria.data
    console = form.console.data
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
    form = JogoForm(request.form)

    if not form.validate_on_submit():
        flash('Erro. Verifique os dados e tente novamente.')
        return redirect(url_for('index'))

    jogo = Jogos.query.filter_by(id=request.form['id']).first()
    jogo.nome = form.nome.data
    jogo.categoria = form.categoria.data
    jogo.console = form.console.data
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
    form = UserForm()
    proxima = request.args.get('proxima')
    return render_template('login.html', titulo="Login", proxima=proxima, form=form)

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

