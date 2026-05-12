import tkinter as tk
import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join("DB", "pontofacil.db")


def ver_historico(janela_pai, email):

    janela = tk.Toplevel(janela_pai)
    janela.title("Histórico")
    janela.geometry("420x420")
    janela.resizable(False, False)
    janela.configure(bg="#f3f4f6")

    titulo = tk.Label(
        janela,
        text="HISTÓRICO DE REGISTROS",
        bg="#f3f4f6",
        fg="gray",
        font=("Arial", 10, "bold"),
    )
    titulo.pack(anchor="w", padx=12, pady=(12, 8))

    hoje = datetime.now()
    ano_mes = hoje.strftime("%Y-%m")

    conexao = sqlite3.connect(DB_PATH)
    cursor = conexao.cursor()

    cursor.execute(
        """
        SELECT data, hora
        FROM registros_ponto
        WHERE email = ?
        AND data LIKE ?
        ORDER BY data ASC, hora ASC
    """,
        (email, f"{ano_mes}%"),
    )

    registros = cursor.fetchall()
    conexao.close()

    if not registros:
        tk.Label(
            janela,
            text="Nenhum registro encontrado.",
            bg="#f3f4f6",
            fg="gray",
            font=("Arial", 10),
        ).pack(pady=20)
        return

    registros_por_dia = {}

    for data, hora in registros:

        if data not in registros_por_dia:
            registros_por_dia[data] = []

        if len(registros_por_dia[data]) < 4:
            registros_por_dia[data].append(hora)

    for data in registros_por_dia:

        horarios = registros_por_dia[data]

        while len(horarios) < 4:
            horarios.append("--:--")

        data_formatada = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")

        card = tk.Frame(janela, bg="white", bd=1, relief="solid")
        card.pack(fill="x", padx=10, pady=4)

        tk.Label(
            card,
            text=data_formatada,
            bg="white",
            fg="black",
            font=("Arial", 8, "bold"),
            width=10,
        ).grid(row=0, column=0, padx=4, pady=10)

        for i in range(4):

            tk.Label(
                card,
                text=horarios[i],
                bg="white",
                fg="black",
                font=("Arial", 8),
                width=8,
            ).grid(row=0, column=i + 1, padx=2)
