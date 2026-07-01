from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

SECRET_KEY = "****************************"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15

pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


def verificar_senha(senha, senha_hash):
    return pwd_context.verify(senha, senha_hash)


def gerar_hash(senha):
    return pwd_context.hash(senha)


def criar_token(dados: dict):
    dados_token = dados.copy()

    expira = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dados_token.update({"exp": expira})

    return jwt.encode(dados_token, SECRET_KEY, algorithm=ALGORITHM)
