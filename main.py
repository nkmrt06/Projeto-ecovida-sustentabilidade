import customtkinter as ctk
from tkinter import messagebox
from connection import registrar_usuario, verificar_login
from register import Register
from sistema import Sistema
import os
from PIL import Image, ImageTk

ctk.set_appearance_mode("light")  
ctk.set_default_color_theme("green")


# janela principal
class Main(ctk.CTk):
    def __init__(self):
        super().__init__()


        self.title("")
        self.iconbitmap("N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/eco_icon.ico")
        self.resizable(False, False)


        self.geometry("400x190")
        self.background_color = "#000000"
        self.grid_columnconfigure((0, 1), weight=1)
       
        titulo = ctk.CTkLabel(self, text="♻", font=("Arial", 20))
        titulo.grid(row=1, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self, text="Seja bem-vindo(a) ao Eco-vida!", font=("Arial", 24)).grid(row=6, column=0, columnspan=2, pady=20)

    
        self.button = ctk.CTkButton(
            self, 
            text="Entrar", 
            command=self.abrir_register,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F",
            text_color="white",
         )
        self.button.grid(row=7, column=0, padx=20,pady=10,sticky="ew", columnspan=2)

    def abrir_register(self):
        
        self.destroy()
        register = Register()
        register.mainloop()

# Executar o app
if __name__ == "__main__":
    app = Main()
    app.mainloop()
