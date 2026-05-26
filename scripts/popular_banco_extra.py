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


# Lista de NOVOS lojistas ficticios para testes.
LOJISTAS = [
    ("Loja Geek Universe", "55.444.333/0001-22", Decimal("3.00")),
    ("Livraria do Saber", "44.555.666/0001-33", Decimal("2.00")),
]

# Lista de NOVOS clientes ficticios.
CLIENTES = [
    # Este cliente fará transações normalmente
    ("Daniel Oliveira", "daniel.oliveira@email.com", "111.222.333-44"),
    
    # Este cliente NÃO TERÁ NENHUMA TRANSAÇÃO. 
    # Isso forçará o FULL OUTER JOIN a mostrar 'NULL' nas colunas de transações para este cliente!
    ("Fernanda Lima", "fernanda.lima@email.com", "555.666.777-88"),
]

# Metodos de pagamento para os novos clientes
METODOS_PAGAMENTO = [
    {
        "cliente_email": "daniel.oliveira@email.com",
        "tipo": "CARTAO_CREDITO",
        "token_gateway": "tok_daniel_visa_001",
        "ultimos_4_digitos": "5555",
        "bandeira": "VISA",
    },
]

# Contas bancarias
CONTAS_BANCARIAS = [
    {
        "lojista_documento": "55.444.333/0001-22",
        "banco_codigo": "341",
        "agencia": "4004",
        "conta": "55555-5",
        "chave_pix": "financeiro@geekuniverse.com",
    },
]

# Novas Transacoes
TRANSACOES = [
    {
        "lojista_documento": "55.444.333/0001-22",
        "cliente_email": "daniel.oliveira@email.com",
        "token_gateway": "tok_daniel_visa_001",
        "valor_bruto": Decimal("250.00"),
        "valor_liquido": Decimal("242.50"),
        "status": "APROVADA",
        "tipo_pagamento": "CARTAO",
        "payload_adquirente": "seed_tx_005",
    },
    {
        "lojista_documento": "44.555.666/0001-33",
        "cliente_email": "daniel.oliveira@email.com",
        "token_gateway": None,
        "valor_bruto": Decimal("85.00"),
        "valor_liquido": Decimal("83.30"),
        "status": "PENDENTE",
        "tipo_pagamento": "PIX",
        "payload_adquirente": "seed_tx_006",
    },
    # TRANSAÇÃO SEM CLIENTE VINCULADO (Guest checkout). 
    # Se a estrutura do banco permitir cliente_id NULL, isso fará o FULL OUTER JOIN 
    # mostrar 'NULL' nas colunas do cliente!
    {
        "lojista_documento": "55.444.333/0001-22",
        "cliente_email": None, 
        "token_gateway": None,
        "valor_bruto": Decimal("15.90"),
        "valor_liquido": Decimal("15.42"),
        "status": "APROVADA",
        "tipo_pagamento": "PIX",
        "payload_adquirente": "seed_tx_007",
    },
]

ESTORNOS = []
REPASSES = []

def conectar_banco():
    return psycopg2.connect(**CONFIG_BANCO)

def obter_ou_criar_lojista(cursor, nome_fantasia, documento, taxa_percentual):
    cursor.execute("SELECT lojista_id FROM lojistas WHERE documento = %s", (documento,))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]

    cursor.execute(
        """INSERT INTO lojistas (nome_fantasia, documento, taxa_percentual)
           VALUES (%s, %s, %s) RETURNING lojista_id""",
        (nome_fantasia, documento, taxa_percentual),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_cliente(cursor, nome, email, documento):
    cursor.execute("SELECT cliente_id FROM clientes WHERE email = %s AND documento = %s", (email, documento))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]

    cursor.execute(
        """INSERT INTO clientes (nome, email, documento)
           VALUES (%s, %s, %s) RETURNING cliente_id""",
        (nome, email, documento),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_metodo_pagamento(cursor, cliente_id, tipo, token_gateway, ultimos_4_digitos, bandeira):
    cursor.execute("SELECT metodo_pagamento_id FROM metodos_pagamento WHERE token_gateway = %s", (token_gateway,))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]

    cursor.execute(
        """INSERT INTO metodos_pagamento (cliente_id, tipo, token_gateway, ultimos_4_digitos, bandeira)
           VALUES (%s, %s, %s, %s, %s) RETURNING metodo_pagamento_id""",
        (cliente_id, tipo, token_gateway, ultimos_4_digitos, bandeira),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_conta_bancaria(cursor, lojista_id, banco_codigo, agencia, conta, chave_pix):
    cursor.execute("SELECT conta_bancaria_id FROM contas_bancarias WHERE lojista_id = %s AND chave_pix = %s", (lojista_id, chave_pix))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]

    cursor.execute(
        """INSERT INTO contas_bancarias (lojista_id, banco_codigo, agencia, conta, chave_pix)
           VALUES (%s, %s, %s, %s, %s) RETURNING conta_bancaria_id""",
        (lojista_id, banco_codigo, agencia, conta, chave_pix),
    )
    return cursor.fetchone()[0]


def obter_ou_criar_transacao(cursor, lojista_id, cliente_id, metodo_pagamento_id, valor_bruto, valor_liquido, status, tipo_pagamento, payload_adquirente):
    cursor.execute("SELECT transacao_id FROM transacoes WHERE payload_adquirente = %s", (payload_adquirente,))
    resultado = cursor.fetchone()
    if resultado: return resultado[0]

    cursor.execute(
        """INSERT INTO transacoes (lojista_id, cliente_id, metodo_pagamento_id, valor_bruto, valor_liquido, status, tipo_pagamento, payload_adquirente)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING transacao_id""",
        (lojista_id, cliente_id, metodo_pagamento_id, valor_bruto, valor_liquido, status, tipo_pagamento, payload_adquirente),
    )
    return cursor.fetchone()[0]


def popular_banco(cursor):
    ids_lojistas = {}
    ids_clientes = {}
    ids_metodos = {}
    ids_contas = {}

    for nome_fantasia, documento, taxa_percentual in LOJISTAS:
        ids_lojistas[documento] = obter_ou_criar_lojista(cursor, nome_fantasia, documento, taxa_percentual)

    for nome, email, documento in CLIENTES:
        ids_clientes[email] = obter_ou_criar_cliente(cursor, nome, email, documento)

    for metodo in METODOS_PAGAMENTO:
        ids_metodos[metodo["token_gateway"]] = obter_ou_criar_metodo_pagamento(
            cursor, ids_clientes[metodo["cliente_email"]], metodo["tipo"], 
            metodo["token_gateway"], metodo["ultimos_4_digitos"], metodo["bandeira"]
        )

    for conta in CONTAS_BANCARIAS:
        ids_contas[conta["chave_pix"]] = obter_ou_criar_conta_bancaria(
            cursor, ids_lojistas[conta["lojista_documento"]], conta["banco_codigo"], 
            conta["agencia"], conta["conta"], conta["chave_pix"]
        )

    for transacao in TRANSACOES:
        metodo_pagamento_id = None
        if transacao["token_gateway"]:
            metodo_pagamento_id = ids_metodos[transacao["token_gateway"]]
            
        cliente_id = None
        if transacao["cliente_email"]:
            cliente_id = ids_clientes[transacao["cliente_email"]]

        try:
            # Pula a transação sem cliente se ela tiver email = None,
            # pois sabemos que o banco não aceita cliente_id nulo.
            if transacao["payload_adquirente"] == "seed_tx_007":
                print("Aviso: Ignorando a transação seed_tx_007 pois a tabela transacoes não aceita cliente_id nulo.")
                continue

            obter_ou_criar_transacao(
                cursor,
                ids_lojistas[transacao["lojista_documento"]],
                cliente_id, # Pode ser None
                metodo_pagamento_id,
                transacao["valor_bruto"],
                transacao["valor_liquido"],
                transacao["status"],
                transacao["tipo_pagamento"],
                transacao["payload_adquirente"],
            )
        except Exception as e:
            print(f"Aviso: Nao foi possivel inserir a transacao {transacao['payload_adquirente']} "
                  f"(talvez a coluna cliente_id nao aceite nulos?). Erro: {e}")
            cursor.connection.rollback()

def main():
    connection = None
    cursor = None
    try:
        connection = conectar_banco()
        cursor = connection.cursor()
        popular_banco(cursor)
        connection.commit()
        print("Dados ficticios (teste 2) inseridos com sucesso.")
    except (Exception, Error) as error:
        if connection: connection.rollback()
        print("Erro ao popular o PostgreSQL:", error)
    finally:
        if cursor: cursor.close()
        if connection:
            connection.close()
            print("Conexao encerrada.")

if __name__ == "__main__":
    main()
