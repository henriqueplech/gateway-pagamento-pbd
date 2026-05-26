-- ============================================================
--  DESAFIO 1 — LEFT JOIN
-- ============================================================
--
--  ENUNCIADO:
--  Liste todos os clientes e seus pedidos (transações).
--  Inclua os clientes que NÃO fizeram pedidos.
-- ============================================================


-- ============================================================
--  O QUE É O LEFT JOIN?  (explicação para quem tem 10 anos 😄)
-- ============================================================
--
--  Imagine que você tem duas listas de papel:
--
--  📋 Lista da ESQUERDA = todos os clientes cadastrados
--     1. Ana Lima
--     2. Bruno Costa
--     3. Carla Souza
--
--  📋 Lista da DIREITA = todas as transações que já foram feitas
--     (seed_tx_001) Ana Lima   → R$ 150,00  APROVADA
--     (seed_tx_002) Bruno Costa → R$ 89,90  APROVADA
--     (seed_tx_003) Carla Souza → R$ 42,50  PENDENTE
--     (seed_tx_004) Bruno Costa → R$ 320,00 CANCELADA
--
--  O LEFT JOIN diz assim:
--  "Pega TODOS da lista da ESQUERDA (clientes).
--   Para cada um deles, tenta encontrar algo na lista da DIREITA.
--   Se achar → ótimo, mostra os dois juntos!
--   Se NÃO achar → tudo bem, mostra o cliente mesmo assim,
--                  só deixa o lado direito em branco (NULL)."
--
--  Por isso o nome LEFT (esquerda): a lista da ESQUERDA nunca
--  fica de fora, aconteça o que acontecer!
--
-- ============================================================
--  DIAGRAMA VISUAL:
--
--     clientes          transacoes
--    ┌──────────┐      ┌────────────┐
--    │ Ana Lima │◄────►│ tx_001     │  ← achou! aparece junto
--    │ Bruno    │◄────►│ tx_002     │  ← achou! aparece junto
--    │ Bruno    │◄────►│ tx_004     │  ← achou! aparece junto
--    │ Carla    │◄────►│ tx_003     │  ← achou! aparece junto
--    └──────────┘      └────────────┘
--
--  * Se existisse um cliente "Daniel" SEM transação, ele apareceria
--    assim na linha:  Daniel | NULL | NULL | NULL | NULL ...
--    (os campos da tabela transacoes ficam vazios = NULL)
--
-- ============================================================


-- ============================================================
--  SOLUÇÃO — seguindo o padrão do slide
-- ============================================================

SELECT clientes.nome, transacoes.transacao_id, transacoes.valor_bruto
FROM clientes
LEFT JOIN transacoes
ON clientes.cliente_id = transacoes.cliente_id;


-- ============================================================
--  EXPLICAÇÃO LINHA POR LINHA:
--
--  SELECT clientes.nome          → pega o nome do cliente
--         transacoes.transacao_id → pega o número da transação
--         transacoes.valor_bruto  → pega o valor cobrado
--
--  FROM clientes                 → começa pela tabela da ESQUERDA
--
--  LEFT JOIN transacoes          → junta com a tabela da DIREITA,
--                                  mas mantendo TODOS os clientes
--
--  ON clientes.cliente_id        → a "ponte" entre as duas tabelas:
--     = transacoes.cliente_id      o campo cliente_id precisa ser
--                                  igual nos dois lados para juntar
-- ============================================================


-- ============================================================
--  RESULTADO ESPERADO COM OS DADOS DO NOSSO BANCO:
--
--  nome         | transacao_id | valor_bruto
--  -------------|--------------|------------
--  Ana Lima     |      1       |   150.00     ← tem transação ✅
--  Bruno Costa  |      2       |    89.90     ← tem transação ✅
--  Bruno Costa  |      4       |   320.00     ← tem 2 transações ✅
--  Carla Souza  |      3       |    42.50     ← tem transação ✅
--
--  ⚠️  No nosso banco todos os clientes têm transação.
--     Mas se houvesse um cliente sem pedido, a linha seria:
--
--  Daniel Silva |    NULL      |    NULL      ← sem transação ⚠️
--
-- ============================================================
