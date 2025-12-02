from model.conexao_model import conexao

def get_usuarios():
    """Lista todos os usuários"""
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario ORDER BY nome")
        usuarios = cursor.fetchall()
        cursor.close()
        
        return usuarios
    
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return []


def excluir_usuario(id_usuario):
    """Exclui um usuário pelo ID"""
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM usuario WHERE id_usuario = %s", (id_usuario,))
        conexao.commit()
        cursor.close()
        
        return {"success": True, "message": "Usuário excluído com sucesso."}
    
    except Exception as e:
        print(f"Erro ao excluir usuário: {e}")
        return {"success": False, "error": str(e)}