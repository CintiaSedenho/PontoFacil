import sqlite3

conn = sqlite3.connect("pontofacil.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM registros_ponto")

registros = cursor.fetchall()

for r in registros:
    print(r)

conn.close()
