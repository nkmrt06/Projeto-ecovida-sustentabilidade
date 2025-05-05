import customtkinter as ctk
from tkinter import messagebox
from connection import verificar_login
from sistema import Sistema

class Login(ctk.CTk):
    def __init__(self):
        super().__init__()

        titulo = ctk.CTkLabel(self, text="♻", font=("Arial", 20))
        titulo.grid(row=1, column=0, columnspan=2, pady=10)
        
        self.title("")
        self.iconbitmap("N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/eco_icon.ico")
        self.resizable(False, False)
        self.geometry("340x300")
        self.grid_columnconfigure((0, 1), weight=1)
      
        ctk.CTkLabel(self, text="Login", font=("Arial", 22)).grid(row=3, column=0, columnspan=2, pady=25)

        ctk.CTkLabel(self, text="E-mail:",font=("Arial",18)).grid(row=5)
        self.email_entry = ctk.CTkEntry(self)
        self.email_entry.grid(row=5, column=1,padx=25,pady=10, sticky="ew")

        ctk.CTkLabel(self, text="Senha:",font=("Arial",18)).grid(row=6)
        self.senha_entry = ctk.CTkEntry(self, show="*")
        self.senha_entry.grid(row=6, column=1,padx=25,pady=10, sticky="ew")

        ctk.CTkButton(self, 
                    text="Logar", 
                    command=self.login,
                    fg_color="#2D6A4F",
                    hover_color="#2D6A4F").grid(row=7, column=0, columnspan=2, pady=20,padx=30,sticky="ew")

    def login(self):
        email = self.email_entry.get() 
        senha = self.senha_entry.get() 
        usuario_id = verificar_login(email, senha)

        if not email or not senha:
            messagebox.showwarning("Campos vazios", "Por favor, preencha todos os campos.")
            return
        if usuario_id:
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.destroy()
            sistema = Sistema(usuario_id)  
            sistema.mainloop()
        else:
            messagebox.showerror("Erro", "Credenciais inválidas.")

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    def conectar_conta(self, usuario_id=None):
        
        self.destroy()
        sistema = Sistema(usuario_id) 
        sistema.mainloop()
