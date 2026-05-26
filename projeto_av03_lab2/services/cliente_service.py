from projeto_av03_lab2.repositories import cliente_repository


def cadastrar_cliente(nome, email, documento):
    """Cadastra um novo cliente."""
    cliente_repository.inserir(nome, email, documento)


def buscar_clientes(termo_busca=None):
    """Busca clientes por nome ou lista todos."""
    cliente_repository.buscar(termo_busca)


def atualizar_cliente(id_cliente, novo_nome, novo_email, novo_documento):
    """Atualiza os dados de um cliente existente."""
    cliente_repository.atualizar(id_cliente, novo_nome, novo_email, novo_documento)


def remover_cliente(id_cliente):
    """Remove um cliente e todos os seus registros dependentes."""
    cliente_repository.deletar(id_cliente)
