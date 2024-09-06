from flask import Flask, render_template, request, redirect
import pyodbc

# Configurar a string de conexão com autenticação integrada do Windows
connection_string = (
    "DRIVER={SQL Server};"
    "SERVER=DESKTOP-U88IQLJ\\SRV4132;"  # Nome do servidor SQL
    "DATABASE=ab_ifood;"  # Nome do banco de dados
    "Trusted_Connection=yes;"  # Autenticação integrada do Windows
)

# Classe para representar um usuário
class Usuario:
    def __init__(self, nome, cpf, email, celular):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.celular = celular

# Lista de usuários (substituível por uma consulta ao banco de dados)
lista = []

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('login.html', titulo='Login', usuarios=lista)

@app.route('/cadastro')
def novo():
    return render_template('cadastrar-usuario.html', titulo='Faça o seu cadastro!')

@app.route('/criar', methods=['POST',])
def criar():
    nome = request.form['nome']
    cpf = request.form['cpf']
    email = request.form['email']
    celular = request.form['Telefone']
    
    # Inserir o usuário no banco de dados
    try:
        connection = pyodbc.connect(connection_string)
        cursor = connection.cursor()
        
        insert_query = """
        INSERT INTO clientes (Nome, CPF, Email, Telefone)
        VALUES (?, ?, ?, ?)
        """
        dados = (nome, cpf, email, celular)
        cursor.execute(insert_query, dados)
        
        connection.commit()  # Confirmar a transação
    except Exception as e:
        print(f"Erro ao inserir dados no banco: {e}")
    finally:
        connection.close()
    
    # Adicionar o usuário à lista (somente para exibição)
    usuario = Usuario(nome, cpf, email, celular)
    lista.append(usuario)
    
    return render_template('lista-usuario.html', titulo='Lista de Usuarios', usuarios=lista)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/autenticar', methods=['POST',])
def autenticar():
    senha = request.form['senha']
    if senha == '123':  # A senha deveria ser verificada no banco de dados
        return redirect('/cadastro')
    else:
        return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
