-- =============================================
-- GATEWAY DE PAGAMENTO - Scripts DDL
-- Projeto de Banco de Dados
-- =============================================


-- ===============================
-- TABELA: lojistas
-- ===============================
CREATE TABLE lojistas (
    lojista_id      SERIAL          PRIMARY KEY,
    nome_fantasia   VARCHAR(150)    NOT NULL,
    documento       VARCHAR(18)     NOT NULL UNIQUE,  -- CNPJ ou CPF
    taxa_percentual NUMERIC(5,2)    NOT NULL,          -- Ex: 2.50
    criado_em       TIMESTAMP       DEFAULT NOW()
);


-- ===============================
-- TABELA: clientes
-- ===============================
CREATE TABLE clientes (
    cliente_id  SERIAL          PRIMARY KEY,
    nome        VARCHAR(150)    NOT NULL,
    email       VARCHAR(150)    NOT NULL,
    documento   VARCHAR(14)     NOT NULL,              -- CPF
    criado_em   TIMESTAMP       DEFAULT NOW()
);


-- ===============================
-- TABELA: metodos_pagamento
-- ===============================
CREATE TABLE metodos_pagamento (
    metodo_pagamento_id SERIAL          PRIMARY KEY,
    cliente_id          INT             NOT NULL REFERENCES clientes(cliente_id),
    tipo                VARCHAR(50),                   -- Ex: CARTAO_CREDITO
    token_gateway       VARCHAR(255)    NOT NULL,
    ultimos_4_digitos   VARCHAR(4),
    bandeira            VARCHAR(20)                    -- VISA, MASTERCARD, etc
);


-- ===============================
-- TABELA: transacoes
-- ===============================
CREATE TABLE transacoes (
    transacao_id        SERIAL          PRIMARY KEY,
    lojista_id          INT             NOT NULL REFERENCES lojistas(lojista_id),
    cliente_id          INT             NOT NULL REFERENCES clientes(cliente_id),
    metodo_pagamento_id INT             REFERENCES metodos_pagamento(metodo_pagamento_id),
    valor_bruto         NUMERIC(12,2)   NOT NULL,
    valor_liquido       NUMERIC(12,2)   NOT NULL,      -- Valor apos taxa do gateway
    status              VARCHAR(20),                   -- PENDENTE, APROVADA, RECUSADA, CANCELADA
    tipo_pagamento      VARCHAR(20),                   -- PIX, BOLETO, CARTAO
    payload_adquirente  TEXT,
    criado_em           TIMESTAMP       DEFAULT NOW()
);


-- ===============================
-- TABELA: estornos
-- ===============================
CREATE TABLE estornos (
    estorno_id      SERIAL          PRIMARY KEY,
    transacao_id    INT             NOT NULL UNIQUE REFERENCES transacoes(transacao_id),
    valor_estornado NUMERIC(12,2)   NOT NULL,
    motivo          TEXT,
    status          VARCHAR(20),                       -- PROCESSANDO, CONCLUIDO, FALHOU
    criado_em       TIMESTAMP       DEFAULT NOW()
);


-- ===============================
-- TABELA: contas_bancarias
-- ===============================
CREATE TABLE contas_bancarias (
    conta_bancaria_id   SERIAL          PRIMARY KEY,
    lojista_id          INT             NOT NULL REFERENCES lojistas(lojista_id),
    banco_codigo        VARCHAR(10),
    agencia             VARCHAR(10),
    conta               VARCHAR(20),
    chave_pix           VARCHAR(150)
);


-- ===============================
-- TABELA: repasses
-- ===============================
CREATE TABLE repasses (
    repasse_id          SERIAL          PRIMARY KEY,
    lojista_id          INT             NOT NULL REFERENCES lojistas(lojista_id),
    conta_bancaria_id   INT             NOT NULL REFERENCES contas_bancarias(conta_bancaria_id),
    valor_total         NUMERIC(12,2)   NOT NULL,
    status              VARCHAR(20),                   -- AGENDADO, PROCESSANDO, PAGO, FALHOU
    data_prevista       DATE,
    criado_em           TIMESTAMP       DEFAULT NOW()
);