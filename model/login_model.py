from flask import request, jsonify
from model.conexao_model import conexao

def acessar_login():
    email = request.form.get('Email')
    senha = request.form.get('Senha')

    if not email or not senha:
        return jsonify({"erro": "Email e senha são obrigatórios"}), 400

    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Primeiro verifica na tabela adm (administradores)
        sql_adm = "SELECT email, senha FROM adm WHERE email = %s AND senha = %s"
        cursor.execute(sql_adm, (email, senha))
        resultado_adm = cursor.fetchone()
        
        if resultado_adm:
            return jsonify({
                "mensagem": "Login de administrador realizado com sucesso",
                "tipo": "admin"
            }), 200
        
        # Se não for admin, verifica na tabela funcionario
        sql_funcionario = "SELECT email, senha FROM funcionario WHERE email = %s AND senha = %s"
        cursor.execute(sql_funcionario, (email, senha))
        resultado_funcionario = cursor.fetchone()
        
        if resultado_funcionario:
            return jsonify({
                "mensagem": "Login de funcionário realizado com sucesso",
                "tipo": "funcionario"
            }), 200
        
        # Se não for funcionário, verifica na tabela usuario (clientes)
        sql_usuario = "SELECT email, senha FROM usuario WHERE email = %s AND senha = %s"
        cursor.execute(sql_usuario, (email, senha))
        resultado_usuario = cursor.fetchone()
        
        if resultado_usuario:
            return jsonify({
                "mensagem": "Login de cliente realizado com sucesso",
                "tipo": "usuario"
            }), 200
        else:
            return jsonify({"erro": "Email ou senha incorretos"}), 401

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

    finally:
        if 'cursor' in locals():
            cursor.close()