import os
from jogoteca import app

def recuperar_imagem(id):
    for nome_arquivo in os.listdir(app.config['UPLOAD_PATH']):
        if f'capa_{id}' in nome_arquivo:
            return nome_arquivo
        
    return 'default.png'


def deletar_arquivo(id):
    arquivo = recuperar_imagem(id)
    if arquivo != 'default.png':
        os.remove(os.path.join(app.config['UPLOAD_PATH'], arquivo))