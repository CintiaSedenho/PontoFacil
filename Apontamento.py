from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from database import conectar

from auth import get_current_user

router = APIRouter(prefix="/apontamento", tags=["Apontamento"])

DATABASE = "database/pontofacil.db"


class RegistroPonto(BaseModel):
    tipo: str


def conectar():
    conn = conectar()
    cursor = conn.cursor(dictionary=True)
    return conn


@router.post("/")
def registrar_ponto(registro: RegistroPonto, usuario=Depends(get_current_user)):

    tipos_validos = ["ENTRADA", "SAIDA_ALMOCO", "RETORNO_ALMOCO", "SAIDA"]

    if registro.tipo not in tipos_validos:
        raise HTTPException(status_code=400, detail="Tipo de registro inválido.")

    conn = conectar()
    cursor = conn.cursor()

    data = datetime.now().strftime("%Y-%m-%d")
    hora = datetime.now().strftime("%H:%M:%S")

    cursor.execute(
        """

        INSERT INTO apontamentos
        (
            usuario_id,
            data,
            hora,
            tipo
        )

        VALUES
        (
            %s, %s, %s, %s
        )

    """,
        (usuario["id"], data, hora, registro.tipo),
    )

    conn.commit()
    conn.close()

    return {
        "mensagem": "Ponto registrado com sucesso.",
        "tipo": registro.tipo,
        "hora": hora,
    }


@router.get("/hoje")
def listar_pontos_hoje(usuario=Depends(get_current_user)):

    conn = conectar()
    cursor = conn.cursor()

    hoje = datetime.now().strftime("%Y-%m-%d")

    cursor.execute(
        """

        SELECT
            hora,
            tipo

        FROM apontamentos

        WHERE usuario_id=%s
        AND data=%s

        ORDER BY hora

    """,
        (usuario["id"], hoje),
    )

    registros = cursor.fetchall()

    conn.close()

    return registros


@router.get("/historico")
def historico(usuario=Depends(get_current_user)):

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT

            data,
            hora,
            tipo

        FROM apontamentos

        WHERE usuario_id=%s

        ORDER BY data DESC, hora DESC

    """,
        (usuario["id"],),
    )

    dados = cursor.fetchall()

    conn.close()

    return dados

    conn.close()

    return dados
