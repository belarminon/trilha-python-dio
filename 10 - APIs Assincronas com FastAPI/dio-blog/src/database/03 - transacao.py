import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DB_PATH = ROOT_PATH / 'database' / 'meu_banco.db'

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row


try:
    
    cursor.execute('''INSERT INTO clientes (name, email) VALUES (?, ?);''', ('Belarmino Nicolau Monteiro Simão', 'belarmino.nicolau@bnms.com.br'))
    cursor.executemany('''INSERT INTO clientes (id, name, email) VALUES (?, ?, ?);''', [(2, 'John Doe', 'john.doe@bnms.com.br')])
    conexao.commit()
    
except Exception as e:
    print(f"An error occurred: {e}")
    conexao.rollback()
    
finally:
    conexao.close()
