from contextlib import contextmanager
import psycopg2
from projeto_av03_lab2.config import DB_CONFIG


def conectar_bd():
    """Conecta ao banco de dados PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


@contextmanager
def obter_cursor(auto_commit=True):
    """Abre conexao e cursor, fecha tudo automaticamente no final.

    Uso:
        with obter_cursor() as (conn, cursor):
            cursor.execute("SELECT ...")
    """
    conn = conectar_bd()
    if conn is None:
        raise ConnectionError("Nao foi possivel conectar ao banco de dados.")

    cursor = conn.cursor()
    try:
        yield conn, cursor
        if auto_commit:
            conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        cursor.close()
        conn.close()
