import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DB_PATH = ROOT_PATH / 'database' / 'meu_banco.db'

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row

def create_table(conexao):
    cursor.execute('''CREATE TABLE IF NOT EXISTS clientes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name varchar(100) NOT NULL,
        email varchar(150)
    )''')
    conexao.commit()

def insert_data(conexao, cursor, nome, email):
    data = (nome, email)
    cursor.execute('''INSERT INTO clientes (name, email) VALUES (?, ?);''', data)
    conexao.commit()
    
def insert_many_data(conexao, cursor, data):
    cursor.executemany('''INSERT INTO clientes (name, email) VALUES (?, ?);''', data)
    conexao.commit()
    
many_data = [
    ('Belarmino Nicolau Monteiro Simão', 'belarmino.nicolau@bnms.com.br'),
    ('John Doe', 'john.doe@bnms.com.br'),
    ('Jane Smith', 'jane.smith@bnms.com.br')
]

# insert_many_data(conexao, cursor, many_data)

def update_data(conexao, cursor, id, nome, email):
    data = (nome, email, id)
    cursor.execute('''UPDATE clientes SET name = ?, email = ? WHERE id = ?;''', data)
    conexao.commit()

# update_data(conexao, cursor, 1, 'Belarmino Nicolau Monteiro Simão', 'belarmino.nicolau@bnms.com.br')

def delete_data(conexao, cursor, id):
    cursor.execute('''DELETE FROM clientes WHERE id = ?;''', (id,))
    conexao.commit()
    
# delete_data(conexao, cursor, 3)

def select_data(cursor):
    return cursor.execute('''SELECT * FROM clientes ORDER BY name;''')

cleintes = select_data(cursor)
for cliente in cleintes:
    print(dict(cliente))

def select_data_by_id(cursor, id):
    cursor.execute('''SELECT * FROM clientes WHERE id = ?;''', (id,))
    return cursor.fetchone()

# cliente = select_data_by_id(cursor, 2)
# print(dict(cliente))

conexao.close()