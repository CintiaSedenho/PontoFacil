import tkinter as tk
from tkinter import messagebox
import hashlib
import sqlite3
import ResetSenha

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

# Função de login (placeholder)
def login():
    email = entry_email.get()
    senha = entry_senha.get()

    if not email or not senha:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")
        return

    senha_hash = hash_senha(senha)
    
    try:    
        conn = sqlite3.connect("pontofacil.db")
        cursor = conn.cursor()
    
        cursor.execute(
        "SELECT * FROM usuarios WHERE email = ? AND senha = ?",
        (email, senha_hash)
        )

        usuario = cursor.fetchone()
        conn.close()
    
        if usuario:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            #chamar a próxima janela ou funcionalidade aqui
        else:
            messagebox.showerror("Erro", "Email ou senha inválidos.")
    except sqlite3.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")

# Função para abrir a janela de redefinição de senha
def abrir_redefinir_senha():
    root.withdraw()          # esconde o login
    ResetSenha.abrir(root)   # abre a tela de reset

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
            
# Janela principal
root = tk.Tk()
root.title("Ponto Fácil - Login")
root.geometry("400x350")
root.resizable(False, False)

# Container
frame = tk.Frame(root, padx=30, pady=30)
frame.pack(expand=True)

# Título
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

# Email
label_email = tk.Label(frame, text="Email")
label_email.pack(anchor="w")

entry_email = tk.Entry(frame, width=35)
entry_email.pack(pady=(0, 15))

# Senha
label_senha = tk.Label(frame, text="Senha")
label_senha.pack(anchor="w")

senha_frame = tk.Frame(frame)
senha_frame.pack(pady=(0, 10), fill="x")

entry_senha = tk.Entry(senha_frame, width=30, show="*")
entry_senha.pack(side="left")

btn_olho = tk.Button(
    senha_frame,
    text="👁️",
    font=("Segoe UI Emoji", 10),
    width=3,
    height=2,
    bd=0,
    relief="flat",
    command=alternar_senha,
    cursor="hand2",
    anchor="center"
)
btn_olho.pack(side="left", padx=6)


# Esqueceu a senha
btn_forgot = tk.Button(
    frame,
    text="Esqueceu a senha?",
    bd=0,
    fg="#1a73e8",
    cursor="hand2",
    command=abrir_redefinir_senha
)
btn_forgot.pack(anchor="e", pady=(0, 20))

# Botão Entrar
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
root.mainloop()        