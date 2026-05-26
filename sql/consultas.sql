-- Deve retornar as 4 tabelas relevantes para a AV03
SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
  AND table_name IN ('usuarios', 'clientes', 'transacoes', 'lojistas')
ORDER BY table_name;


-- Ver usuários cadastrados (senhas aparecem como hash, nunca texto puro)
SELECT * FROM usuarios;
-- Ver clientes inseridos pelo CRUD
SELECT * FROM clientes;
-- Ver os dois juntos em contexto real (JOIN para a sabatina!)
SELECT 
    u.nome        AS usuario_sistema,
    u.email       AS email_login,
    c.nome        AS cliente_cadastrado,
    c.documento   AS cpf
FROM usuarios u
LEFT JOIN clientes c ON u.email = c.email;


-- ============================================================
-- ARQUIVO DE ESTUDO: CONSULTAS SQL PARA O GATEWAY DE PAGAMENTO
-- ============================================================
--
-- Antes de executar estas consultas, rode o arquivo `teste1.py`
-- para garantir que o banco tenha os dados ficticios de apoio.
--
-- Banco esperado:
--   postgres
--
-- Tabelas usadas:
--   lojistas
--   clientes
--   metodos_pagamento
--   transacoes
--   estornos
--   contas_bancarias
--   repasses


-- ============================================================
-- 1. SELECT BASICO
-- ============================================================

-- 1.1 Ver todos os lojistas cadastrados.
SELECT *
FROM lojistas;


-- 1.2 Ver apenas algumas colunas dos clientes.
SELECT cliente_id, nome, email
FROM clientes;


-- 1.3 Filtrar transacoes aprovadas.
SELECT transacao_id, valor_bruto, valor_liquido, status
FROM transacoes
WHERE status = 'APROVADA';


-- 1.4 Filtrar transacoes por tipo de pagamento.
SELECT transacao_id, tipo_pagamento, valor_bruto
FROM transacoes
WHERE tipo_pagamento = 'CARTAO';


-- ============================================================
-- 2. ORDER BY
-- ============================================================

-- 2.1 Ordenar clientes em ordem alfabetica.
SELECT cliente_id, nome, email
FROM clientes
ORDER BY nome ASC;


-- 2.2 Mostrar as maiores transacoes primeiro.
SELECT transacao_id, valor_bruto, status
FROM transacoes
ORDER BY valor_bruto DESC;


-- 2.3 Ordenar os repasses pela data prevista.
SELECT repasse_id, valor_total, status, data_prevista
FROM repasses
ORDER BY data_prevista ASC;


-- ============================================================
-- 3. JOIN
-- ============================================================

-- 3.1 Mostrar cada transacao com o nome do cliente e do lojista.
SELECT
    t.transacao_id,
    c.nome AS cliente,
    l.nome_fantasia AS lojista,
    t.valor_bruto,
    t.valor_liquido,
    t.status,
    t.tipo_pagamento
FROM transacoes t
JOIN clientes c ON c.cliente_id = t.cliente_id
JOIN lojistas l ON l.lojista_id = t.lojista_id
ORDER BY t.transacao_id;


-- 3.2 Mostrar os metodos de pagamento cadastrados por cliente.
SELECT
    c.nome AS cliente,
    mp.tipo,
    mp.bandeira,
    mp.ultimos_4_digitos
FROM metodos_pagamento mp
JOIN clientes c ON c.cliente_id = mp.cliente_id
ORDER BY c.nome;


-- 3.3 Mostrar os repasses com o nome do lojista e a chave PIX utilizada.
SELECT
    r.repasse_id,
    l.nome_fantasia AS lojista,
    cb.chave_pix,
    r.valor_total,
    r.status,
    r.data_prevista
FROM repasses r
JOIN lojistas l ON l.lojista_id = r.lojista_id
JOIN contas_bancarias cb ON cb.conta_bancaria_id = r.conta_bancaria_id
ORDER BY r.data_prevista;


-- 3.4 LEFT JOIN para ver todas as transacoes, incluindo as que nao possuem estorno.
SELECT
    t.transacao_id,
    t.status AS status_transacao,
    t.valor_bruto,
    e.estorno_id,
    e.valor_estornado,
    e.status AS status_estorno
FROM transacoes t
LEFT JOIN estornos e ON e.transacao_id = t.transacao_id
ORDER BY t.transacao_id;


-- ============================================================
-- 4. GROUP BY
-- ============================================================

-- 4.1 Contar quantas transacoes existem por status.
SELECT
    status,
    COUNT(*) AS quantidade
FROM transacoes
GROUP BY status
ORDER BY quantidade DESC;


-- 4.2 Somar o valor bruto transacionado por lojista.
SELECT
    l.nome_fantasia AS lojista,
    SUM(t.valor_bruto) AS total_bruto
FROM transacoes t
JOIN lojistas l ON l.lojista_id = t.lojista_id
GROUP BY l.nome_fantasia
ORDER BY total_bruto DESC;


-- 4.3 Somar o valor liquido apenas das transacoes aprovadas por lojista.
SELECT
    l.nome_fantasia AS lojista,
    SUM(t.valor_liquido) AS total_liquido_aprovado
FROM transacoes t
JOIN lojistas l ON l.lojista_id = t.lojista_id
WHERE t.status = 'APROVADA'
GROUP BY l.nome_fantasia
ORDER BY total_liquido_aprovado DESC;


-- ============================================================
-- 5. HAVING
-- ============================================================

-- 5.1 Mostrar apenas lojistas cuja soma de valor bruto seja maior que 100.
SELECT
    l.nome_fantasia AS lojista,
    SUM(t.valor_bruto) AS total_bruto
FROM transacoes t
JOIN lojistas l ON l.lojista_id = t.lojista_id
GROUP BY l.nome_fantasia
HAVING SUM(t.valor_bruto) > 100
ORDER BY total_bruto DESC;


-- 5.2 Mostrar apenas status com mais de uma transacao.
SELECT
    status,
    COUNT(*) AS quantidade
FROM transacoes
GROUP BY status
HAVING COUNT(*) > 1
ORDER BY quantidade DESC;


-- ============================================================
-- 6. SUBQUERIES
-- ============================================================

-- 6.1 Transacoes com valor bruto acima da media geral.
SELECT
    transacao_id,
    valor_bruto,
    status
FROM transacoes
WHERE valor_bruto > (
    SELECT AVG(valor_bruto)
    FROM transacoes
)
ORDER BY valor_bruto DESC;


-- 6.2 Clientes que possuem pelo menos uma transacao aprovada.
SELECT
    cliente_id,
    nome,
    email
FROM clientes
WHERE cliente_id IN (
    SELECT cliente_id
    FROM transacoes
    WHERE status = 'APROVADA'
)
ORDER BY nome;


-- 6.3 Lojistas que tiveram transacoes canceladas.
SELECT
    lojista_id,
    nome_fantasia,
    documento
FROM lojistas
WHERE lojista_id IN (
    SELECT lojista_id
    FROM transacoes
    WHERE status = 'CANCELADA'
)
ORDER BY nome_fantasia;


-- 6.4 Mostrar as transacoes que possuem o maior valor bruto do sistema.
SELECT
    transacao_id,
    valor_bruto,
    status
FROM transacoes
WHERE valor_bruto = (
    SELECT MAX(valor_bruto)
    FROM transacoes
);


-- ============================================================
-- 7. CONSULTAS UM POUCO MAIS COMPLETAS
-- ============================================================

-- 7.1 Relatorio de transacoes com varias informacoes relacionadas.
SELECT
    t.transacao_id,
    l.nome_fantasia AS lojista,
    c.nome AS cliente,
    COALESCE(mp.bandeira, 'SEM CARTAO') AS bandeira,
    t.tipo_pagamento,
    t.valor_bruto,
    t.valor_liquido,
    t.status
FROM transacoes t
JOIN lojistas l ON l.lojista_id = t.lojista_id
JOIN clientes c ON c.cliente_id = t.cliente_id
LEFT JOIN metodos_pagamento mp
    ON mp.metodo_pagamento_id = t.metodo_pagamento_id
ORDER BY t.transacao_id;


-- 7.2 Total de transacoes e valor bruto por cliente.
SELECT
    c.nome AS cliente,
    COUNT(t.transacao_id) AS qtd_transacoes,
    SUM(t.valor_bruto) AS total_gasto
FROM clientes c
JOIN transacoes t ON t.cliente_id = c.cliente_id
GROUP BY c.nome
ORDER BY total_gasto DESC;


-- 7.3 Lojistas cujo total liquido aprovado esta acima da media dos lojistas.
SELECT
    resumo.lojista,
    resumo.total_liquido
FROM (
    SELECT
        l.nome_fantasia AS lojista,
        SUM(t.valor_liquido) AS total_liquido
    FROM transacoes t
    JOIN lojistas l ON l.lojista_id = t.lojista_id
    WHERE t.status = 'APROVADA'
    GROUP BY l.nome_fantasia
) AS resumo
WHERE resumo.total_liquido > (
    SELECT AVG(sub.total_liquido)
    FROM (
        SELECT SUM(t2.valor_liquido) AS total_liquido
        FROM transacoes t2
        WHERE t2.status = 'APROVADA'
        GROUP BY t2.lojista_id
    ) AS sub
)
ORDER BY resumo.total_liquido DESC;
