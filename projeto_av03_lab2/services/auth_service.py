from werkzeug.security import generate_password_hash, check_password_hash
from projeto_av03_lab2.repositories import usuario_repository


def cadastrar_usuario(nome, email, senha):
    """Cadastra um novo usuario com senha criptografada (hash)."""
    senha_hash = generate_password_hash(senha)
    usuario_repository.inserir(nome, email, senha_hash)


def login(email, senha):
    """Valida as credenciais do usuario. Retorna True se deu certo."""
    usuario = usuario_repository.buscar_por_email(email)

    if usuario is None:
        print("Usuário não encontrado.")
        return False

    id_usuario, senha_hash_bd = usuario

    if check_password_hash(senha_hash_bd, senha):
        print("Login realizado com sucesso!")
        return True
    else:
        print("Senha incorreta.")
        return False
