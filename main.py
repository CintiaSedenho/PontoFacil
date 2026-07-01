from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from routes.reset_senha import router as reset_router
import hashlib
import os

import ResetSenha
import CriarUsuario
from Apontamento import TelaApontamento
from HashSenha import hash_senha, verificar_senha

app.include_router(reset_router)

# Configuração do caminho do banco de dados
DB_PATH = os.path.join("DB", "pontofacil.db")
app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")


class LoginRequest(BaseModel):
    email: str
    senha: str


@app.post("/login")
def login(login_data: LoginRequest):
    email = login_data.email.strip()
    senha = login_data.senha.strip()

    lbl_msg.config(text="")
    lbl_error.config(text="")

    if not email or not senha:
        lbl_msg.config(text="Preencha todos os campos.")
        return

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, email, senha FROM usuarios WHERE email = ?", (email,)
        )

        usuario = cursor.fetchone()
        conn.close()

        if not usuario:
            lbl_msg.config(text="E-mail ou senha inválidos.")
            return

        senha_hash = usuario[2]

        # verifica argon2
        if senha_hash.startswith("$argon2"):
            if verificar_senha(senha, senha_hash):
                TelaApontamento.abrir(root, email)
                root.withdraw()
            else:
                lbl_msg.config(text="Senha incorreta.")
            return

        # verifica SHA-256 antigo
        senha_sha256 = hashlib.sha256(senha.encode()).hexdigest()

        if senha_sha256 == senha_hash:
            novo_hash = hash_senha(senha)  # MIGRA automaticamente

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET senha = ? WHERE email = ?", (novo_hash, email)
            )
            conn.commit()
            conn.close()

            TelaApontamento.abrir(root, email)
            root.withdraw()
        else:
            lbl_msg.config(text="Senha incorreta.")

    except Exception as e:
        lbl_error.config(text=f"Erro: {e}")


@app.get("/reset-senha", response_class=HTMLResponse)
async def tela_reset_senha(request: Request):
    return templates.TemplateResponse(
        "reset_senha.html", {"request": request, "mensagem": "", "erro": ""}
    )


senha_visivel = False


def alternar_senha():
    global senha_visivel
    if senha_visivel:
        entry_senha.config(show="*")
        btn_olho.config(text="👁️")
        senha_visivel = False
    else:
        entry_senha.config(show="")
        senha_visivel = True


@app.post("/reset-senha", response_class=HTMLResponse)
async def reset_senha(request: Request, email: str = Form(...)):

    if email == "":
        return templates.TemplateResponse(
            "reset_senha.html",
            {"request": request, "erro": "Informe o e-mail.", "mensagem": ""},
        )

    # Aqui futuramente:
    # gerar token
    # salvar token no banco
    # enviar e-mail

    return templates.TemplateResponse(
        "reset_senha.html",
        {"request": request, "mensagem": "E-mail enviado com sucesso.", "erro": ""},
    )
