from model.conexao_model import conexao

def get_funcionarios():
    """Lista todos os funcionários"""
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionario ORDER BY nome")
        funcionarios = cursor.fetchall()
        cursor.close()
        
        return {"success": True, "funcionarios": funcionarios}
    
    except Exception as e:
        print(f"Erro ao buscar funcionários: {e}")
        return {"success": False, "error": str(e)}