# Gateway de Pagamento — Projeto BD + AV03 Lab Prog 2

> Projeto acadêmico para as disciplinas de **Projeto de Banco de Dados (PBD)** e **Laboratório de Programação 2** — CESMAC.

![Status](https://img.shields.io/badge/status-em%20desenvolvimento-yellow)
![Disciplina](https://img.shields.io/badge/disciplina-PBD%20%7C%20Lab%20Prog%202-blue)
![Instituição](https://img.shields.io/badge/instituição-CESMAC-green)

---

## Equipe

| Papel       | Nome                  |
|-------------|-----------------------|
| Professora  | Tacyana Batista       |
| Professor   | Wagner                |
| Aluno       | Henrique Ferrario     |
| Aluno       | João Danilo           |

---

## Estrutura do Repositório

```
gateway-pagamento-pbd/
│
├── docs/                                # documentacao do projeto
│   └── minimundo.md                     # descricao textual do sistema
│
├── diagramas/                           # modelos entidade-relacionamento
│   ├── MER_chen.png                     # modelo conceitual (notacao de Chen)
│   └── DER_dbdiagram.png               # modelo logico (dbdiagram.io)
│
├── sql/                                 # scripts do banco de dados
│   ├── ddl_create_tables_desenv.sql     # criacao das tabelas (ambiente dev)
│   ├── ddl_create_tables_prod.sql       # criacao das tabelas (ambiente prod)
│   ├── add_usuarios.sql                 # tabela de usuarios (AV03)
│   ├── consultas.sql                    # consultas SQL de estudo
│   └── joins/                           # exercicios de JOIN
│       ├── desafio1_left_join.sql
│       ├── desafio2_right_join.sql
│       └── desafio3_full_outer_join.sql
│
├── projeto_av03_lab2/                   # sistema Python (AV03 - Lab Prog 2)
│   ├── main.py                          # ponto de entrada do sistema
│   ├── config.py                        # configuracoes do banco
│   ├── database.py                      # conexao e context manager
│   ├── repositories/                    # acesso a dados
│   │   ├── usuario_repository.py        # CRUD tabela usuarios
│   │   └── cliente_repository.py        # CRUD tabela clientes
│   ├── services/                        # regras de negocio
│   │   ├── auth_service.py              # cadastro + login (hash)
│   │   └── cliente_service.py           # operacoes de clientes
│   ├── ui/                              # interface de terminal
│   │   └── menus.py                     # menus externo e interno
│   └── consultas/                       # consultas JOIN via Python
│       ├── inner_join.py                # INNER JOIN
│       ├── left_join.py                 # LEFT JOIN
│       └── full_outer_join.py           # FULL OUTER JOIN
│
├── scripts/                             # scripts auxiliares
│   ├── popular_banco.py                 # seed de dados ficticios
│   └── popular_banco_extra.py           # seed adicional
│
├── .gitignore
└── README.md
```

---

## Como Executar

### Pre-requisitos
- Python 3.8+
- PostgreSQL rodando localmente
- Dependencias: `psycopg2`, `werkzeug`

### Instalacao

```bash
# Criar e ativar o ambiente virtual
python -m venv .venv
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install psycopg2-binary werkzeug
```

### Criar as tabelas no banco

Execute o script SQL de criacao das tabelas no PostgreSQL:
```sql
-- Usar o arquivo sql/ddl_create_tables_prod.sql
-- E depois o sql/add_usuarios.sql para a tabela de usuarios
```

### Popular o banco com dados ficticios

```bash
python scripts/popular_banco.py
python scripts/popular_banco_extra.py
```

### Executar o sistema (AV03)

```bash
python -m projeto_av03_lab2.main
```

---

## Descricao dos Arquivos

| Arquivo | Descricao |
|---------|-----------|
| `docs/minimundo.md` | Contextualizacao do sistema em linguagem natural |
| `diagramas/MER_chen.png` | Modelo conceitual na notacao de Chen |
| `diagramas/DER_dbdiagram.png` | Modelo logico exportado do dbdiagram.io |
| `sql/ddl_create_tables_*.sql` | Scripts DDL para criacao das tabelas |
| `sql/consultas.sql` | Consultas SQL para estudo |
| `sql/joins/` | Exercicios de LEFT, RIGHT e FULL OUTER JOIN |
| `projeto_av03_lab2/` | Sistema CRUD com autenticacao e consultas JOIN |
| `scripts/` | Scripts para popular o banco com dados de teste |

---

## Tecnologias

![SQL](https://img.shields.io/badge/SQL-DDL-orange)
![Python](https://img.shields.io/badge/Python-3.x-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-336791)
![psycopg2](https://img.shields.io/badge/lib-psycopg2-orange)
![werkzeug](https://img.shields.io/badge/lib-werkzeug-green)
![dbdiagram.io](https://img.shields.io/badge/diagrama-dbdiagram.io-blueviolet)
