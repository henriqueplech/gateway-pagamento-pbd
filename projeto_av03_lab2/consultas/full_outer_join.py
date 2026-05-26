# FULL OUTER JOIN - Todos os clientes x Todas as transacoes.
# Retorna todos os registros de ambos os lados, com ou sem correspondencia.

from projeto_av03_lab2.database import obter_cursor


SQL_FULL_OUTER_JOIN = """
    SELECT
        c.cliente_id,
        c.nome              AS nome_cliente,
        c.email,
        t.transacao_id,
        t.valor_bruto,
        t.valor_liquido,
        t.tipo_pagamento,
        t.status            AS status_transacao,
        t.criado_em         AS data_transacao
    FROM clientes c
    FULL OUTER JOIN transacoes t ON c.cliente_id = t.cliente_id
    ORDER BY
        c.nome NULLS LAST,
        t.transacao_id NULLS LAST
"""


def executar():
    """Executa o FULL OUTER JOIN e exibe os resultados."""
    print("\n" + "=" * 115)
    print("  FULL OUTER JOIN - Todos os clientes x Todas as transacoes")
    print("=" * 115)
    print("  Mostra TODOS os registros de ambos os lados, com ou sem correspondencia.")
    print("-" * 115)

    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            cursor.execute(SQL_FULL_OUTER_JOIN)
            resultados = cursor.fetchall()

            if resultados:
                print(f"\n{'Cli ID':<8} {'Cliente':<20} {'Email':<28} {'Tx ID':<8} "
                      f"{'Bruto':>10} {'Liquido':>10} {'Tipo':<8} {'Status':<12} {'Data'}")
                print("-" * 115)

                sem_transacao = 0
                sem_cliente = 0

                for r in resultados:
                    cli_id = str(r[0]) if r[0] is not None else "NULL"
                    nome = r[1] if r[1] is not None else "NULL"
                    email = r[2] if r[2] is not None else "NULL"
                    tx_id = str(r[3]) if r[3] is not None else "NULL"
                    bruto = f"{r[4]:.2f}" if r[4] is not None else "NULL"
                    liquido = f"{r[5]:.2f}" if r[5] is not None else "NULL"
                    tipo = r[6] if r[6] is not None else "NULL"
                    status = r[7] if r[7] is not None else "NULL"
                    data = str(r[8]) if r[8] is not None else "NULL"

                    marcador = ""
                    if r[3] is None and r[0] is not None:
                        marcador = " << sem transacao"
                        sem_transacao += 1
                    elif r[0] is None and r[3] is not None:
                        marcador = " << sem cliente"
                        sem_cliente += 1

                    print(f"{cli_id:<8} {nome:<20} {email:<28} {tx_id:<8} "
                          f"{bruto:>10} {liquido:>10} {tipo:<8} {status:<12} {data}{marcador}")

                print(f"\n  Total de registros: {len(resultados)}")
                if sem_transacao > 0:
                    print(f"  Clientes sem transacao: {sem_transacao}")
                if sem_cliente > 0:
                    print(f"  Transacoes sem cliente: {sem_cliente}")
            else:
                print("Nenhum resultado encontrado.")

    except Exception as e:
        print(f"Erro ao executar FULL OUTER JOIN: {e}")

    print("=" * 115)
