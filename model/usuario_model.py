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
        return {"success": False, "error": str(e)}
