import psycopg2
from decimal import Decimal
from psycopg2 import Error


# Configuracao da conexao com o PostgreSQL.
# Ajuste apenas estes valores se o banco mudar.
CONFIG_BANCO = {
    "dbname": "postgres",
    "user": "postgres",
    "password": "1234",
    "host": "localhost",
    "port": "5432",
}


# Lista de lojistas ficticios para testes.
# O "documento" e usado como chave de busca para evitar duplicidade.
LOJISTAS = [
    ("Loja Tech Prime", "12.345.678/0001-90", Decimal("2.50")),
    ("Mercado Central", "98.765.432/0001-10", Decimal("1.99")),
    ("Cafe da Praca", "11.222.333/0001-44", Decimal("3.10")),
]


# Lista de clientes ficticios.
# O par (email, documento) sera usado para localizar registros existentes.
CLIENTES = [
    ("Ana Lima", "ana.lima@email.com", "123.456.789-00"),
    ("Bruno Costa", "bruno.costa@email.com", "987.654.321-00"),
    ("Carla Souza", "carla.souza@email.com", "456.789.123-00"),
]


# Cada metodo de pagamento aponta para um cliente por email.
METODOS_PAGAMENTO = [
    {
        "cliente_email": "ana.lima@email.com",
        "tipo": "CARTAO_CREDITO",
        "token_gateway": "tok_ana_visa_001",
        "ultimos_4_digitos": "1234",
        "bandeira": "VISA",
    },
    {
        "cliente_email": "bruno.costa@email.com",
        "tipo": "CARTAO_CREDITO",
        "token_gateway": "tok_bruno_master_001",
        "ultimos_4_digitos": "9876",
        "bandeira": "MASTERCARD",
    },
    {
        "cliente_email": "carla.souza@email.com",
        "tipo": "CARTAO_DEBITO",
        "token_gateway": "tok_carla_elo_001",
        "ultimos_4_digitos": "4567",
        "bandeira": "ELO",
    },
]


# Cada conta bancaria aponta para um lojista por documento.
CONTAS_BANCARIAS = [
    {
        "lojista_documento": "12.345.678/0001-90",
        "banco_codigo": "001",
        "agencia": "1001",
        "conta": "12345-6",
        "chave_pix": "financeiro@lojatechprime.com",
    },
    {
        "lojista_documento": "98.765.432/0001-10",
        "banco_codigo": "237",
        "agencia": "2002",
        "conta": "23456-7",
        "chave_pix": "mercadocentral@pix.com",
    },
    {
        "lojista_documento": "11.222.333/0001-44",
        "banco_codigo": "104",
        "agencia": "3003",
        "conta": "34567-8",
        "chave_pix": "cafedapraca@pix.com",
    },
]


# As transacoes ligam clientes, lojistas e, quando houver, um metodo de pagamento.
# O campo "payload_adquirente" serve como identificador unico do seed.
TRANSACOES = [
    {
        "lojista_documento": "12.345.678/0001-90",
        "cliente_email": "ana.lima@email.com",
        "token_gateway": "tok_ana_visa_001",
        "valor_bruto": Decimal("150.00"),
        "valor_liquido": Decimal("146.25"),
        "status": "APROVADA",
        "tipo_pagamento": "CARTAO",
        "payload_adquirente": "seed_tx_001",
    },
    {
        "lojista_documento": "98.765.432/0001-10",
        "cliente_email": "bruno.costa@email.com",
        "token_gateway": "tok_bruno_master_001",
        "valor_bruto": Decimal("89.90"),
        "valor_liquido": Decimal("88.11"),
        "status": "APROVADA",
        "tipo_pagamento": "CARTAO",
        "payload_adquirente": "seed_tx_002",
    },
    {
        "lojista_documento": "11.222.333/0001-44",
        "cliente_email": "carla.souza@email.com",
        "token_gateway": None,
        "valor_bruto": Decimal("42.50"),
        "valor_liquido": Decimal("41.18"),
        "status": "PENDENTE",
        "tipo_pagamento": "PIX",
        "payload_adquirente": "seed_tx_003",
    },
    {
        "lojista_documento": "12.345.678/0001-90",
        "cliente_email": "bruno.costa@email.com",
        "token_gateway": "tok_bruno_master_001",
        "valor_bruto": Decimal("320.00"),
        "valor_liquido": Decimal("312.00"),
        "status": "CANCELADA",
        "tipo_pagamento": "CARTAO",
        "payload_adquirente": "seed_tx_004",
    },
]


# O estorno precisa apontar para uma transacao existente.
ESTORNOS = [
    {
        "payload_adquirente": "seed_tx_004",
        "valor_estornado": Decimal("320.00"),
        "motivo": "Compra cancelada pelo cliente",
        "status": "CONCLUIDO",
    }
]


# O repasse precisa apontar para um lojista e para uma conta bancaria dele.
REPASSES = [
    {
        "lojista_documento": "12.345.678/0001-90",
        "chave_pix": "financeiro@lojatechprime.com",
        "valor_total": Decimal("458.25"),
        "status": "PAGO",
        "data_prevista": "2026-04-30",
    },
    {
        "lojista_documento": "98.765.432/0001-10",
        "chave_pix": "mercadocentral@pix.com",
        "valor_total": Decimal("88.11"),
        "status": "AGENDADO",
        "data_prevista": "2026-05-02",
    },
]


def conectar_banco():
    """Abre a conexao com o PostgreSQL usando a configuracao definida no topo."""
    return psycopg2.connect(**CONFIG_BANCO)


def obter_ou_criar_lojista(cursor, nome_fantasia, documento, taxa_percentual):
    """Busca um lojista pelo documento; se nao existir, cria um novo."""
    cursor.execute(
        "SELECT lojista_id FROM lojistas WHERE documento = %s",
        (documento,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO lojistas (nome_fantasia, documento, taxa_percentual)
        VALUES (%s, %s, %s)
        RETURNING lojista_id
        """,
        (nome_fantasia, documento, taxa_percentual),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_cliente(cursor, nome, email, documento):
    """Busca um cliente pelo email e documento; se nao existir, cria um novo."""
    cursor.execute(
        """
        SELECT cliente_id
        FROM clientes
        WHERE email = %s AND documento = %s
        """,
        (email, documento),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO clientes (nome, email, documento)
        VALUES (%s, %s, %s)
        RETURNING cliente_id
        """,
        (nome, email, documento),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_metodo_pagamento(
    cursor,
    cliente_id,
    tipo,
    token_gateway,
    ultimos_4_digitos,
    bandeira,
):
    """Busca um metodo pelo token do gateway; se nao existir, cria um novo."""
    cursor.execute(
        """
        SELECT metodo_pagamento_id
        FROM metodos_pagamento
        WHERE token_gateway = %s
        """,
        (token_gateway,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO metodos_pagamento (
            cliente_id,
            tipo,
            token_gateway,
            ultimos_4_digitos,
            bandeira
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING metodo_pagamento_id
        """,
        (cliente_id, tipo, token_gateway, ultimos_4_digitos, bandeira),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_conta_bancaria(
    cursor,
    lojista_id,
    banco_codigo,
    agencia,
    conta,
    chave_pix,
):
    """Busca uma conta pelo lojista e pela chave PIX; se nao existir, cria uma nova."""
    cursor.execute(
        """
        SELECT conta_bancaria_id
        FROM contas_bancarias
        WHERE lojista_id = %s AND chave_pix = %s
        """,
        (lojista_id, chave_pix),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO contas_bancarias (
            lojista_id,
            banco_codigo,
            agencia,
            conta,
            chave_pix
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING conta_bancaria_id
        """,
        (lojista_id, banco_codigo, agencia, conta, chave_pix),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_transacao(
    cursor,
    lojista_id,
    cliente_id,
    metodo_pagamento_id,
    valor_bruto,
    valor_liquido,
    status,
    tipo_pagamento,
    payload_adquirente,
):
    """Busca uma transacao pelo payload; se nao existir, cria uma nova."""
    cursor.execute(
        """
        SELECT transacao_id
        FROM transacoes
        WHERE payload_adquirente = %s
        """,
        (payload_adquirente,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO transacoes (
            lojista_id,
            cliente_id,
            metodo_pagamento_id,
            valor_bruto,
            valor_liquido,
            status,
            tipo_pagamento,
            payload_adquirente
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING transacao_id
        """,
        (
            lojista_id,
            cliente_id,
            metodo_pagamento_id,
            valor_bruto,
            valor_liquido,
            status,
            tipo_pagamento,
            payload_adquirente,
        ),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_estorno(cursor, transacao_id, valor_estornado, motivo, status):
    """Busca um estorno pela transacao; se nao existir, cria um novo."""
    cursor.execute(
        """
        SELECT estorno_id
        FROM estornos
        WHERE transacao_id = %s
        """,
        (transacao_id,),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO estornos (transacao_id, valor_estornado, motivo, status)
        VALUES (%s, %s, %s, %s)
        RETURNING estorno_id
        """,
        (transacao_id, valor_estornado, motivo, status),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_repasse(
    cursor,
    lojista_id,
    conta_bancaria_id,
    valor_total,
    status,
    data_prevista,
):
    """Busca um repasse com os mesmos dados principais; se nao existir, cria um novo."""
    cursor.execute(
        """
        SELECT repasse_id
        FROM repasses
        WHERE lojista_id = %s
          AND conta_bancaria_id = %s
          AND valor_total = %s
          AND data_prevista = %s
        """,
        (lojista_id, conta_bancaria_id, valor_total, data_prevista),
    )
    resultado = cursor.fetchone()

    if resultado:
        return resultado[0]

    cursor.execute(
        """
        INSERT INTO repasses (
            lojista_id,
            conta_bancaria_id,
            valor_total,
            status,
            data_prevista
        )
        VALUES (%s, %s, %s, %s, %s)
        RETURNING repasse_id
        """,
        (lojista_id, conta_bancaria_id, valor_total, status, data_prevista),
    )
    return cursor.fetchone()[0]


def popular_banco(cursor):
    """
    Insere os dados ficticios em ordem correta:
    1. Lojistas
    2. Clientes
    3. Metodos de pagamento
    4. Contas bancarias
    5. Transacoes
    6. Estornos
    7. Repasses
    """
    ids_lojistas = {}
    ids_clientes = {}
    ids_metodos = {}
    ids_contas = {}
    ids_transacoes = {}

    # Cria ou reaproveita lojistas para permitir varias execucoes do script.
    for nome_fantasia, documento, taxa_percentual in LOJISTAS:
        lojista_id = obter_ou_criar_lojista(
            cursor,
            nome_fantasia,
            documento,
            taxa_percentual,
        )
        ids_lojistas[documento] = lojista_id

    # Cria ou reaproveita clientes para depois relaciona-los com pagamentos.
    for nome, email, documento in CLIENTES:
        cliente_id = obter_ou_criar_cliente(cursor, nome, email, documento)
        ids_clientes[email] = cliente_id

    # Cria ou reaproveita os cartoes e outros metodos cadastrados pelos clientes.
    for metodo in METODOS_PAGAMENTO:
        metodo_id = obter_ou_criar_metodo_pagamento(
            cursor,
            ids_clientes[metodo["cliente_email"]],
            metodo["tipo"],
            metodo["token_gateway"],
            metodo["ultimos_4_digitos"],
            metodo["bandeira"],
        )
        ids_metodos[metodo["token_gateway"]] = metodo_id

    # Cria ou reaproveita as contas bancarias dos lojistas.
    for conta in CONTAS_BANCARIAS:
        conta_id = obter_ou_criar_conta_bancaria(
            cursor,
            ids_lojistas[conta["lojista_documento"]],
            conta["banco_codigo"],
            conta["agencia"],
            conta["conta"],
            conta["chave_pix"],
        )
        ids_contas[conta["chave_pix"]] = conta_id

    # Cria ou reaproveita as transacoes que voce podera usar em SELECT com JOIN.
    for transacao in TRANSACOES:
        metodo_pagamento_id = None
        if transacao["token_gateway"]:
            metodo_pagamento_id = ids_metodos[transacao["token_gateway"]]

        transacao_id = obter_ou_criar_transacao(
            cursor,
            ids_lojistas[transacao["lojista_documento"]],
            ids_clientes[transacao["cliente_email"]],
            metodo_pagamento_id,
            transacao["valor_bruto"],
            transacao["valor_liquido"],
            transacao["status"],
            transacao["tipo_pagamento"],
            transacao["payload_adquirente"],
        )
        ids_transacoes[transacao["payload_adquirente"]] = transacao_id

    # Cria ou reaproveita o estorno vinculado a uma transacao cancelada.
    for estorno in ESTORNOS:
        obter_ou_criar_estorno(
            cursor,
            ids_transacoes[estorno["payload_adquirente"]],
            estorno["valor_estornado"],
            estorno["motivo"],
            estorno["status"],
        )

    # Cria ou reaproveita os repasses financeiros para estudo.
    for repasse in REPASSES:
        obter_ou_criar_repasse(
            cursor,
            ids_lojistas[repasse["lojista_documento"]],
            ids_contas[repasse["chave_pix"]],
            repasse["valor_total"],
            repasse["status"],
            repasse["data_prevista"],
        )


def exibir_resumo(cursor):
    """Mostra um pequeno resumo para confirmar no terminal que os dados existem."""
    consultas = {
        "lojistas": "SELECT COUNT(*) FROM lojistas",
        "clientes": "SELECT COUNT(*) FROM clientes",
        "metodos_pagamento": "SELECT COUNT(*) FROM metodos_pagamento",
        "contas_bancarias": "SELECT COUNT(*) FROM contas_bancarias",
        "transacoes": "SELECT COUNT(*) FROM transacoes",
        "estornos": "SELECT COUNT(*) FROM estornos",
        "repasses": "SELECT COUNT(*) FROM repasses",
    }

    print("\nResumo das tabelas:")
    for nome_tabela, sql in consultas.items():
        cursor.execute(sql)
        quantidade = cursor.fetchone()[0]
        print(f"- {nome_tabela}: {quantidade} registro(s)")


def main():
    """Funcao principal que conecta, popula os dados e fecha a conexao."""
    connection = None
    cursor = None

    try:
        # Abre a conexao com o banco.
        connection = conectar_banco()

        # Cria o cursor, que sera usado para executar os comandos SQL.
        cursor = connection.cursor()

        # Insere os dados ficticios de forma organizada e sem duplicar seeds.
        popular_banco(cursor)

        # Salva as alteracoes no banco.
        connection.commit()
        print("Dados ficticios inseridos ou reaproveitados com sucesso.")

        # Exibe um resumo simples para voce validar pelo terminal.
        exibir_resumo(cursor)

    except (Exception, Error) as error:
        # Em caso de erro, desfaz as alteracoes pendentes para manter consistencia.
        if connection:
            connection.rollback()
        print("Erro ao popular o PostgreSQL:", error)

    finally:
        # Fecha o cursor primeiro, pois ele depende da conexao aberta.
        if cursor:
            cursor.close()

        # Fecha a conexao com o banco ao final do processo.
        if connection:
            connection.close()
            print("\nConexao encerrada.")


# Executa o script apenas quando o arquivo for chamado diretamente.
if __name__ == "__main__":
    main()
