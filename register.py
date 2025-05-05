import customtkinter as ctk
from tkinter import messagebox
from connection import registrar_usuario, verificar_login
from login import Login
from sistema import Sistema



class Register(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("")
        self.iconbitmap("N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/eco_icon.ico")
        self.resizable(False, False)

        self.geometry("340x420")
        self.grid_columnconfigure((0, 1), weight=1)
       
        titulo = ctk.CTkLabel(self, text="♻", font=("Arial", 20))
        titulo.grid(row=1, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self, text="Registrar Usuário", font=("Arial", 24)).grid(row=3, column=0, columnspan=2, pady=25)

        ctk.CTkLabel(self, text="Nome:",font=("Arial",18)).grid(row=4)
        self.nome_entry = ctk.CTkEntry(self, font=("Arial", 14))
        self.nome_entry.grid(row=4, column=1,padx=25, pady=10, sticky="ew",columnspan=2)

        ctk.CTkLabel(self, text="E-mail:",font=("Arial",18)).grid(row=5)
        self.email_entry = ctk.CTkEntry(self, font=("Arial", 14))
        self.email_entry.grid(row=5, column=1,padx=25,pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Senha:",font=("Arial",18)).grid(row=6)
        self.senha_entry = ctk.CTkEntry(self, font=("Arial", 14), show="*")
        self.senha_entry.grid(row=6, column=1,padx=25,pady=10, sticky="ew")

        self.button = ctk.CTkButton(
            self, 
            text="Registrar", 
            command=self.button_register,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
            )
        self.button.grid(row=7, column=0, padx=30,pady=10,sticky="ew", columnspan=2)
    
        self.button = ctk.CTkButton(
            self, 
            text="Logar", 
            command=self.abrir_login,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
            )
        self.button.grid(row=8, column=0, padx=30,pady=0,sticky="ew", columnspan=2)

    def button_register(self):
        nome = self.nome_entry.get()
        email = self.email_entry.get()
        senha = self.senha_entry.get()

        if not nome or not email or not senha:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
            return

        sucesso = registrar_usuario(nome, email, senha)
        if sucesso:
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso!")
            self.clear_frame()
            self.abrir_login()
        else:
            messagebox.showerror("Erro", "Erro ao registrar. O e-mail já pode estar cadastrado.")
    
    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def abrir_login(self):
        
        self.destroy()
        login = Login()
        login.mainloop()
