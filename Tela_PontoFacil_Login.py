import tkinter as tk
from tkinter import messagebox
import sqlite3
import TelaResetSenha
from TelaApontamento import TelaApontamento
from HashSenha import hash_senha, verificar_senha

def login():
    email = entry_email.get().strip()
    senha = entry_senha.get()

    lbl_msg.config(text="")
    lbl_error.config(text="")

    if not email or not senha:
        lbl_msg.config(text="Preencha todos os campos.")
        return

    try:
        conn = sqlite3.connect(r"DB\pontofacil.db")
        cursor = conn.cursor()

        cursor.execute(
            "SELECT id, email, senha FROM usuarios WHERE email = ?",
            (email,)
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
                TelaApontamento.abrir(root)
                root.withdraw()
            else:
                lbl_msg.config(text="Senha incorreta.")
            return

        # verifica SHA-256 antigo
        senha_sha256 = hashlib.sha256(senha.encode()).hexdigest()

        if senha_sha256 == senha_hash:            
            novo_hash = hash_senha(senha) # MIGRA automaticamente

            conn = sqlite3.connect(r"DB\pontofacil.db")
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE usuarios SET senha = ? WHERE email = ?",
                (novo_hash, email)
            )
            conn.commit()
            conn.close()

            TelaApontamento.abrir(root)
            root.withdraw()
        else:
            lbl_msgm.config(text="Senha incorreta.")

    except Exception as e:
        lbl_error.config(text=f"Erro: {e}")

def abrir_redefinir_senha():
    root.withdraw()
    TelaResetSenha.abrir(root)  

senha_visivel = False

def alternar_senha():
    global senha_visivel
    if senha_visivel:
        entry_senha.config(show="*")
        btn_olho.config(text="👁️")
        senha_visivel = False
    else:
        entry_senha.config(show="")
        btn_olho.config(text="🙈")
        senha_visivel = True
            
root = tk.Tk()
root.title("Ponto Fácil - Login")
root.geometry("420x420")
root.resizable(False, False)

frame = tk.Frame(root, padx=30, pady=30)
frame.pack(expand=True)

label_title = tk.Label(
    frame,
    text="Ponto Fácil",
    font=("Arial", 20, "bold")
)
label_title.pack(pady=(0, 10))

label_subtitle = tk.Label(
    frame,
    text="Sistema de Controle de Ponto",
    font=("Arial", 10),
    fg="gray"
)
label_subtitle.pack(pady=(0, 20))

tk.Label(frame, text="E-mail").pack(anchor="w")

entry_email = tk.Entry(frame)
entry_email.pack(fill="x", pady=(0, 15))

tk.Label(frame, text="Senha").pack(anchor="w")

campo_senha = tk.Frame(frame)
campo_senha.pack(fill="x", pady=(0, 15))

entry_senha = tk.Entry(campo_senha, show="*")
entry_senha.pack(side="left", fill="x", expand=True)

btn_olho = tk.Button(
    campo_senha,
    text="👁️",
    font=("Segoe UI Emoji", 9),
    width=2,
    bd=0,
    relief="flat",
    command=alternar_senha,
    cursor="hand2",
    pady=0
)
btn_olho.pack(side="left", padx=(6, 0))

btn_forgot = tk.Button(
    frame,
    text="Esqueceu a senha?",
    bd=0,
    fg="#1a73e8",
    cursor="hand2",
    command=abrir_redefinir_senha
)
btn_forgot.pack(anchor="e", pady=(0, 20))

btn_login = tk.Button(
    frame,
    text="Entrar",
    width=30,
    height=2,
    bg="#1a73e8",
    fg="white",
    command=login
)
btn_login.pack()

lbl_mensagem = tk.Label(frame, text="", fg="red")
lbl_mensagem.pack(pady=(5, 0))

lbl_error = tk.Label(frame, text="", fg="red")
lbl_error.pack(pady=(5, 0))

def abrir_TelaCriarUsuario():
    root.withdraw()
    TelaCriarUsuario.abrir(root)

btn_newuser = tk.Button(
    frame,
    text="Criar uma nova conta",
    bd=0,
    fg="#1a73e8",
    cursor="hand2",
    command=abrir_TelaCriarUsuario
)
btn_newuser.pack(pady=(8,0))

root.mainloop()       
btn_login.pack()
root.mainloop()        
