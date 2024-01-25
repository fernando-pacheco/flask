from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# CONFIGURAÇÃO
app = Flask(__name__)
app.config.from_pyfile('config.py')
db = SQLAlchemy(app)

from views import *

# INICIANDO A APLICAÇÃO
if __name__ == '__main__':
    app.run(debug=True)