import sqlite3   # Importa a biblioteca padrão do Python para trabalhar com SQLite

# Conecta (ou cria) o arquivo do banco de dados chamado 'database.db'
# Se o arquivo não existir, ele será criado automaticamente
conn = sqlite3.connect('database.db')

# Cria um cursor, que é o "controlador" para executar comandos SQL no banco
c = conn.cursor()

# Executa o comando SQL para criar a tabela "produtos"
# - id: identificador único, numérico, autoincremental
# - nome: campo de texto obrigatório
# - preco: campo numérico decimal obrigatório
c.execute('''
CREATE TABLE produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    preco REAL NOT NULL
)
''')

# Salva (confirma) as alterações feitas no banco
conn.commit()

# Fecha a conexão com o banco, liberando os recursos
conn.close()
