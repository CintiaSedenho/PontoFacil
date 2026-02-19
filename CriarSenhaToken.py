import tkinter as tk
from tkinter import messagebox
import sqlite3
import uuid
import datetime
import smtplib
from email.mime.text import MIMEText

def enviar_email(destinatario, token):

    remetente = "seuemail@gmail.com"
    senha_app = "SENHA_DE_APLICATIVO"

    link = f"http://localhost/reset?token={token}"

    corpo = f"""
    Olá,

    Clique no link abaixo para redefinir sua senha:

    {link}

    Este link expira em 60 minutos.
    """

    msg = MIMEText(corpo)
    msg["Subject"] = "Redefinição de Senha"
    msg["From"] = remetente
    msg["To"] = destinatario

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(remetente, senha_app)
            server.send_message(msg)

    except Exception as e:
        print("Erro ao enviar e-mail:", e)
        raise
    
def abrir_tela_reset():
    def enviar_link():
        email = entry_email.get()

        if not email:
            messagebox.showwarning("Atenção", "Informe o e-mail")
            return

        token = str(uuid.uuid4())
        expira = datetime.datetime.now() + datetime.timedelta(minutes=15)

        conn = sqlite3.connect("pontofacil.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO password_reset (email, token, expira_em)
            VALUES (?, ?, ?)
        """, (email, token, expira.isoformat()))

        conn.commit()
        conn.close()

    try:
    enviar_email(email, token)
    messagebox.showinfo("Sucesso", "E-mail enviado com sucesso!")
    reset.destroy()
    
    except Exception:
    messagebox.showerror("Erro", "Não foi possível enviar o e-mail.")
    return
        
    reset = tk.Toplevel()
    reset.title("Ponto Fácil - Redefinir senha")
    reset.geometry("360x260")

    tk.Label(reset, text="Redefinir senha", font=("Arial", 16)).pack(pady=10)
    tk.Label(reset, text="Enviaremos um link para seu e-mail").pack()

    tk.Label(reset, text="Email").pack(pady=5)
    entry_email = tk.Entry(reset, width=30)
    entry_email.pack()

    tk.Button(
        reset,
        text="Redefinir senha",
        bg="#2f80ed",
        fg="white",
        command=enviar_link
    ).pack(pady=20)
