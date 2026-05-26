-- =============================================
-- AV03 - Adicionar tabela de usuarios
-- Rodar APENAS UMA VEZ no banco gateway_pagamento
-- Não precisa recriar as tabelas existentes!
-- =============================================

CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id  SERIAL          PRIMARY KEY,
    nome        VARCHAR(150)    NOT NULL,
    email       VARCHAR(150)    NOT NULL UNIQUE,
    senha       VARCHAR(255)    NOT NULL,   -- armazena hash werkzeug/bcrypt, NUNCA texto puro
    criado_em   TIMESTAMP       DEFAULT NOW()
);
