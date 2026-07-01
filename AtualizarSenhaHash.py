import datetime
import hashlib
from database import conectar


def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()


def atualizar_senha(email, nova_senha):
    senha_hash = hash_senha(nova_senha)

    conn = conectar()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        UPDATE usuarios
        SET senha = %s
        WHERE email = %s
    """,
        (senha_hash, email),
    )

    conn.commit()
    conn.close()
