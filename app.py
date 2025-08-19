from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
from pathlib import Path

# Cria a aplicação Flask
app = Flask(__name__)

# Chave secreta usada para sessões, mensagens flash etc. (aqui uma simples para dev)
app.secret_key = "dev"

# Caminho absoluto do banco de dados (garante que funcione mesmo fora da pasta atual)
DB_PATH = (Path(__file__).parent / "database.db").resolve()


# Função auxiliar para abrir conexão com o banco
def get_db_connection():
    conn = sqlite3.connect(DB_PATH)   # Conecta ao SQLite
    conn.row_factory = sqlite3.Row    # Permite acessar colunas por nome (ex: row["nome"])
    return conn


# Função para criar o banco e tabela caso não existam
def init_db():
    if not DB_PATH.exists():  # Verifica se o arquivo do banco já existe
        print("[INIT_DB] Criando novo banco...")
        with get_db_connection() as conn:  # Abre conexão
            conn.executescript("""        # Executa várias queries de uma vez
                CREATE TABLE produtos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único
                    nome TEXT NOT NULL,                   -- Nome do produto
                    preco REAL NOT NULL                   -- Preço em número decimal
                );
            """)
            conn.commit()  # Salva as alterações
        print("[INIT_DB] Banco criado em:", DB_PATH)


# Rota principal ("/") que lista os produtos
@app.route("/", endpoint="home")  # "endpoint" = nome interno da rota
def home():
    with get_db_connection() as conn:  # Abre conexão
        produtos = conn.execute(
            "SELECT id, nome, CAST(preco AS REAL) AS preco FROM produtos ORDER BY id DESC"
        ).fetchall()  # Busca todos os produtos, mais recentes primeiro
    return render_template("index.html", produtos=produtos)  # Renderiza a página


# Rota para adicionar um produto
@app.route("/add", methods=["GET", "POST"], endpoint="add")
def add_product():
    if request.method == "POST":  # Se o formulário foi enviado
        nome = (request.form.get("nome") or "").strip()  # Pega o nome do form
        preco_raw = (request.form.get("preco") or "").strip()  # Pega o preço do form

        try:
            if not nome:
                raise ValueError("Nome vazio")  # Não permite produto sem nome
            preco = float(preco_raw.replace(",", "."))  # Converte para float (aceita vírgula também)
        except Exception:
            flash("Preencha corretamente nome e preço (ex.: 19.90).", "error")  # Mostra erro
            return redirect(url_for("add"))  # Volta para o formulário

        # Insere no banco
        with get_db_connection() as conn:
            conn.execute("INSERT INTO produtos (nome, preco) VALUES (?, ?)", (nome, preco))
            conn.commit()

        flash("Produto cadastrado com sucesso!", "success")  # Mensagem de sucesso
        return redirect(url_for("home"))  # Volta para a listagem

    # Se for GET, apenas mostra o formulário
    return render_template("add.html")


# Executa o app
if __name__ == "__main__":
    init_db()  # Garante que o banco exista antes de rodar
    app.run(debug=True)  # Executa em modo debug (auto-reload + erros detalhados)
