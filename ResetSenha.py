import tkinter as tk
from tkinter import messagebox

def abrir(janela_login):
    janela = tk.Toplevel(janela_login)
    janela.title("Ponto Fácil - Redefinir Senha")
    janela.geometry("420x420")
    janela.resizable(False, False)
    janela.configure(bg="#f5f6f8")

    def cancelar():
        janela.destroy()
        janela_login.deiconify()

    def redefinir():
        email = entry_email.get()

        if not email:
            messagebox.showwarning("Atenção", "Informe seu e-mail.")
            return

        # Aqui futuramente entra a lógica (token + banco + email)
        lbl_sucesso.config(text="✔ E-mail enviado com sucesso")
        lbl_sucesso.pack(pady=(15, 0))

    # Container central (card)
    card = tk.Frame(janela, bg="white", bd=0)
    card.place(relx=0.5, rely=0.45, anchor="center", width=360, height=260)

    # Título
    tk.Label(
        card,
        text="Redefinir senha",
        font=("Arial", 14, "bold"),
        bg="white"
    ).pack(pady=(20, 5))

    # Subtítulo
    tk.Label(
        card,
        text="Enviaremos um link para seu e-mail",
        font=("Arial", 9),
        fg="gray",
        bg="white"
    ).pack(pady=(0, 15))

    # Email label
    tk.Label(
        card,   
        anchor="w",
        bg="white"
    ).pack(fill="x", padx=25)

    # Email entry
    entry_email = tk.Entry(card, width=35)
    entry_email.pack(padx=25, pady=(5, 20))

    # Botões
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(pady=(5, 0))

    tk.Button(
        btn_frame,
        text="Cancelar",
        width=14,
        command=cancelar
    ).pack(side="left", padx=5)

    tk.Button(
        btn_frame,
        text="Redefinir senha",
        width=18,
        bg="#1a73e8",
        fg="white",
        command=redefinir
    ).pack(side="left", padx=5)

    # Mensagem de sucesso (oculta inicialmente)
    lbl_sucesso = tk.Label(
        janela,
        text="",
        fg="green",
        bg="#f5f6f8",
        font=("Arial", 10, "bold")
    )
