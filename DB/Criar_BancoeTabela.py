import sqlite3

conexao = sqlite3.connect("pontofacil.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS registros_ponto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL,
    data TEXT NOT NULL,
    hora TEXT NOT NULL,
    data_hora TEXT NOT NULL
)
""")

conexao.commit()
conexao.close()
