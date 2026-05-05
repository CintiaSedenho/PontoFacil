import sqlite3
from datetime import datetime
from tkinter import messagebox


def registrar_ponto(email_usuario):
    agora = datetime.now()

    data = agora.strftime("%d/%m/%Y")
    hora = agora.strftime("%H:%M:%S")
    data_hora = agora.strftime("%Y-%m-%d %H:%M:%S")

    conexao = sqlite3.connect("DB/pontofacil.db")
    cursor = conexao.cursor()

    cursor.execute(
        """
        INSERT INTO registros_ponto (email, data, hora, data_hora)
        VALUES (?, ?, ?, ?)
    """,
        (email_usuario, data, hora, data_hora),
    )

    conexao.commit()
    conexao.close()

    messagebox.showinfo("Sucesso", "Ponto registrado com sucesso!")
