import mysql.connector
from mysql.connector import errorcode

print('Conectando...')
try:
    cnx = mysql.connector.connect(
        user='root',
        password='4210*Fernando',
        host='localhost',
    )

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

cursor = cnx.cursor()
cursor.execute("DROP DATABASE IF EXISTS `jogoteca`;")
cursor.execute("CREATE DATABASE `jogoteca`;")
cursor.execute("USE `jogoteca`;")

# Cria tabelas
TABLES = {}
TABLES['Jogos'] = ('''
    CREATE TABLE `jogos`(
        id int(11) NOT NULL AUTO_INCREMENT,
        nome varchar(50) NOT NULL,
        categoria varchar(40) NOT NULL,
        console varchar(20) NOT NULL,
        PRIMARY KEY (id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `usuarios` (
        nickname varchar(8) NOT NULL,
        nome varchar(20) NOT NULL,
        senha varchar(8) NOT NULL,
        PRIMARY KEY (nickname)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print("Criando tabela {}: ".format(tabela_nome), end='')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print("Ja existe")
        else:
            print(err.msg)
    else:
        print("OK")

# Inserindo usuarios
usuario_sql = 'INSERT INTO jogoteca.usuarios (nickname, nome, senha) VALUES (%s, %s, %s)'
usuarios = [
    ('luan', 'Luan Marques', 'flask'),
    ('nico', 'Nico', '7a1'),
    ('flask', 'Flask', '9bd'),
    ('fernando', 'Fernando', '4210')
]
cursor.executemany(usuario_sql, usuarios)
cursor.execute('select * from jogoteca.usuarios')
print()
print('Usuários: ')
for user in cursor.fetchall():
    print(user[1])


# Inserindo jogos
jogo_sql = 'INSERT INTO jogoteca.jogos (nome, categoria, console) VALUES (%s, %s, %s)'
jogos = [
    ('God of War 4', 'Ação', 'PS4'),
    ('NBA 2k18', 'Esporte', 'Xbox One'),
    ('Rayman', 'Indie', 'PS4'),
    ('Super Mario Kart', 'Corrida', 'SNES'),
]

cursor.executemany(jogo_sql, jogos)
cursor.execute('select * from jogoteca.jogos')
print()
print('Jogos:')
for jogo in cursor.fetchall():
    print(jogo[1])

cnx.commit()
cursor.close()
cnx.close()