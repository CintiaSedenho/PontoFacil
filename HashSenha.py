from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["argon2"],
    argon2__type="ID",
    deprecated="auto"
)

def hash_senha(senha):
    return pwd_context.hash(senha)

def verificar_senha(senha, hash_senha_banco):
    return pwd_context.verify(senha, hash_senha_banco)