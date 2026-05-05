import tkinter as tk
from tkinter import messagebox
import sqlite3
from HashSenha import hash_senha

DB_PATH = "DB/pontofacil.db"


def abrir_tela_criar_usuario(root):
    tela = tk.Toplevel(root)
    tela.title("Criar Usuário - Ponto Fácil")
    tela.geometry("420x420")
    tela.resizable(False, False)

    frame = tk.Frame(tela, padx=30, pady=30)
    frame.pack(expand=True)

    titulo = tk.Label(
        frame, text=" Usuário Novo", font=("Arial", 16, "bold"), fg="black"
    )
    titulo.pack(pady=(0, 20))

    tk.Label(frame, text="E-mail").pack(anchor="w")
    entry_email = tk.Entry(frame, width=35)
    entry_email.pack(fill="x", pady=(0, 15))

    tk.Label(frame, text="Senha").pack(anchor="w")
    campo_senha = tk.Frame(frame)
    campo_senha.pack(fill="x", pady=(0, 15))
    entry_senha = tk.Entry(campo_senha, show="*", width=30)
    entry_senha.pack(side="left", fill="x")

    tk.Label(frame, text="Confirmar Senha").pack(
        anchor="w"
    )  # Espaço para o botão de alternar senha
    campo_confirmar = tk.Frame(frame)
    campo_confirmar.pack(fill="x", pady=(0, 15))
    entry_confirmar = tk.Entry(campo_confirmar, show="*", width=30)
    entry_confirmar.pack(side="left", fill="x")

    lbl_msg = tk.Label(frame, text="", fg="red")
    lbl_msg.pack(pady=(5, 0))

    def criar_usuario():
        email = entry_email.get().strip()
        senha = entry_senha.get().strip()
        confirmar = entry_confirmar.get().strip()

        if not email or not senha or not confirmar:
            lbl_msg.config(text="Preencha todos os campos.")
            return

        if senha != confirmar:
            lbl_msg.config(text="As senhas não conferem.")
            return

        try:
            senha_hash = gerar_hash_senha(senha)

            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute(
                "INSERT INTO usuarios (email, senha) VALUES (?, ?)", (email, senha_hash)
            )

            conn.commit()
            conn.close()

            messagebox.showinfo("Sucesso", "Usuário criado com sucesso!")
            tela.destroy()

        except sqlite3.IntegrityError:
            lbl_msg.config(text="Este email já está cadastrado.")

        except Exception as erro:
            lbl_msg.config(text=f"Erro ao criar usuário: {erro}")

    btn_criar = tk.Button(
        frame,
        text="Criar Conta",
        width=10,
        height=1,
        bg="#1a73e8",
        fg="white",
        font=("Arial", 12, "bold"),
        cursor="hand2",
        command=criar_usuario,
    )
    btn_criar.pack(pady=(10, 15))

    btn_voltar = tk.Button(
        frame,
        text="Voltar",
        fg="#1a73e8",
        bd=0,
        cursor="hand2",
        command=lambda: voltar(),
    )
    btn_voltar.pack()

    def voltar():
        tela.destroy()
        root.deiconify()
