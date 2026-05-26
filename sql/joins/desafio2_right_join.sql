-- ============================================================
-- DESAFIO 2 — RIGHT JOIN
-- ============================================================
-- Enunciado:
--   Liste todos os pedidos (transações) e os respectivos clientes.
--   Inclua os pedidos que NÃO têm clientes correspondentes.
--
-- Por que RIGHT JOIN?
--   O RIGHT JOIN retorna TODOS os registros da tabela da DIREITA
--   (transacoes) e, quando houver correspondência, os dados da
--   tabela da ESQUERDA (clientes). Quando uma transação não possui
--   cliente vinculado, as colunas de clientes aparecem como NULL.
--
-- Diagrama conceitual:
--
--   clientes  ────────────────→  transacoes
--   (somente os que batem)  RIGHT JOIN  (todas)
--
-- Obs.: RIGHT JOIN é o espelho do LEFT JOIN.
--       A consulta abaixo equivale a fazer:
--         FROM transacoes LEFT JOIN clientes ...
-- ============================================================

SELECT
    t.transacao_id,
    t.valor_bruto,
    t.valor_liquido,
    t.tipo_pagamento,
    t.status                        AS status_transacao,
    t.criado_em                     AS data_transacao,
    c.cliente_id,
    c.nome                          AS nome_cliente,
    c.email
FROM
    clientes AS c                   -- tabela da ESQUERDA
RIGHT JOIN
    transacoes AS t                 -- tabela da DIREITA (base — todos aparecem)
    ON c.cliente_id = t.cliente_id  -- condição de junção
ORDER BY
    t.transacao_id;

-- ============================================================
-- O QUE ESPERAR NO RESULTADO:
--   • Transações COM cliente   → aparecem com todos os dados
--   • Transações SEM cliente   → aparecem com cliente_id = NULL
--                                e demais colunas de clientes = NULL
--                                (situação incomum neste schema pois
--                                 cliente_id em transacoes é NOT NULL,
--                                 mas o conceito continua válido para estudo)
-- ============================================================
