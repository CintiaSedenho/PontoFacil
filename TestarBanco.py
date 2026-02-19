import sqlite3

conn = sqlite3.connect("ponto_facil.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tabelas = cursor.fetchall()

print("Tabelas no banco:")
for tabela in tabelas:
    print("-", tabela[0])

conn.close()
