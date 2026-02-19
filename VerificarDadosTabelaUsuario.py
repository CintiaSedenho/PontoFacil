import sqlite3

conn = sqlite3.connect("pontofacil.db")
cursor = conn.cursor()

cursor.execute("SELECT id, email, senha FROM usuarios")
usuarios = cursor.fetchall()

if usuarios:
    for u in usuarios:
        print(u)
else:
    print("Nenhum usuário cadastrado.")

conn.close()
