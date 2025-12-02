import sys
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(ROOT)

from flask import Flask, render_template, request, redirect, jsonify

from model.conexao_model import conexao
from model.cadastro_model import salvar_cadastro
from model.login_model import acessar_login

# Importar o CRUD do painel administrativo
from crud_painel_adm import (
    get_produtos, get_produto_detalhes, create_produto, update_produto,
    delete_produto, activate_produto, update_estoque, filtrar_produtos,
    estatisticas_produtos, get_adms, get_funcionarios, get_usuarios,
    get_estatisticas_gerais
)

conectar = conexao
cursor = conectar.cursor()

current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, '..', 'view', 'templates')

app = Flask(__name__, template_folder=template_dir)

@app.route('/')
def home():
    return render_template('redeAmigo.html')

@app.route("/", methods=['GET','POST'])
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

@app.route('/admin_page')
def admin_page():
    try:
        print("🔍 Tentando conectar ao banco de dados...")
        
        # ===== BUSCAR ADMINISTRADORES =====
        cursor.execute("SELECT nome_admin, email, senha FROM adm")
        usuario_adm = cursor.fetchall()
        
        print(f"✅ Admins recuperados: {usuario_adm}")
        print(f"📊 Quantidade de admins: {len(usuario_adm)}")
        
        # Converter para dicionários
        usuarios_lista = []
        for usuario in usuario_adm:
            usuarios_lista.append({
                'nome_admin': usuario[0],
                'email': usuario[1],
                'senha': usuario[2]
            })
        
        print(f"📋 Admins formato final: {usuarios_lista}")

        # ===== BUSCAR FUNCIONÁRIOS =====
        cursor.execute("SELECT nome, email, idade, telefone, senha, cargo, status_funcionario FROM funcionario")
        funcionarios = cursor.fetchall()
        
        print(f"✅ Funcionários recuperados: {funcionarios}")
        print(f"📊 Quantidade de funcionários: {len(funcionarios)}")
        
        # Converter para dicionários
        funcionarios_lista = []
        for funcionario in funcionarios:
            funcionarios_lista.append({
                'nome': funcionario[0],
                'email': funcionario[1],
                'idade': funcionario[2],
                'telefone': funcionario[3],
                'senha': funcionario[4],
                'cargo': funcionario[5],
                'status_funcionario': funcionario[6]
            })
        
        print(f"📋 Funcionários formato final: {funcionarios_lista}")
        
        return render_template("pagina_admin.html", usuario_adm=usuarios_lista, funcionarios=funcionarios_lista)
    
    except Exception as e:
        print(f"❌ Erro ao buscar dados: {e}")
        return f"Erro: {e}", 500

# ========== API PARA PRODUTOS ==========

@app.route('/api/admin/produtos', methods=['GET'])
def api_get_produtos():
    """API para listar produtos"""
    result = get_produtos()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/admin/produtos/<int:id>', methods=['GET'])
def api_get_produto(id):
    """API para obter detalhes de um produto"""
    result = get_produto_detalhes(id)
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 404 if result['error'] == "Produto não encontrado" else 500

@app.route('/api/admin/produtos', methods=['POST'])
def api_create_produto():
    """API para criar um novo produto"""
    data = request.get_json()
    result = create_produto(data)
    if result['success']:
        return jsonify(result), 201
    else:
        return jsonify(result), 400

@app.route('/api/admin/produtos/<int:id>', methods=['PUT'])
def api_update_produto(id):
    """API para atualizar um produto"""
    data = request.get_json()
    result = update_produto(id, data)
    if result['success']:
        return jsonify(result)
    else:
        if result['error'] == "Produto não encontrado":
            return jsonify(result), 404
        return jsonify(result), 400

@app.route('/api/admin/produtos/<int:id>', methods=['DELETE'])
def api_delete_produto(id):
    """API para desativar um produto"""
    result = delete_produto(id)
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/admin/produtos/<int:id>/activate', methods=['POST'])
def api_activate_produto(id):
    """API para reativar um produto"""
    result = activate_produto(id)
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/admin/produtos/<int:id>/estoque', methods=['PUT'])
def api_update_estoque(id):
    """API para atualizar estoque de um produto"""
    data = request.get_json()
    if 'quantidade_estoque' not in data:
        return jsonify({"success": False, "error": "Quantidade de estoque é obrigatória"}), 400
    
    result = update_estoque(id, data['quantidade_estoque'])
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

@app.route('/api/admin/produtos/filtrar', methods=['GET'])
def api_filtrar_produtos():
    """API para filtrar produtos"""
    filtros = {
        'especie': request.args.get('especie'),
        'fase_vida': request.args.get('fase_vida'),
        'status': request.args.get('status', 'Ativo'),
        'empresa': request.args.get('empresa'),
        'estoque_minimo': request.args.get('estoque_minimo')
    }
    
    result = filtrar_produtos(filtros)
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 400

# ========== API PARA ESTATÍSTICAS ==========

@app.route('/api/admin/estatisticas/produtos', methods=['GET'])
def api_estatisticas_produtos():
    """API para estatísticas de produtos"""
    result = estatisticas_produtos()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/admin/estatisticas/gerais', methods=['GET'])
def api_estatisticas_gerais():
    """API para estatísticas gerais do sistema"""
    result = get_estatisticas_gerais()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

# ========== API PARA OUTRAS ENTIDADES ==========

@app.route('/api/admin/administradores', methods=['GET'])
def api_get_administradores():
    """API para listar administradores"""
    result = get_adms()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/admin/funcionarios', methods=['GET'])
def api_get_funcionarios():
    """API para listar funcionários"""
    result = get_funcionarios()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

@app.route('/api/admin/usuarios', methods=['GET'])
def api_get_usuarios():
    """API para listar usuários"""
    result = get_usuarios()
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500

# ========== ROTA PARA CARREGAR DADOS INICIAIS DO PAINEL ==========

@app.route('/api/admin/dashboard', methods=['GET'])
def api_admin_dashboard():
    """API para carregar todos os dados do painel de uma vez"""
    try:
        produtos = get_produtos()
        funcionarios = get_funcionarios()
        administradores = get_adms()
        usuarios = get_usuarios()
        estatisticas = get_estatisticas_gerais()
        
        # Verificar se todas as consultas foram bem sucedidas
        all_success = (
            produtos['success'] and 
            funcionarios['success'] and 
            administradores['success'] and 
            usuarios['success'] and 
            estatisticas['success']
        )
        
        if all_success:
            return jsonify({
                "success": True,
                "produtos": produtos['produtos'],
                "funcionarios": funcionarios['funcionarios'],
                "administradores": administradores['administradores'],
                "usuarios": usuarios['usuarios'],
                "estatisticas": estatisticas['estatisticas']
            })
        else:
            return jsonify({"success": False, "error": "Erro ao carregar alguns dados"}), 500
    
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
        
if __name__ == '__main__':
    app.run(debug=True)