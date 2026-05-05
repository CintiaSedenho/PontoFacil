import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import sqlite3
import os

DB_PATH = os.path.join("DB", "pontofacil.db")


class TelaApontamento:
    @staticmethod
    def abrir(janela_login, email_logado):
        janela = tk.Toplevel(janela_login)
        janela.title("Ponto Fácil - Apontamento")
        janela.geometry("420x420")
        janela.resizable(False, False)

        # TOPO
        topo = tk.Frame(janela, bg="#0f4c97", height=60)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        lbl_titulo = tk.Label(
            topo,
            text="Registro de Ponto",
            bg="#0f4c97",
            fg="white",
            font=("Arial", 12, "bold"),
        )
        lbl_titulo.pack(side="left", padx=18, pady=16)

        lbl_menu = tk.Label(
            topo, text="☰", bg="#0f4c97", fg="white", font=("Arial", 16, "bold")
        )
        lbl_menu.pack(side="right", padx=18)

        # CONTEÚDO PRINCIPAL
        conteudo = tk.Frame(janela, bg="#f3f4f6")
        conteudo.pack(fill="both", expand=True, padx=18, pady=6)

        lbl_bemvindo = tk.Label(
            conteudo,
            text="Bem vindo!",
            bg="#f3f4f6",
            fg="black",
            font=("Arial", 18, "bold"),
        )
        lbl_bemvindo.pack(anchor="w", pady=(0, 6))

        lbl_colaborador = tk.Label(
            conteudo, text="Colaborador", bg="#f3f4f6", fg="gray", font=("Arial", 11)
        )
        lbl_colaborador.pack(anchor="w", pady=(0, 16))

        # CARD LOGO ABAIXO DO COLABORADOR
        card = tk.Frame(conteudo, bg="white", bd=1, relief="solid")
        card.pack(fill="x", pady=(0, 0))

        lbl_hora = tk.Label(
            card, text="00:00:00", bg="white", fg="black", font=("Arial", 20, "bold")
        )
        lbl_hora.pack(pady=(22, 8))

        lbl_data = tk.Label(card, text="", bg="white", fg="gray", font=("Arial", 11))
        lbl_data.pack()

        def atualizar_relogio():
            agora = datetime.now()
            lbl_hora.config(text=agora.strftime("%H:%M:%S"))
            lbl_data.config(text=agora.strftime("%d/%m/%Y"))
            janela.after(1000, atualizar_relogio)

        atualizar_relogio()

        btn_registrar = tk.Button(
            card,
            text="Registrar ponto agora",
            bg="#1f73ea",
            fg="white",
            font=("Arial", 12, "bold"),
            relief="flat",
            bd=0,
            padx=10,
            pady=12,
            cursor="hand2",
        )
        btn_registrar.pack(fill="x", padx=16, pady=20)

        def registrar_ponto():
            agora = datetime.now()
            data = agora.strftime("%Y-%m-%d")
            hora = agora.strftime("%H:%M:%S")

            try:
                conn = sqlite3.connect("DB/pontofacil.db")
                cursor = conn.cursor()

                cursor.execute("""CREATE TABLE IF NOT EXISTS registros_ponto (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT NOT NULL,
                        data TEXT NOT NULL,
                        hora TEXT NOT NULL,
                        criado_em TEXT NOT NULL
                    )""")
                cursor.execute(
                    """INSERT INTO registros_ponto (email, data, hora, data_hora) VALUES (?, ?, ?, ?)""",
                    (email_logado, data, hora, datetime.now()),
                )

                conn.commit()
                conn.close()

                messagebox.showinfo("Sucesso", "Ponto registrado com sucesso!")

            except Exception as erro:
                messagebox.showerror("Erro", f"Erro ao registrar ponto: {erro}")

        btn_registrar.config(command=registrar_ponto)

        def abrir(root, email_logado):
            pass
