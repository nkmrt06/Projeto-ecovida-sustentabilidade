import bcrypt
import sqlite3
import mysql.connector
from datetime import datetime
import matplotlib.pyplot as plt
from fpdf import FPDF
import os
from io import BytesIO

def conectar():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="1731",
            database="ecovida"
        )
        if conn.is_connected():
            print("Conexão bem-sucedida com o banco de dados.")
            return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

def registrar_usuario(nome, email, senha):
    conn = conectar()
    if conn is None:
        return False
    
    cursor = conn.cursor()
    
    
    cursor.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
    if cursor.fetchone():
        conn.close()
        return False
    
    senha_criptografada = bcrypt.hashpw(senha.encode('utf-8'), bcrypt.gensalt())
    
    
    cursor.execute("""
        INSERT INTO usuarios (nome, email, senha)
        VALUES (%s, %s, %s)
    """, (nome, email, senha_criptografada.decode()))
    
    conn.commit()
    conn.close()
    return True

# Função para verificar o login do usuário
def verificar_login(email, senha):
    conn = conectar()
    if conn is None:
        return None
    
    cursor = conn.cursor()
    cursor.execute("SELECT id, senha FROM usuarios WHERE email = %s", (email,))
    resultado = cursor.fetchone()
    conn.close()

    if resultado:
        usuario_id, senha_armazenada = resultado
        if bcrypt.checkpw(senha.encode('utf-8'), senha_armazenada.encode('utf-8')):
            return usuario_id
    return None

# Função para registrar hábitos no banco de dados
def registrar_habito(usuario_id, nome_habito, quantidade, unidade, categoria):
    conn = conectar()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()
        
        
        cursor.execute("""
            SELECT id FROM habitos WHERE nome = %s AND unidade = %s AND categoria = %s
            """, (nome_habito, unidade, categoria))
        habito = cursor.fetchone()

        if habito:
            habito_id = habito[0]
        else:
            
            cursor.execute("""
                INSERT INTO habitos (nome, unidade, categoria)
                VALUES (%s, %s, %s)
            """, (nome_habito, unidade, categoria))
            conn.commit()
            cursor.execute("SELECT LAST_INSERT_ID()")
            habito_id = cursor.fetchone()[0]

        
        data = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
            INSERT INTO registros (usuario_id, habito_id, quantidade, data_registro)
            VALUES (%s, %s, %s, %s)
        """, (usuario_id, habito_id, quantidade, data))
        conn.commit()
        
        conn.close()
        return True
    except Exception as e:
        print(f"Erro ao registrar hábito: {e}")
        if conn and conn.is_connected():
            conn.close()
        return False

def calcular_pontuacao(usuario_id):
    conn = conectar()
    if conn is None:
        return 0
        
    try:
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT COUNT(*) FROM registros WHERE usuario_id = %s
        """, (usuario_id,))
        count = cursor.fetchone()[0]
        
        if count == 0:
            conn.close()
            return 0  
            
        cursor.execute("""
            SELECT h.categoria, h.nome, SUM(r.quantidade) as total
            FROM registros r
            JOIN habitos h ON r.habito_id = h.id
            WHERE r.usuario_id = %s
            GROUP BY h.categoria, h.nome;
        """, (usuario_id,))
        resultados = cursor.fetchall()
        conn.close()

        pontuacao = 0
        # Pesos invertidos para premiar economia: quanto menor o consumo, maior a pontuação
        pesos = {
            'água': 5.0,     
            'energia': 4.0,  
            'transporte': 3.0, 
            'resíduos': 2.0   
        }
        
        # Valores de referência (consumo médio por categoria)
        referencias = {
            'água': 150.0,    
            'energia': 10.0,  
            'transporte': 30.0, 
            'resíduos': 2.0    
        }

        for categoria, nome, quantidade in resultados:
            if quantidade is None:
                continue 
                
            try:
                quantidade = float(quantidade)  
            except (ValueError, TypeError):
                continue  
                
            categoria = categoria.lower() if categoria else "outros"
            if categoria in pesos and categoria in referencias:
                
                if quantidade < referencias[categoria]:
                    
                    economia = (referencias[categoria] - quantidade) / referencias[categoria]
                    pontos = economia * 100 * pesos[categoria]
                    pontuacao += pontos
                else:
                    
                    excesso = (quantidade - referencias[categoria]) / referencias[categoria]
                    pontos = -excesso * 10 * pesos[categoria]  
                    pontuacao += pontos

        
        return max(round(pontuacao, 2), 0)
        
    except Exception as e:
        print(f"Erro ao calcular pontuação: {e}")
        if conn and conn.is_connected():
            conn.close()
        return 0
    

def grafico_habitos(usuario_id):
    conn = conectar()
    if conn is None:
        return
        
    cursor = conn.cursor()
    cursor.execute("""
        SELECT h.categoria, SUM(r.quantidade) as total
        FROM registros r
        JOIN habitos h ON r.habito_id = h.id
        WHERE r.usuario_id = %s
        GROUP BY h.categoria;
    """, (usuario_id,))
    resultados = cursor.fetchall()
    conn.close()

    if not resultados:
        print("Nenhum dado para exibir.")
        return

    categorias = [categoria for categoria, _ in resultados]
    quantidades = [float(quantidade) for _, quantidade in resultados]

    plt.figure(figsize=(10, 6))
    plt.bar(categorias, quantidades, color='mediumseagreen')
    plt.xlabel("Categoria")
    plt.ylabel("Quantidade Total")
    plt.title("Consumo por Categoria")
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # Calcular pontuação baseada nos dados do gráfico
    pontuacao = calcular_pontuacao(usuario_id)
    print(f"Pontuação de Sustentabilidade: {pontuacao}")

def exportar_para_pdf(usuario_id):
    try:
        
        conn = conectar()
        if conn is None:
            return False
            
        cursor = conn.cursor()
        cursor.execute("SELECT nome, email FROM usuarios WHERE id = %s", (usuario_id,))
        usuario = cursor.fetchone()
        
        if not usuario:
            print(f"Usuário ID {usuario_id} não encontrado.")
            conn.close()
            return False
            
        nome_usuario, email_usuario = usuario
        
        
        cursor.execute("""
            SELECT h.nome, h.categoria, h.unidade, r.quantidade, r.data_registro
            FROM registros r
            JOIN habitos h ON r.habito_id = h.id
            WHERE r.usuario_id = %s
            ORDER BY r.data_registro DESC;
        """, (usuario_id,))
        registros = cursor.fetchall()
        
        if not registros:
            print("Nenhum registro encontrado para este usuário.")
            conn.close()
            return False

        
        pdf = FPDF()
        pdf.add_page()
        
        
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, "Relatório de Sustentabilidade", ln=True, align="C")
        
        pdf.set_font("Arial", "", 12)
        pdf.cell(0, 10, f"Usuário: {nome_usuario} ({email_usuario})", ln=True)
        pdf.cell(0, 10, f"Data: {datetime.now().strftime('%d/%m/%Y')}", ln=True)
        pdf.ln(5)
        
        # Tabela de registros
        pdf.set_font("Arial", "B", 12)
        pdf.cell(50, 10, "Hábito", border=1)
        pdf.cell(40, 10, "Categoria", border=1)
        pdf.cell(30, 10, "Quantidade", border=1)
        pdf.cell(30, 10, "Unidade", border=1)
        pdf.cell(40, 10, "Data", border=1)
        pdf.ln()
        
        pdf.set_font("Arial", "", 10)
        for nome, categoria, unidade, quantidade, data in registros:
            try:
                data_formatada = data.strftime("%d/%m/%Y") if hasattr(data, 'strftime') else str(data)
                pdf.cell(50, 10, str(nome)[:25], border=1)
                pdf.cell(40, 10, str(categoria)[:20], border=1)
                pdf.cell(30, 10, str(quantidade), border=1)
                pdf.cell(30, 10, str(unidade)[:15], border=1)
                pdf.cell(40, 10, data_formatada, border=1)
                pdf.ln()
            except Exception as e:
                print(f"Erro ao adicionar registro ao PDF: {e}")
                continue
        
        
        pdf.ln(10)
        pontuacao = calcular_pontuacao(usuario_id)
        pdf.set_font("Arial", "B", 14)
        pdf.cell(0, 10, f"Pontuação de Sustentabilidade: {pontuacao}", ln=True)
        
        
        cursor.execute("""
            SELECT h.categoria, SUM(r.quantidade) as total
            FROM registros r
            JOIN habitos h ON r.habito_id = h.id
            WHERE r.usuario_id = %s
            GROUP BY h.categoria;
        """, (usuario_id,))
        dados_grafico = cursor.fetchall()
        conn.close()
        
        # Criar gráfico
        if dados_grafico:
            try:
                categorias = [categoria for categoria, _ in dados_grafico]
                quantidades = [float(quantidade) for _, quantidade in dados_grafico]
                
                plt.figure(figsize=(8, 4))
                plt.bar(categorias, quantidades, color='mediumseagreen')
                plt.xlabel("Categoria")
                plt.ylabel("Quantidade Total")
                plt.title("Consumo por Categoria")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()
                
                
                img_path = f"grafico_temp_{usuario_id}.png"
                plt.savefig(img_path)
                plt.close()
                
                
                pdf.ln(5)
                pdf.cell(0, 10, "Gráfico de Consumo por Categoria:", ln=True)
                pdf.image(img_path, x=20, y=None, w=170)
                
                
                try:
                    os.remove(img_path)
                except Exception as e:
                    print(f"Aviso: Não foi possível remover a imagem temporária: {e}")
            except Exception as e:
                print(f"Erro ao criar gráfico: {e}")
                
        
        # Salvar o PDF
        try:
            pdf_path = f"N:/Meus-trabalhos/Projetos/Projeto-ecovida-sustentabilidade/pdf_relatorios/relatorio_sustentabilidade_{usuario_id}.pdf"
            pdf.output(pdf_path)

            import os
            caminho_completo = os.path.abspath(pdf_path)
            print(f"PDF salvo em: {caminho_completo}")

            print(f"Relatório gerado com sucesso! Salvo como: {pdf_path}")
            return True
        except Exception as e:
            print(f"Erro ao salvar o PDF: {e}")
            return False
        
    except Exception as e:
        print(f"Erro ao gerar o PDF: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    
def limpar_dados():
    conn = conectar()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM registros")
        
        cursor.execute("DELETE FROM habitos")
        conn.commit()
        conn.close()
        print("📂 Todos os registros foram apagados.")
        return True
    except Exception as e:
        print(f"Erro ao limpar dados: {e}")
        if conn and conn.is_connected():
            conn.close()
        return False

def zerar_tempos():
    conn = conectar()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM registros")
        conn.commit()
        conn.close()
        print("⏰ Todos os registros foram zerados.")
        return True
    except Exception as e:
        print(f"Erro ao zerar tempos: {e}")
        if conn and conn.is_connected():
            conn.close()
        return False

def recomendar_habito(usuario_id):  
    conn = conectar()
    if conn is None:
        return "Erro de conexão com o banco de dados."
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT h.nome, h.categoria, AVG(r.quantidade) as media
            FROM registros r
            JOIN habitos h ON r.habito_id = h.id
            WHERE r.usuario_id = %s
            GROUP BY h.nome, h.categoria
            ORDER BY media DESC
            LIMIT 1;
        """, (usuario_id,))
        resultado = cursor.fetchone()
        conn.close()

        if resultado:
            nome, categoria, media = resultado
            # Recomendações baseadas na categoria
            recomendacoes = {
                'água': [
                    f"Você está usando em média {int(media)} litros em '{nome}'. Tente reduzir para economizar água.",
                    "Dica: Feche a torneira enquanto escova os dentes ou ensaboa as mãos.",
                    "Dica: Um banho econômico pode usar menos de 45 litros de água."
                ],
                'energia': [
                    f"Seu consumo médio de energia para '{nome}' é de {int(media)} kWh. Tente reduzir.",
                    "Dica: Desligue aparelhos da tomada quando não estiverem em uso.",
                    "Dica: Use lâmpadas LED, que consomem até 80% menos energia."
                ],
                'transporte': [
                    f"Você percorre em média {int(media)} km em '{nome}'. Considere alternativas mais sustentáveis.",
                    "Dica: Use transporte público ou considere uma carona compartilhada.",
                    "Dica: Para distâncias curtas, caminhe ou use bicicleta."
                ],
                'resíduos': [
                    f"Você produz em média {int(media)} kg de resíduos em '{nome}'. Tente reduzir.",
                    "Dica: Separe seus resíduos para reciclagem.",
                    "Dica: Evite produtos com embalagens excessivas."
                ]
            }
            
            categoria_lower = categoria.lower() if categoria else "outros"
            if categoria_lower in recomendacoes:
                return "\n\n".join(recomendacoes[categoria_lower])
            else:
                return f"📌 Você pode melhorar suas práticas relacionadas a '{nome}' (média de {int(media)})"
        else:
            return "Sem dados suficientes para recomendação. Registre mais hábitos!"
    except Exception as e:
        print(f"Erro ao gerar recomendação: {e}")
        if conn and conn.is_connected():
            conn.close()
        return "Erro ao gerar recomendação. Por favor, tente novamente."
