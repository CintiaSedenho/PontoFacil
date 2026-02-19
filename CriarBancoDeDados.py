import sqlite3
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

conn = sqlite3.connect("pontofacil.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    senha TEXT NOT NULL
)
""")

# Usuário inicial (admin)
email_admin = "admin@pontofacil.com"
senha_admin = hash_senha("123456")

cursor.execute(
    "INSERT OR IGNORE INTO usuarios (email, senha) VALUES (?, ?)",
    (email_admin, senha_admin)
)

conn.commit()
conn.close()

print("Banco criado com sucesso!")
