from projeto_av03_lab2.database import obter_cursor


def inserir(nome, email, documento):
    """INSERT - Adiciona um novo cliente no banco."""
    try:
        with obter_cursor() as (conn, cursor):
            sql = "INSERT INTO clientes (nome, email, documento) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, email, documento))
            print("Cliente cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao inserir cliente: {e}")


def buscar(termo_busca=None):
    """SELECT - Consulta clientes. Usa ILIKE se tiver termo de busca."""
    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            if termo_busca:
                sql = "SELECT * FROM clientes WHERE nome ILIKE %s"
                cursor.execute(sql, (f'%{termo_busca}%',))
            else:
                sql = "SELECT * FROM clientes"
                cursor.execute(sql)

            resultados = cursor.fetchall()
            if resultados:
                print(f"\n{'ID':<5} {'Nome':<30} {'Email':<30} {'Documento':<15} {'Criado em'}")
                print("-" * 90)
                for linha in resultados:
                    print(f"{linha[0]:<5} {linha[1]:<30} {linha[2]:<30} {linha[3]:<15} {linha[4]}")
            else:
                print("Nenhum cliente encontrado.")
    except Exception as e:
        print(f"Erro ao buscar clientes: {e}")


def atualizar(id_cliente, novo_nome, novo_email, novo_documento):
    """UPDATE - Modifica dados de um cliente existente."""
    try:
        with obter_cursor() as (conn, cursor):
            sql = "UPDATE clientes SET nome = %s, email = %s, documento = %s WHERE cliente_id = %s"
            cursor.execute(sql, (novo_nome, novo_email, novo_documento, id_cliente))

            if cursor.rowcount > 0:
                print("Cliente atualizado com sucesso!")
            else:
                print("Nenhum cliente encontrado com esse ID.")
    except Exception as e:
        print(f"Erro ao atualizar cliente: {e}")


def deletar(id_cliente):
    """DELETE - Remove um cliente e seus registros dependentes (FK)."""
    try:
        with obter_cursor() as (conn, cursor):
            # Remove estornos vinculados as transacoes do cliente
            cursor.execute("""
                DELETE FROM estornos
                WHERE transacao_id IN (
                    SELECT transacao_id FROM transacoes WHERE cliente_id = %s
                )
            """, (id_cliente,))

            # Remove transacoes do cliente
            cursor.execute("DELETE FROM transacoes WHERE cliente_id = %s", (id_cliente,))

            # Remove metodos de pagamento do cliente
            cursor.execute("DELETE FROM metodos_pagamento WHERE cliente_id = %s", (id_cliente,))

            # Remove o proprio cliente
            cursor.execute("DELETE FROM clientes WHERE cliente_id = %s", (id_cliente,))

            if cursor.rowcount > 0:
                print("Cliente e seus registros dependentes removidos com sucesso!")
            else:
                print("Nenhum cliente encontrado com esse ID para deletar.")
    except Exception as e:
        print(f"Erro ao deletar cliente: {e}")
