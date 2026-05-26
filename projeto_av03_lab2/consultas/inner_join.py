# INNER JOIN - Transacoes com dados do cliente e do lojista.
# So retorna linhas que possuem correspondencia em todas as tabelas.

from projeto_av03_lab2.database import obter_cursor


SQL_INNER_JOIN = """
    SELECT
        t.transacao_id,
        c.nome              AS cliente,
        l.nome_fantasia     AS lojista,
        t.valor_bruto,
        t.valor_liquido,
        t.status,
        t.tipo_pagamento,
        t.criado_em         AS data_transacao
    FROM transacoes t
    INNER JOIN clientes c ON c.cliente_id = t.cliente_id
    INNER JOIN lojistas l ON l.lojista_id = t.lojista_id
    ORDER BY t.transacao_id
"""


def executar():
    """Executa o INNER JOIN e exibe os resultados."""
    print("\n" + "=" * 100)
    print("  INNER JOIN - Transacoes com cliente e lojista")
    print("=" * 100)
    print("  So aparecem transacoes que possuem cliente E lojista validos.")
    print("-" * 100)

    try:
        with obter_cursor(auto_commit=False) as (conn, cursor):
            cursor.execute(SQL_INNER_JOIN)
            resultados = cursor.fetchall()

            if resultados:
                print(f"\n{'ID':<5} {'Cliente':<20} {'Lojista':<25} {'Bruto':>12} "
                      f"{'Liquido':>12} {'Status':<12} {'Tipo':<8} {'Data'}")
                print("-" * 100)
                for r in resultados:
                    print(f"{r[0]:<5} {r[1]:<20} {r[2]:<25} {r[3]:>12.2f} "
                          f"{r[4]:>12.2f} {r[5]:<12} {r[6]:<8} {r[7]}")
            else:
                print("Nenhum resultado encontrado.")

            print(f"\n  Total de registros: {len(resultados)}")

    except Exception as e:
        print(f"Erro ao executar INNER JOIN: {e}")

    print("=" * 100)
