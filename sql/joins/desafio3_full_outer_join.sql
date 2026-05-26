-- ============================================================
-- DESAFIO 3 — FULL OUTER JOIN
-- ============================================================
-- Enunciado:
--   Mostre uma lista de todos os clientes e pedidos (transações),
--   independentemente de haver correspondências entre eles.
--
-- Por que FULL OUTER JOIN?
--   O FULL OUTER JOIN combina o LEFT JOIN e o RIGHT JOIN:
--   retorna TODOS os registros de AMBAS as tabelas.
--   Onde não houver correspondência em qualquer lado, as colunas
--   da tabela oposta aparecem como NULL.
--
-- Diagrama conceitual:
--
--   clientes  ←──────────────→  transacoes
--   (todos)    FULL OUTER JOIN   (todos)
--
-- Equivalência lógica:
--   FULL OUTER JOIN  =  LEFT JOIN  UNION  RIGHT JOIN
-- ============================================================

SELECT
    -- Colunas do cliente (NULL se a transação não tiver cliente)
    c.cliente_id,
    c.nome                          AS nome_cliente,
    c.email,

    -- Colunas da transação (NULL se o cliente não tiver transação)
    t.transacao_id,
    t.valor_bruto,
    t.valor_liquido,
    t.tipo_pagamento,
    t.status                        AS status_transacao,
    t.criado_em                     AS data_transacao
FROM
    clientes AS c                       -- tabela da ESQUERDA
FULL OUTER JOIN
    transacoes AS t                     -- tabela da DIREITA
    ON c.cliente_id = t.cliente_id      -- condição de junção
ORDER BY
    c.nome NULLS LAST,
    t.transacao_id NULLS LAST;

-- ============================================================
-- O QUE ESPERAR NO RESULTADO:
--   • Cliente COM transação        → linha com dados dos dois lados
--   • Cliente SEM transação        → linha com colunas de transacoes = NULL
--   • Transação SEM cliente        → linha com colunas de clientes = NULL
--
-- DICA DE ESTUDO — Comparação rápida dos JOINs:
--   INNER JOIN       → somente linhas com correspondência nos dois lados
--   LEFT JOIN        → todos da ESQUERDA + correspondências da direita
--   RIGHT JOIN       → todos da DIREITA  + correspondências da esquerda
--   FULL OUTER JOIN  → todos dos DOIS lados, com ou sem correspondência
-- ============================================================
