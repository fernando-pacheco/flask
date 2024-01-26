import os

SECRET_KEY = 'estudoflask'

UPLOAD_PATH = os.path.abspath(os.path.dirname(__file__)) + '/uploads'
SQLALCHEMY_DATABASE_URI = '{sql}://{user}:{password}@localhost/{db}'.format(
    password='4210*Fernando',
    sql='mysql+mysqlconnector',
    user='root',
    db='jogoteca',
)