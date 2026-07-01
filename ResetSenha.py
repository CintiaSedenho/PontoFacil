import secrets
from datetime import datetime, timedelta
from fastapi import APIRouter, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from passlib.context import CryptContext
from database import get_connection

router = APIRouter()

templates = Jinja2Templates(directory="templates")

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")

# ---------------------------------------------------
# Tela
# ---------------------------------------------------


@router.get("/reset-senha", response_class=HTMLResponse)
async def tela_reset(request: Request):

    return templates.TemplateResponse("reset_senha.html", {"request": request})


# ---------------------------------------------------
# Enviar solicitação
# ---------------------------------------------------


@router.post("/reset-senha")
async def solicitar_reset(email: str = Form(...)):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id
        FROM usuarios
        WHERE email=%s
    """,
        (email,),
    )

    usuario = cursor.fetchone()

    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuário não encontrado.")

    token = secrets.token_urlsafe(32)

    expiracao = datetime.now() + timedelta(minutes=30)

    cursor.execute(
        """
        UPDATE usuarios
        SET reset_token=%s,
            reset_expira=%s
        WHERE email=%s
    """,
        (token, expiracao, email),
    )

    conn.commit()
    conn.close()

    # futuramente enviar por e-mail

    return {"mensagem": "Token gerado.", "token": token}


# ---------------------------------------------------
# Tela nova senha
# ---------------------------------------------------


@router.get("/nova-senha/{token}", response_class=HTMLResponse)
async def tela_nova_senha(request: Request, token: str):

    return templates.TemplateResponse(
        "nova_senha.html", {"request": request, "token": token}
    )


# ---------------------------------------------------
# Alterar senha
# ---------------------------------------------------


@router.post("/nova-senha")
async def alterar_senha(
    token: str = Form(...), senha: str = Form(...), confirmar: str = Form(...)
):

    if senha != confirmar:

        raise HTTPException(status_code=400, detail="As senhas não conferem.")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """

        SELECT id, reset_expira

        FROM usuarios

        WHERE reset_token=%s

    """,
        (token,),
    )

    usuario = cursor.fetchone()

    if usuario is None:

        raise HTTPException(status_code=400, detail="Token inválido.")

    expira = datetime.fromisoformat(usuario[1])

    if datetime.now() > expira:

        raise HTTPException(status_code=400, detail="Token expirado.")

    senha_hash = pwd_context.hash(senha)

    cursor.execute(
        """

        UPDATE usuarios

        SET senha=%s,
            reset_token=NULL,
            reset_expira=NULL

        WHERE id=?

    """,
        (senha_hash, usuario[0]),
    )

    conn.commit()
    conn.close()

    return RedirectResponse(url="/login", status_code=303)
