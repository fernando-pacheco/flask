from flask import Flask, render_template, request

class Jogo:
    def __init__(self, nome, categoria, console):
        self.nome = nome
        self.categoria = categoria
        self.console = console

jogo1 = Jogo('Super Mario', 'Ação', 'SNES')
jogo2 = Jogo('Pokemon Gold', 'RPG', 'GB')
jogo3 = Jogo('Mortal Kombat', 'Luta', 'SNES')
jogo4 = Jogo('Tetris', 'Puzzle', 'Atari')
jogo5 = Jogo('Football Manager', 'Futebol', 'Xbox')
lista =[jogo1, jogo2, jogo3, jogo4, jogo5]

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('lista.html', titulo="Jogos", jogos=lista)

@app.route('/novo')
def novo():
    return render_template('novo.html', titulo="Cadastrar novo jogo")

@app.route('/criar', methods=['POST'])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    jogo = Jogo(nome, categoria, console)
    lista.append(jogo)
    return render_template('lista.html', titulo="Jogos", jogos=lista)

app.run(debug=True)