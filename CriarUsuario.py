from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
import sqlite3
from passlib.context import CryptContext

router = APIRouter()

DATABASE = "banco/pontofacil.db"

pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto"
)


# ============================
# Modelos
# ============================

class CriarUsuarioRequest(BaseModel):
    nome: str
    email: EmailStr
    senha: str


class CriarUsuarioResponse(BaseModel):
    sucesso: bool
    mensagem: str


# ============================
# Cadastro
# ============================

@router.post(
    "/criar_usuario",
    response_model=CriarUsuarioResponse
)
def criar_usuario(dados: CriarUsuarioRequest):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # verifica se email existe

    cursor.execute("""
        SELECT id
        FROM usuarios
        WHERE email=?
    """, (dados.email,))

    usuario = cursor.fetchone()

    if usuario:

        conn.close()

        raise HTTPException(
            status_code=400,
            detail="E-mail já cadastrado."
        )

    senha_hash = pwd_context.hash(dados.senha)

    cursor.execute("""
        INSERT INTO usuarios
        (
            nome,
            email,
            senha
        )
        VALUES
        (?, ?, ?)
    """,
    (
        dados.nome,
        dados.email,
        senha_hash
    ))

    conn.commit()
    conn.close()

    return CriarUsuarioResponse(
        sucesso=True,
        mensagem="Usuário criado com sucesso."
    )
