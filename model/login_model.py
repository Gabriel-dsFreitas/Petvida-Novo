from flask import request, jsonify
from model.conexao_model import conexao

def acessar_login():
    email = request.form.get('loginEmail')
    senha = request.form.get('loginSenha')

    if not email or not senha:
        return {"erro": "Email e senha são obrigatórios", "sucesso": False}, 400

    try:
        cursor = conexao.cursor(dictionary=True)

        # Lista de tabelas e o tipo correspondente
        tabelas = [
            ("adm", "admin"),
            ("funcionario", "funcionario"),
            ("usuario", "usuario")
        ]

        # Verificação unificada
        for tabela, tipo in tabelas:
            query = f"SELECT email FROM {tabela} WHERE email = %s AND senha = %s LIMIT 1"
            cursor.execute(query, (email, senha))
            resultado = cursor.fetchone()
 
            if resultado:
                return {
                    "mensagem": f"Login de {tipo} realizado com sucesso",
                    "tipo": tipo,
                    "sucesso": True
                }, 200

        # Se nenhuma tabela encontrou o usuário
        return {"erro": "Email ou senha incorretos", "sucesso": False}, 401

    except Exception as e:
        return {"erro": f"Erro interno: {str(e)}", "sucesso": False}, 500

    finally:
        if 'cursor' in locals():
            cursor.close()
