import os
import csv
from datetime import datetime
from flask import Flask, render_template, request, redirect, send_file, session
from werkzeug.utils import secure_filename
from utils.gerar_pdf import gerar_pdf

app = Flask(__name__)
app.secret_key = 'segredo'  # Pode alterar por uma chave mais segura, se quiser

# Senha fixa para área restrita
senha_fixa = "Leao2025"

# Carrega as peças do arquivo CSV
def carregar_pecas():
    pecas = []
    try:
        with open("pecas.csv", newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            pecas = [row for row in reader]
    except FileNotFoundError:
        pass
    return pecas

# Rota principal
@app.route('/')
def home():
    pecas = carregar_pecas()
    return render_template("index.html", pecas=pecas)

# Gera PDF ao solicitar peça
@app.route('/solicitar', methods=['POST'])
def solicitar():
    nome = request.form['nome']
    peca = request.form['peca']
    obs = request.form['obs']
    data = datetime.now().strftime("%d/%m/%Y %H:%M")
    arquivo_pdf = gerar_pdf(nome, peca, obs, data)
    return send_file(arquivo_pdf, as_attachment=True)

# Login para administradores
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['senha'] == senha_fixa:
            session['logado'] = True
            return redirect('/admin')
    return render_template("login.html")

# Página administrativa
@app.route('/admin')
def admin():
    if not session.get('logado'):
        return redirect('/login')
    return render_template("admin.html")

# Upload da planilha CSV
@app.route('/upload', methods=['POST'])
def upload():
    if not session.get('logado'):
        return redirect('/login')
    file = request.files['arquivo']
    if file:
        filename = secure_filename("pecas.csv")
        file.save(filename)
    return redirect('/admin')

# Adicionar peça manualmente
@app.route('/add_peca', methods=['POST'])
def add_peca():
    if not session.get('logado'):
        return redirect('/login')
    with open("pecas.csv", "a", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([request.form['codigo'], request.form['descricao']])
    return redirect('/admin')

# Início do app (configurado para ambiente de produção)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

