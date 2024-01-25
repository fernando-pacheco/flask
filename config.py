SECRET_KEY = 'estudoflask'
SQLALCHEMY_DATABASE_URI = '{sql}://{user}:{password}@localhost/{db}'.format(
    password='4210*Fernando',
    sql='mysql+mysqlconnector',
    user='root',
    db='jogoteca',
)