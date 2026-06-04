import sqlite3
from pathlib import Path

ROOT_PATH = Path(__file__).parent.parent
DB_PATH = ROOT_PATH / 'database' / 'meu_banco.db'

conexao = sqlite3.connect(DB_PATH)
cursor = conexao.cursor()
cursor.row_factory = sqlite3.Row

id_cliente = input("Digite o ID do cliente: ")

# cursor.execute(f'''SELECT * FROM clientes WHERE id = {id_cliente};''') # Vulnerável a injeção de SQL
cursor.execute('''SELECT * FROM clientes WHERE id = ?;''', (id_cliente,))
clientes = cursor.fetchall()
for cliente in clientes:
    print(dict(cliente))    

conexao.close()