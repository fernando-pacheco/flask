import os
from jogoteca import app
from flask_wtf import FlaskForm
from wtforms import StringField, validators, SubmitField, PasswordField

class JogoForm(FlaskForm):
    nome = StringField('Nome do Jogo', [validators.DataRequired(), validators.Length(min=1, max=50)])
    categoria = StringField('Nome da Categoria', [validators.DataRequired(), validators.Length(min=1, max=40)])
    console = StringField('Console', [validators.DataRequired(), validators.Length(min=1, max=20)])
    salvar = SubmitField('Salvar')

class UserForm(FlaskForm):
    nickname = StringField('Nickname', [validators.DataRequired(), validators.Length(min=1, max=8)])
    password = PasswordField('Password', [validators.DataRequired(), validators.Length(min=1, max=8)])
    login = SubmitField('Login')

def recuperar_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo
        
    return 'default.png'


def deletar_arquivo(id):
    arquivo = recuperar_imagem(id)
    if arquivo != 'default.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))