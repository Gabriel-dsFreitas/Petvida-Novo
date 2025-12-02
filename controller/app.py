import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from flask import Flask, render_template, request, redirect, jsonify

from model.conexao_model import conexao
from model.cadastro_model import salvar_cadastro
from model.login_model import acessar_login

from model.usuario_model import (
    get_usuarios
)

from model.funcionario_model import (
    get_funcionarios
)

from model.produto_model import (
    inserir_produto,
    alterar_produto,
    excluir_produto,
    consultar_produtos
)

conectar = conexao
cursor = conectar.cursor()

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, '..', 'view', 'templates')

app = Flask(__name__, template_folder=template_dir)


# ==========================================================
# ROTAS PRINCIPAIS
# ==========================================================
@app.route('/')
def home():
    return render_template('redeAmigo.html')


@app.route("/", methods=['GET', 'POST'])
def s_cadastro():
    resultado_cadastro = salvar_cadastro()
    if "sucesso" in resultado_cadastro.lower():
        return redirect('/')
    else:
        return render_template('redeAmigo.html', mensagem_erro=resultado_cadastro)


@app.route("/Login", methods=['POST'])
def a_login():
    resultado_login = acessar_login()
    if "sucesso" in resultado_login.lower():
        return redirect('/')
    else:
        return render_template('redeAmigo.html', mensagem_erro=resultado_login)


# ==========================================================
# ADMIN HOME (Dashboard)
# ==========================================================
@app.route('/admin_page')
def admin_dashboard():
    try:
        # Administradores
        cursor.execute("SELECT nome_admin, email FROM adm")
        usuario_adm = cursor.fetchall()

        admin_lista = [
            {"nome_admin": a[0], "email": a[1]}
            for a in usuario_adm
        ]

        return render_template(
            "admin/dashboard.html",
            usuario_adm=admin_lista
        )

    except Exception as e:
        print("Erro:", e)
        return f"Erro interno: {e}", 500


# ==========================================================
# 📦 PRODUTOS
# ==========================================================
@app.route('/admin_page/produtos')
def listar_produtos():
    produtos = consultar_produtos()
    return render_template("admin/produtos.html", produtos=produtos)


@app.route('/admin_page/produtos/novo', methods=['GET', 'POST'])
def novo_produto():
    if request.method == 'POST':
        resultado = inserir_produto()

        if "sucesso" in resultado.lower():
            return redirect('/admin_page/produtos')

        return render_template("admin/novo_produto.html", mensagem_erro=resultado)

    return render_template("admin/novo_produto.html")


@app.route('/admin_page/produtos/editar/<int:id_produto>', methods=['GET', 'POST'])
def editar_produto(id_produto):
    if request.method == 'POST':
        resultado = alterar_produto(id_produto)

        if "sucesso" in resultado.lower():
            return redirect('/admin_page/produtos')

        produto = consultar_produtos(id_produto)
        return render_template("admin/editar_produto.html", produto=produto, mensagem_erro=resultado)

    produto = consultar_produtos(id_produto)
    return render_template("admin/editar_produto.html", produto=produto)


@app.route('/admin_page/produtos/excluir/<int:id_produto>')
def deletar_produto(id_produto):
    excluir_produto(id_produto)
    return redirect('/admin_page/produtos')


# ==========================================================
# 👥 USUÁRIOS
# ==========================================================
@app.route('/admin_page/usuarios')
def admin_usuarios():
   
    usuarios = get_usuarios()

    return render_template("admin/usuarios.html", usuarios=usuarios)


# ==========================================================
# 🏠 ABRIGOS
# ==========================================================
@app.route('/admin_page/abrigos')
def admin_abrigos():
    # Aqui futuramente você buscará do banco
    abrigos = []
    return render_template("admin/abrigos.html", abrigos=abrigos)


# ==========================================================
# 💰 VENDAS
# ==========================================================
@app.route('/admin_page/vendas')
def admin_vendas():
    vendas = []  # Futuro: preencher com SELECT
    return render_template("admin/vendas.html", vendas=vendas)


# ==========================================================
# 🤝 FUNCIONÁRIOS
# ==========================================================
@app.route('/admin_page/colaboradores')
def admin_funcionarios():
    funcionarios = get_funcionarios()

    return render_template("admin/funcionarios.html", funcionarios=funcionarios)


# ==========================================================
# 📍 ENDEREÇO
# ==========================================================
@app.route('/admin_page/endereco')
def admin_endereco():
    return render_template("admin/endereco.html")


# ==========================================================
# EXECUÇÃO
# ==========================================================
if __name__ == '__main__':
    app.run(debug=True)
