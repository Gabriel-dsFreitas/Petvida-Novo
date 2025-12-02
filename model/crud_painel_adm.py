from model.conexao_model import conexao

# ========== CRUD PARA PRODUTOS ==========

def get_produtos():
    """Lista todos os produtos com informações detalhadas"""
    try:
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT 
                p.*,
                e.nome_empresa,
                f.nome as nome_funcionario,
                a.nome_admin as nome_adm
            FROM produto p
            LEFT JOIN empresa e ON p.id_empresa = e.id_empresa
            LEFT JOIN funcionario f ON p.id_funcionario = f.id_funcionario
            LEFT JOIN adm a ON p.id_adm = a.id_adm
            ORDER BY p.nome_produto
        """
        cursor.execute(sql)
        produtos = cursor.fetchall()
        cursor.close()
        
        return {"success": True, "produtos": produtos}
    
    except Exception as e:
        print(f"Erro ao buscar produtos: {e}")
        return {"success": False, "error": str(e)}

def get_produto_detalhes(id_produto):
    """Retorna os detalhes de um produto específico"""
    try:
        cursor = conexao.cursor(dictionary=True)
        sql = """
            SELECT 
                p.*,
                e.nome_empresa,
                f.nome as nome_funcionario,
                a.nome_admin as nome_adm
            FROM produto p
            LEFT JOIN empresa e ON p.id_empresa = e.id_empresa
            LEFT JOIN funcionario f ON p.id_funcionario = f.id_funcionario
            LEFT JOIN adm a ON p.id_adm = a.id_adm
            WHERE p.id_produto = %s
        """
        cursor.execute(sql, (id_produto,))
        produto = cursor.fetchone()
        cursor.close()
        
        if produto:
            return {"success": True, "produto": produto}
        else:
            return {"success": False, "error": "Produto não encontrado"}
    
    except Exception as e:
        print(f"Erro ao buscar produto {id_produto}: {e}")
        return {"success": False, "error": str(e)}

def create_produto(data):
    """Cria um novo produto"""
    try:
        cursor = conexao.cursor()
        
        sql = """
            INSERT INTO produto (
                nome_produto, especie, fase_vida, peso, ingredientes,
                tabela_nutricional, aditivos, descricao, data_fabricacao,
                data_validade, lote, armazenamento, preco_unitario,
                quantidade_estoque, id_empresa, id_funcionario, status, id_adm
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.execute(sql, (
            data['nome_produto'],
            data.get('especie'),
            data.get('fase_vida'),
            data.get('peso'),
            data.get('ingredientes'),
            data.get('tabela_nutricional'),
            data.get('aditivos'),
            data.get('descricao'),
            data.get('data_fabricacao'),
            data.get('data_validade'),
            data.get('lote'),
            data.get('armazenamento'),
            data.get('preco_unitario'),
            data.get('quantidade_estoque', 0),
            data.get('id_empresa'),
            data.get('id_funcionario'),
            data.get('status', 'Ativo'),
            data.get('id_adm')
        ))
        
        conexao.commit()
        produto_id = cursor.lastrowid
        cursor.close()
        
        return {
            "success": True, 
            "message": "Produto criado com sucesso",
            "id_produto": produto_id
        }
    
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao criar produto: {e}")
        return {"success": False, "error": str(e)}

def update_produto(id_produto, data):
    """Atualiza um produto"""
    try:
        cursor = conexao.cursor()
        
        # Verifica se o produto existe
        cursor.execute("SELECT id_produto FROM produto WHERE id_produto = %s", (id_produto,))
        if not cursor.fetchone():
            cursor.close()
            return {"success": False, "error": "Produto não encontrado"}
        
        sql = """
            UPDATE produto 
            SET 
                nome_produto = %s,
                especie = %s,
                fase_vida = %s,
                peso = %s,
                ingredientes = %s,
                tabela_nutricional = %s,
                aditivos = %s,
                descricao = %s,
                data_fabricacao = %s,
                data_validade = %s,
                lote = %s,
                armazenamento = %s,
                preco_unitario = %s,
                quantidade_estoque = %s,
                id_empresa = %s,
                id_funcionario = %s,
                status = %s,
                id_adm = %s
            WHERE id_produto = %s
        """
        
        cursor.execute(sql, (
            data.get('nome_produto'),
            data.get('especie'),
            data.get('fase_vida'),
            data.get('peso'),
            data.get('ingredientes'),
            data.get('tabela_nutricional'),
            data.get('aditivos'),
            data.get('descricao'),
            data.get('data_fabricacao'),
            data.get('data_validade'),
            data.get('lote'),
            data.get('armazenamento'),
            data.get('preco_unitario'),
            data.get('quantidade_estoque'),
            data.get('id_empresa'),
            data.get('id_funcionario'),
            data.get('status'),
            data.get('id_adm'),
            id_produto
        ))
        
        conexao.commit()
        cursor.close()
        
        return {"success": True, "message": "Produto atualizado com sucesso"}
    
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao atualizar produto {id_produto}: {e}")
        return {"success": False, "error": str(e)}

def delete_produto(id_produto):
    """Remove um produto (muda status para Inativo)"""
    try:
        cursor = conexao.cursor()
        
        # Verifica se o produto existe
        cursor.execute("SELECT id_produto FROM produto WHERE id_produto = %s", (id_produto,))
        if not cursor.fetchone():
            cursor.close()
            return {"success": False, "error": "Produto não encontrado"}
        
        # Em vez de deletar, mudamos o status para Inativo
        sql = "UPDATE produto SET status = 'Inativo' WHERE id_produto = %s"
        cursor.execute(sql, (id_produto,))
        
        conexao.commit()
        cursor.close()
        
        return {"success": True, "message": "Produto desativado com sucesso"}
    
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao desativar produto {id_produto}: {e}")
        return {"success": False, "error": str(e)}

def activate_produto(id_produto):
    """Reativa um produto (muda status para Ativo)"""
    try:
        cursor = conexao.cursor()
        
        sql = "UPDATE produto SET status = 'Ativo' WHERE id_produto = %s"
        cursor.execute(sql, (id_produto,))
        
        conexao.commit()
        cursor.close()
        
        return {"success": True, "message": "Produto reativado com sucesso"}
    
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao reativar produto {id_produto}: {e}")
        return {"success": False, "error": str(e)}

def update_estoque(id_produto, quantidade_estoque):
    """Atualiza apenas o estoque de um produto"""
    try:
        cursor = conexao.cursor()
        
        sql = "UPDATE produto SET quantidade_estoque = %s WHERE id_produto = %s"
        cursor.execute(sql, (quantidade_estoque, id_produto))
        
        conexao.commit()
        cursor.close()
        
        return {"success": True, "message": "Estoque atualizado com sucesso"}
    
    except Exception as e:
        conexao.rollback()
        print(f"Erro ao atualizar estoque do produto {id_produto}: {e}")
        return {"success": False, "error": str(e)}

def filtrar_produtos(filtros):
    """Filtra produtos por vários critérios"""
    try:
        especie = filtros.get('especie')
        fase_vida = filtros.get('fase_vida')
        status = filtros.get('status', 'Ativo')
        empresa = filtros.get('empresa')
        estoque_minimo = filtros.get('estoque_minimo')
        
        cursor = conexao.cursor(dictionary=True)
        
        sql = """
            SELECT p.*, e.nome_empresa 
            FROM produto p
            LEFT JOIN empresa e ON p.id_empresa = e.id_empresa
            WHERE 1=1
        """
        params = []
        
        if especie:
            sql += " AND p.especie = %s"
            params.append(especie)
        
        if fase_vida:
            sql += " AND p.fase_vida = %s"
            params.append(fase_vida)
        
        if status:
            sql += " AND p.status = %s"
            params.append(status)
        
        if empresa:
            sql += " AND p.id_empresa = %s"
            params.append(int(empresa))
        
        if estoque_minimo:
            sql += " AND p.quantidade_estoque >= %s"
            params.append(int(estoque_minimo))
        
        sql += " ORDER BY p.nome_produto"
        
        cursor.execute(sql, params)
        produtos = cursor.fetchall()
        cursor.close()
        
        return {"success": True, "produtos": produtos}
    
    except Exception as e:
        print(f"Erro ao filtrar produtos: {e}")
        return {"success": False, "error": str(e)}

def estatisticas_produtos():
    """Retorna estatísticas sobre produtos"""
    try:
        cursor = conexao.cursor(dictionary=True)
        
        # Total de produtos por espécie
        cursor.execute("""
            SELECT especie, COUNT(*) as total, 
                   SUM(quantidade_estoque) as total_estoque
            FROM produto 
            WHERE status = 'Ativo'
            GROUP BY especie
        """)
        por_especie = cursor.fetchall()
        
        # Total de produtos por fase de vida
        cursor.execute("""
            SELECT fase_vida, COUNT(*) as total
            FROM produto 
            WHERE status = 'Ativo'
            GROUP BY fase_vida
        """)
        por_fase_vida = cursor.fetchall()
        
        # Produtos com estoque baixo (menos de 10 unidades)
        cursor.execute("""
            SELECT COUNT(*) as total_baixo_estoque
            FROM produto 
            WHERE status = 'Ativo' AND quantidade_estoque < 10
        """)
        baixo_estoque = cursor.fetchone()['total_baixo_estoque']
        
        # Valor total em estoque
        cursor.execute("""
            SELECT 
                SUM(quantidade_estoque) as total_unidades,
                SUM(preco_unitario * quantidade_estoque) as valor_total_estoque
            FROM produto 
            WHERE status = 'Ativo'
        """)
        valor_estoque = cursor.fetchone()
        
        cursor.close()
        
        estatisticas = {
            "por_especie": por_especie,
            "por_fase_vida": por_fase_vida,
            "baixo_estoque": baixo_estoque,
            "total_unidades": valor_estoque['total_unidades'] or 0,
            "valor_total_estoque": float(valor_estoque['valor_total_estoque'] or 0)
        }
        
        return {"success": True, "estatisticas": estatisticas}
    
    except Exception as e:
        print(f"Erro ao buscar estatísticas de produtos: {e}")
        return {"success": False, "error": str(e)}

# ========== CRUD PARA OUTRAS TABELAS ==========

def get_adms():
    """Lista todos os administradores"""
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM adm ORDER BY nome_admin")
        administradores = cursor.fetchall()
        cursor.close()
        
        return {"success": True, "administradores": administradores}
    
    except Exception as e:
        print(f"Erro ao buscar administradores: {e}")
        return {"success": False, "error": str(e)}

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

def get_usuarios():
    """Lista todos os usuários"""
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuario ORDER BY nome")
        usuarios = cursor.fetchall()
        cursor.close()
        
        return {"success": True, "usuarios": usuarios}
    
    except Exception as e:
        print(f"Erro ao buscar usuários: {e}")
        return {"success": False, "error": str(e)}

def get_estatisticas_gerais():
    """Retorna estatísticas gerais do sistema"""
    try:
        cursor = conexao.cursor(dictionary=True)
        
        estatisticas = {}
        
        # Total de usuários
        cursor.execute("SELECT COUNT(*) as total FROM usuario")
        estatisticas['total_usuarios'] = cursor.fetchone()['total']
        
        # Total de funcionários ativos
        cursor.execute("SELECT COUNT(*) as total FROM funcionario WHERE status = 'Ativo'")
        estatisticas['total_funcionarios'] = cursor.fetchone()['total']
        
        # Total de produtos ativos
        cursor.execute("SELECT COUNT(*) as total FROM produto WHERE status = 'Ativo'")
        estatisticas['total_produtos'] = cursor.fetchone()['total']
        
        # Total de administradores
        cursor.execute("SELECT COUNT(*) as total FROM adm")
        estatisticas['total_adms'] = cursor.fetchone()['total']
        
        # Vendas do mês
        cursor.execute("""
            SELECT 
                COUNT(*) as total_vendas, 
                COALESCE(SUM(valor_total), 0) as total_valor 
            FROM vendas 
            WHERE MONTH(data_venda) = MONTH(CURRENT_DATE()) 
            AND YEAR(data_venda) = YEAR(CURRENT_DATE())
        """)
        vendas_mes = cursor.fetchone()
        estatisticas['total_vendas_mes'] = vendas_mes['total_vendas']
        estatisticas['valor_vendas_mes'] = float(vendas_mes['total_valor'])
        
        cursor.close()
        
        return {"success": True, "estatisticas": estatisticas}
    
    except Exception as e:
        print(f"Erro ao buscar estatísticas gerais: {e}")
        return {"success": False, "error": str(e)}