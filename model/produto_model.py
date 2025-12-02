from flask import request, render_template
from model.conexao_model import conexao


# ============================================================
# INSERT – cadastrar produto
# ============================================================
def inserir_produto():

    dados = {
        "nome_produto": request.form.get("nome_produto"),
        "especie": request.form.get("especie"),
        "fase_vida": request.form.get("fase_vida"),
        "peso": request.form.get("peso"),
        "ingredientes": request.form.get("ingredientes"),
        "tabela_nutricional": request.form.get("tabela_nutricional"),
        "aditivos": request.form.get("aditivos"),
        "descricao": request.form.get("descricao"),
        "data_fabricacao": request.form.get("data_fabricacao"),
        "data_validade": request.form.get("data_validade"),
        "lote": request.form.get("lote"),
        "armazenamento": request.form.get("armazenamento"),
        "preco_unitario": request.form.get("preco_unitario"),
        "quantidade_estoque": request.form.get("quantidade_estoque"),
        "id_empresa": request.form.get("id_empresa"),
        "id_funcionario": request.form.get("id_funcionario"),
        "status": request.form.get("status"),
        "id_adm": request.form.get("id_adm")
    }

    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)

        sql = """
            INSERT INTO produto (
                nome_produto, especie, fase_vida, peso, ingredientes, tabela_nutricional,
                aditivos, descricao, data_fabricacao, data_validade, lote, armazenamento,
                preco_unitario, quantidade_estoque, id_empresa, id_funcionario, status, id_adm
            ) VALUES (
                %(name)s, %(especie)s, %(fase_vida)s, %(peso)s, %(ingredientes)s, %(tabela)s,
                %(aditivos)s, %(descricao)s, %(data_fab)s, %(data_val)s, %(lote)s, %(arma)s,
                %(preco)s, %(quant)s, %(id_empresa)s, %(id_func)s, %(status)s, %(id_adm)s
            )
        """

        # Renomeia para encaixar no SQL acima
        valores = {
            "name": dados["nome_produto"],
            "especie": dados["especie"],
            "fase_vida": dados["fase_vida"],
            "peso": dados["peso"],
            "ingredientes": dados["ingredientes"],
            "tabela": dados["tabela_nutricional"],
            "aditivos": dados["aditivos"],
            "descricao": dados["descricao"],
            "data_fab": dados["data_fabricacao"],
            "data_val": dados["data_validade"],
            "lote": dados["lote"],
            "arma": dados["armazenamento"],
            "preco": dados["preco_unitario"],
            "quant": dados["quantidade_estoque"],
            "id_empresa": dados["id_empresa"],
            "id_func": dados["id_funcionario"],
            "status": dados["status"],
            "id_adm": dados["id_adm"]
        }

        cursor.execute(sql, valores)
        conexao.commit()
        return "Produto cadastrado com sucesso!"

    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"Erro ao inserir produto: {e}")
        return "Erro ao cadastrar produto."

    finally:
        if cursor:
            cursor.close()



# ============================================================
# UPDATE – alterar produto existente
# ============================================================
def alterar_produto(id_produto):

    dados = {
        "nome_produto": request.form.get("nome_produto"),
        "especie": request.form.get("especie"),
        "fase_vida": request.form.get("fase_vida"),
        "peso": request.form.get("peso"),
        "ingredientes": request.form.get("ingredientes"),
        "tabela_nutricional": request.form.get("tabela_nutricional"),
        "aditivos": request.form.get("aditivos"),
        "descricao": request.form.get("descricao"),
        "data_fabricacao": request.form.get("data_fabricacao"),
        "data_validade": request.form.get("data_validade"),
        "lote": request.form.get("lote"),
        "armazenamento": request.form.get("armazenamento"),
        "preco_unitario": request.form.get("preco_unitario"),
        "quantidade_estoque": request.form.get("quantidade_estoque"),
        "id_empresa": request.form.get("id_empresa"),
        "id_funcionario": request.form.get("id_funcionario"),
        "status": request.form.get("status"),
        "id_adm": request.form.get("id_adm")
    }

    cursor = None

    try:
        cursor = conexao.cursor(dictionary=True)

        sql = """
            UPDATE produto
            SET nome_produto=%s, especie=%s, fase_vida=%s, peso=%s,
                ingredientes=%s, tabela_nutricional=%s, aditivos=%s,
                descricao=%s, data_fabricacao=%s, data_validade=%s, lote=%s,
                armazenamento=%s, preco_unitario=%s, quantidade_estoque=%s,
                id_empresa=%s, id_funcionario=%s, status=%s, id_adm=%s
            WHERE id_produto=%s
        """

        valores = (
            dados["nome_produto"], dados["especie"], dados["fase_vida"], dados["peso"],
            dados["ingredientes"], dados["tabela_nutricional"], dados["aditivos"],
            dados["descricao"], dados["data_fabricacao"], dados["data_validade"],
            dados["lote"], dados["armazenamento"], dados["preco_unitario"],
            dados["quantidade_estoque"], dados["id_empresa"], dados["id_funcionario"],
            dados["status"], dados["id_adm"], id_produto
        )

        cursor.execute(sql, valores)
        conexao.commit()

        return "Produto atualizado com sucesso!"

    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"Erro ao alterar produto: {e}")
        return "Erro ao alterar produto."

    finally:
        if cursor:
            cursor.close()



# ============================================================
# DELETE – excluir produto
# ============================================================
def excluir_produto(id_produto):

    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)

        sql = "DELETE FROM produto WHERE id_produto = %s"
        cursor.execute(sql, (id_produto,))
        conexao.commit()

        return "Produto excluído com sucesso!"

    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"Erro ao excluir produto: {e}")
        return "Erro ao excluir produto."

    finally:
        if cursor:
            cursor.close()



# ============================================================
# SELECT – consultar produto (todos ou por id)
# ============================================================
def consultar_produtos(id_produto=None):

    cursor = None
    try:
        cursor = conexao.cursor(dictionary=True)

        if id_produto:
            sql = "SELECT * FROM produto WHERE id_produto = %s"
            cursor.execute(sql, (id_produto,))
            return cursor.fetchone()

        else:
            sql = "SELECT * FROM produto ORDER BY id_produto DESC"
            cursor.execute(sql)
            return cursor.fetchall()

    except Exception as e:
        print(f"Erro ao consultar produtos: {e}")
        return None

    finally:
        if cursor:
            cursor.close()
