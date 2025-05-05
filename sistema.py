import customtkinter as ctk
from tkinter import messagebox
from connection import registrar_habito, grafico_habitos, limpar_dados, zerar_tempos, recomendar_habito, calcular_pontuacao, exportar_para_pdf
import webbrowser
import subprocess
import os
import streamlit as st
import importlib.util
import sys

site_path = r"N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/site.py"

spec = importlib.util.spec_from_file_location("site", site_path)
site = importlib.util.module_from_spec(spec)
sys.modules["site"] = site
spec.loader.exec_module(site)

from site import mostrar_dicas_sustentaveis
class Sistema(ctk.CTk):
    def __init__(self, usuario_id):
        super().__init__()
        self.usuario_id = usuario_id 

        self.title("")
        self.iconbitmap("N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/eco_icon.ico")
        self.resizable(False, False)
        self.geometry("600x700")
        self.grid_columnconfigure((0, 1), weight=1)

        
        titulo = ctk.CTkLabel(self, text="♻ Eco-vida", font=("Arial", 24, "bold"))
        titulo.grid(row=0, column=0, columnspan=2, pady=10)

        ctk.CTkLabel(self, text="Sistema de Sustentabilidade", font=("Arial", 18)).grid(row=1, column=0, columnspan=2, pady=10)

       
        frame_registro = ctk.CTkFrame(self)
        frame_registro.grid(row=2, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        frame_registro.grid_columnconfigure(1, weight=1)

        # Nome do hábito
        ctk.CTkLabel(frame_registro, text="Nome do hábito:", font=("Arial", 14)).grid(row=0, column=0, padx=10, pady=5, sticky="w")
        self.entrada_habito = ctk.CTkEntry(frame_registro, width=200)
        self.entrada_habito.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Categoria
        ctk.CTkLabel(frame_registro, text="Categoria:", font=("Arial", 14)).grid(row=1, column=0, padx=10, pady=5, sticky="w")
        categorias = ["Água", "Energia", "Transporte", "Resíduos"]
        self.categoria_var = ctk.StringVar(value=categorias[0])
        self.combo_categoria = ctk.CTkComboBox(frame_registro, values=categorias, variable=self.categoria_var, width=200)
        self.combo_categoria.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

        # Quantidade
        ctk.CTkLabel(frame_registro, text="Quantidade:", font=("Arial", 14)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.entrada_quantidade = ctk.CTkEntry(frame_registro, width=200)
        self.entrada_quantidade.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        # Unidade
        ctk.CTkLabel(frame_registro, text="Unidade:", font=("Arial", 14)).grid(row=3, column=0, padx=10, pady=5, sticky="w")
        unidades = ["litros", "kWh", "km", "kg"]
        self.unidade_var = ctk.StringVar(value=unidades[0])
        self.combo_unidade = ctk.CTkComboBox(frame_registro, values=unidades, variable=self.unidade_var, width=200)
        self.combo_unidade.grid(row=3, column=1, padx=10, pady=5, sticky="ew")

        # Mensagem de feedback
        self.mensagem = ctk.CTkLabel(self, text="", text_color="green", font=("Arial", 12))
        self.mensagem.grid(row=3, column=0, columnspan=2, pady=5)

        # Botões principais
        frame_botoes = ctk.CTkFrame(self)
        frame_botoes.grid(row=4, column=0, columnspan=2, padx=20, pady=10, sticky="ew")
        frame_botoes.grid_columnconfigure((0, 1), weight=1)

        
        ctk.CTkButton(
            frame_botoes, 
            text="Registrar Hábito", 
            command=self.registrar,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
        ).grid(row=0, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            frame_botoes, 
            text="📊 Ver Gráfico", 
            command=lambda: grafico_habitos(self.usuario_id),
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
        ).grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        
        ctk.CTkButton(
            frame_botoes, 
            text="📌 Ver Recomendação", 
            command=self.recomendar,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
        ).grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            frame_botoes, 
            text="💯 Calcular Pontuação", 
            command=self.pontuacao,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
        ).grid(row=1, column=1, padx=10, pady=5, sticky="ew")

       
        ctk.CTkButton(
            frame_botoes, 
            text="📄 Exportar PDF", 
            command=self.exportar_pdf,
            fg_color="#2D6A4F",
            hover_color="#2D6A4F"
        ).grid(row=2, column=0, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            frame_botoes, 
            text="❌ Limpar Dados", 
            command=self.confirmar_limpar,
            fg_color="#771212",
            hover_color="#7F1D1D"
        ).grid(row=2, column=1, padx=10, pady=5, sticky="ew")

        ctk.CTkButton(
            frame_botoes, 
            text="Deslogar", 
            command=self.abrir_login,
            fg_color="#771212",
            hover_color="#7F1D1D"
        ).grid(row=3, column=0, padx=10, pady=5, sticky="ew", columnspan="2")

        ctk.CTkButton(
            frame_botoes,
            text="🌐 Acessar Dicas Sustentáveis",
            command=self.abrir_dicas,
            fg_color="#1D4ED8",
            hover_color="#2563EB"
        ).grid(row=4, column=0, padx=10, pady=5, sticky="ew", columnspan=2)


        
        self.status_bar = ctk.CTkLabel(self, text=" ", anchor="w", text_color="#6B7280", font=("Arial", 12))
        self.status_bar.grid(row=5, column=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

    def registrar(self):
        nome = self.entrada_habito.get()
        categoria = self.categoria_var.get()
        unidade = self.unidade_var.get()
        
        try:
            quantidade = float(self.entrada_quantidade.get())
            
            if nome and quantidade > 0:
                sucesso = registrar_habito(self.usuario_id, nome, quantidade, unidade, categoria)
                if sucesso:
                    self.mensagem.configure(text="✅ Hábito registrado com sucesso!", text_color="green")
                    self.entrada_habito.delete(0, 'end')
                    self.entrada_quantidade.delete(0, 'end')
                    self.status_bar.configure(text=f"Hábito '{nome}' registrado: {quantidade} {unidade} em {categoria}")
                else:
                    self.mensagem.configure(text="❌ Erro ao registrar o hábito", text_color="red")
            else:
                self.mensagem.configure(text="❌ Preencha o nome e uma quantidade válida", text_color="red")
        except ValueError:
            self.mensagem.configure(text="❌ A quantidade deve ser um número", text_color="red")

    def recomendar(self):
        try:
            recomendacao = recomendar_habito(self.usuario_id)
            messagebox.showinfo("Recomendação de Sustentabilidade", recomendacao)
            self.status_bar.configure(text="Recomendação exibida")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao gerar recomendação: {str(e)}")
            self.status_bar.configure(text="Erro ao gerar recomendação")

    def pontuacao(self):
        try:
            pontos = calcular_pontuacao(self.usuario_id)
            if pontos is not None:
                messagebox.showinfo("Pontuação Total", 
                                f"🌱 Sua pontuação sustentável: {pontos} pontos\n\n" +
                                "Quanto mais você economiza nos recursos, maior sua pontuação!\n" +
                                "Continue registrando seus hábitos diários para ver seu progresso.")
                self.status_bar.configure(text=f"Pontuação calculada: {pontos} pontos")
            else:
                messagebox.showinfo("Sem Pontuação", 
                                "Você ainda não possui registros suficientes para calcular sua pontuação.\n" +
                                "Registre seus hábitos diários para começar a pontuar!")
                self.status_bar.configure(text="Sem pontuação calculada")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao calcular pontuação: {str(e)}")
            self.status_bar.configure(text="Erro ao calcular pontuação")

    def confirmar_limpar(self):
        resposta = messagebox.askyesno("Confirmar", "Tem certeza que deseja limpar todos os dados? Esta ação não pode ser desfeita.")
        if resposta:
            self.limpar()

    def limpar(self):
        try:
            if limpar_dados():
                messagebox.showinfo("Limpeza", "📂 Todos os registros foram apagados.")
                self.status_bar.configure(text="Dados limpos")
            else:
                messagebox.showerror("Erro", "Não foi possível limpar os dados.")
                self.status_bar.configure(text="Erro ao limpar dados")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao limpar dados: {str(e)}")
            self.status_bar.configure(text="Erro ao limpar dados")

    def exportar_pdf(self):
        try:
            resultado = exportar_para_pdf(self.usuario_id)
            if resultado:
                messagebox.showinfo("PDF Gerado", "📄 Relatório PDF gerado com sucesso!")
                self.status_bar.configure(text="PDF exportado com sucesso")
            else:
                messagebox.showerror("Erro", "❌ Não foi possível gerar o relatório PDF. Verifique se você possui registros suficientes.")
                self.status_bar.configure(text="Erro ao exportar PDF")
        except Exception as e:
            messagebox.showerror("Erro", f"❌ Erro ao gerar o PDF: {str(e)}")
            self.status_bar.configure(text="Erro ao exportar PDF")

    def abrir_login(self):
    
        from login import Login  
        self.destroy()
        login = Login()
        login.mainloop()

    def abrir_dicas(self):
        try:
            
            site_path = r"N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/site.py"
            
            
            subprocess.Popen([sys.executable, "-m", "streamlit", "run", site_path])

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir dicas sustentáveis: {str(e)}")
