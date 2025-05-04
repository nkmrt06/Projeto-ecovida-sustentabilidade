import mysql.connector
from mysql.connector import Error

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
    except Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


