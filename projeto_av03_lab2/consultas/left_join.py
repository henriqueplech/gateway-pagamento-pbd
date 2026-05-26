# LEFT JOIN - Todos os clientes, com ou sem transacoes.
# Se um cliente nao tiver transacao, as colunas da direita ficam NULL.

from projeto_av03_lab2.database import obter_cursor


SQL_LEFT_JOIN = """
    SELECT
        c.cliente_id,
        c.nome              AS cliente,
        c.email,
        t.transacao_id,
        t.valor_bruto,
        t.status            AS status_transacao,
        t.tipo_pagamento
    FROM clientes c
    LEFT JOIN transacoes t ON c.cliente_id = t.cliente_id
    ORDER BY c.nome, t.transacao_id
"""


def executar():
    """Executa o LEFT JOIN e exibe os resultados."""
    print("\n" + "=" * 110)
    print("  LEFT JOIN - Todos os clientes (com ou sem transacoes)")
    print("=" * 110)
    print("  Clientes sem transacao aparecem com valores NULL nas colunas da direita.")
    print("-" * 110)

    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            cursor.execute(SQL_LEFT_JOIN)
            resultados = cursor.fetchall()

            if resultados:
                print(f"\n{'ID':<5} {'Cliente':<20} {'Email':<30} {'Tx ID':<8} "
                      f"{'Valor Bruto':>12} {'Status':<12} {'Tipo'}")
                print("-" * 110)
                for r in resultados:
                    tx_id = str(r[3]) if r[3] is not None else "NULL"
                    valor = f"{r[4]:.2f}" if r[4] is not None else "NULL"
                    status = r[5] if r[5] is not None else "NULL"
                    tipo = r[6] if r[6] is not None else "NULL"
                    marcador = "  << sem transacao" if r[3] is None else ""
                    print(f"{r[0]:<5} {r[1]:<20} {r[2]:<30} {tx_id:<8} "
                          f"{valor:>12} {status:<12} {tipo}{marcador}")
            else:
                print("Nenhum resultado encontrado.")

            print(f"\n  Total de registros: {len(resultados)}")

    except Exception as e:
        print(f"Erro ao executar LEFT JOIN: {e}")

    print("=" * 110)
