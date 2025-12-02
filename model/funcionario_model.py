from model.conexao_model import conexao

# ============================================================
# SELECT – lista todos os funcionários
# ============================================================
def get_funcionarios():
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionario ORDER BY nome")
        funcionarios = cursor.fetchall()
        cursor.close()
        
        return funcionarios

    except Exception as e:
        print(f"Erro ao buscar funcionários: {e}")
        return None


# ============================================================
# SELECT – funcionário por ID
# ============================================================
def get_funcionario(id_funcionario):
    try:
        cursor = conexao.cursor(dictionary=True)
        cursor.execute("SELECT * FROM funcionario WHERE id_funcionario = %s", (id_funcionario,))
        funcionario = cursor.fetchone()
        cursor.close()

        return funcionario

    except Exception as e:
        print(f"Erro ao buscar funcionário: {e}")
        return None


# ============================================================
# INSERT – cadastrar funcionário
# ============================================================
def inserir_funcionario(dados):
    try:
        cursor = conexao.cursor()

        sql = """
            INSERT INTO funcionario
            (nome, email, idade, telefone, senha, cargo, status_funcionario, id_adm, novo_status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        valores = (
            dados["nome"],
            dados["email"],
            dados["idade"],
            dados["telefone"],
            dados["senha"],
            dados["cargo"],
            dados["status_funcionario"],
            dados["id_adm"],
            dados["novo_status"]
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()

        return "Funcionário cadastrado com sucesso!"

    except Exception as e:
        print(f"Erro ao inserir funcionário: {e}")
        return f"Erro ao cadastrar funcionário: {e}"


# ============================================================
# UPDATE – alterar funcionário
# ============================================================
def alterar_funcionario(id_funcionario, dados):
    try:
        cursor = conexao.cursor()

        sql = """
            UPDATE funcionario SET
            nome=%s, email=%s, idade=%s, telefone=%s, senha=%s,
            cargo=%s, status_funcionario=%s, id_adm=%s, novo_status=%s
            WHERE id_funcionario=%s
        """

        valores = (
            dados["nome"],
            dados["email"],
            dados["idade"],
            dados["telefone"],
            dados["senha"],
            dados["cargo"],
            dados["status_funcionario"],
            dados["id_adm"],
            dados["novo_status"],
            id_funcionario
        )

        cursor.execute(sql, valores)
        conexao.commit()
        cursor.close()

        return "Funcionário atualizado com sucesso!"

    except Exception as e:
        print(f"Erro ao alterar funcionário: {e}")
        return f"Erro ao atualizar funcionário: {e}"


# ============================================================
# DELETE – excluir funcionário
# ============================================================
def excluir_funcionario(id_funcionario):
    try:
        cursor = conexao.cursor()
        cursor.execute("DELETE FROM funcionario WHERE id_funcionario = %s", (id_funcionario,))
        conexao.commit()
        cursor.close()

        return "Funcionário excluído com sucesso!"

    except Exception as e:
        print(f"Erro ao excluir funcionário: {e}")
        return f"Erro ao excluir funcionário: {e}"
