import getpass

from projeto_av03_lab2.services import auth_service, cliente_service
from projeto_av03_lab2.consultas import inner_join, left_join, full_outer_join
from projeto_av03_lab2.repositories import usuario_repository


def menu_consultas_join():
    """Submenu para rodar as consultas JOIN."""
    while True:
        print("\n=== CONSULTAS JOIN ===")
        print("1. INNER JOIN  - Transacoes com cliente e lojista")
        print("2. LEFT JOIN   - Todos os clientes (com/sem transacoes)")
        print("3. FULL OUTER  - Clientes x Transacoes (todos os lados)")
        print("0. Voltar")

        opcao = input("Escolha uma consulta: ")

        if opcao == '1':
            inner_join.executar()
        elif opcao == '2':
            left_join.executar()
        elif opcao == '3':
            full_outer_join.executar()
        elif opcao == '0':
            break
        else:
            print("Opcao invalida.")


def menu_interno():
    """Menu do Sistema (Area Interna - Pos-login)"""
    while True:
        print("\n=== AREA INTERNA - GESTAO DE CLIENTES ===")
        print("--- Tabela: clientes ---")
        print("1. Cadastrar  (INSERT  novo cliente)")
        print("2. Alterar    (UPDATE  cliente existente por ID)")
        print("3. Remover    (DELETE  cliente por ID)")
        print("4. Buscar     (SELECT  cliente por nome - LIKE)")
        print("5. Exibir todos os clientes (SELECT *)")
        print("--- Tabela: usuarios ---")
        print("6. Exibir todos os usuarios do sistema (SELECT *)")
        print("--- Consultas ---")
        print("7. Consultas JOIN (INNER, LEFT, FULL OUTER)")
        print("0. Sair / Logout")

        opcao = input("Escolha uma opcao: ")

        if opcao == '1':
            nome = input("Nome do cliente: ")
            email = input("Email: ")
            documento = input("CPF (somente numeros): ")
            cliente_service.cadastrar_cliente(nome, email, documento)
        elif opcao == '2':
            id_cliente = int(input("ID do cliente a alterar: "))
            nome = input("Novo Nome: ")
            email = input("Novo Email: ")
            documento = input("Novo CPF: ")
            cliente_service.atualizar_cliente(id_cliente, nome, email, documento)
        elif opcao == '3':
            id_cliente = int(input("ID do cliente a remover: "))
            cliente_service.remover_cliente(id_cliente)
        elif opcao == '4':
            termo = input("Digite o nome para buscar (LIKE): ")
            cliente_service.buscar_clientes(termo)
        elif opcao == '5':
            cliente_service.buscar_clientes()
        elif opcao == '6':
            usuario_repository.listar_todos()
        elif opcao == '7':
            menu_consultas_join()
        elif opcao == '0':
            print("Voltando para a area externa...")
            break
        else:
            print("Opcao invalida.")


def menu_externo():
    """Menu Inicial (Area Externa)"""
    while True:
        print("\n=== SISTEMA PRINCIPAL ===")
        print("1. Cadastrar Usuario")
        print("2. Realizar Login")
        print("0. Encerrar aplicacao")

        opcao = input("Escolha uma opcao: ")

        if opcao == '1':
            nome = input("Seu Nome: ")
            email = input("Seu Email: ")
            senha = getpass.getpass("Sua Senha (oculta): ")
            auth_service.cadastrar_usuario(nome, email, senha)
        elif opcao == '2':
            email = input("Email: ")
            senha = getpass.getpass("Senha (oculta): ")
            if auth_service.login(email, senha):
                menu_interno()
        elif opcao == '0':
            print("Encerrando aplicacao...")
            break
        else:
            print("Opcao invalida.")
