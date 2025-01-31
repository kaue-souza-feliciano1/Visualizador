import requests
import sqlite3
from flask import Flask, request, render_template
from werkzeug.security import generate_password_hash, check_password_hash

ip_publico = requests.get("https://api4.ipify.org?format=text").text
app = Flask(__name__)

# Criar o banco de dados e a tabela (se não existir)
def criar_banco():
    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            ip TEXT NOT NULL  -- Adicionada a coluna para armazenar o IP
        )
    """)

    conn.commit()
    conn.close()

@app.route("/")
def formulario():
    return render_template("index.html")  # Renderiza o HTML do formulário

@app.route("/salvar", methods=["POST"])
def salvar():
    nome = request.form["nome"]
    senha = request.form["senha"]
    ip = request.remote_addr
    # Hash da senha antes de armazenar
    senha_hash = generate_password_hash(senha)

    conn = sqlite3.connect("dados.db")
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO usuarios (nome, senha, ip) VALUES (?, ?, ?)", (nome, senha, ip))
        conn.commit()
        mensagem = "Cadastro realizado com sucesso!"
    except sqlite3.IntegrityError:
        mensagem = "Erro: Nome de usuário já cadastrado!"

    conn.close()
    return f"<h2>{mensagem}</h2><a href='/'>Voltar</a>"

if __name__ == "__main__":
    criar_banco()
    app.run(debug=True)