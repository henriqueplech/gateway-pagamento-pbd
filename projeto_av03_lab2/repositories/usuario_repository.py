from projeto_av03_lab2.database import obter_cursor


def inserir(nome, email, senha_hash):
    """Insere um novo usuario com a senha ja em hash."""
    try:
        with obter_cursor() as (conn, cursor):
            sql = "INSERT INTO usuarios (nome, email, senha) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nome, email, senha_hash))
            print("Usuário cadastrado com sucesso!")
    except Exception as e:
        print(f"Erro ao cadastrar usuário: {e}")


def buscar_por_email(email):
    """Busca um usuario pelo email. Retorna (usuario_id, senha_hash) ou None."""
    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            sql = "SELECT usuario_id, senha FROM usuarios WHERE email = %s"
            cursor.execute(sql, (email,))
            return cursor.fetchone()
    except Exception as e:
        print(f"Erro ao buscar usuário: {e}")
        return None


def listar_todos():
    """Lista todos os usuarios cadastrados no sistema."""
    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            sql = "SELECT usuario_id, nome, email, criado_em FROM usuarios ORDER BY usuario_id"
            cursor.execute(sql)
            resultados = cursor.fetchall()

            if resultados:
                print(f"\n{'ID':<5} {'Nome':<30} {'Email':<35} {'Cadastrado em'}")
                print("-" * 90)
                for linha in resultados:
                    print(f"{linha[0]:<5} {linha[1]:<30} {linha[2]:<35} {linha[3]}")
            else:
                print("Nenhum usuário cadastrado.")
    except Exception as e:
        print(f"Erro ao listar usuários: {e}")
