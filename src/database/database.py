# database/database.py
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def get_connection():
    return psycopg2.connect(
        dbname=os.getenv("PGDATABASE"),
        user=os.getenv("PGUSER"),
        password=os.getenv("PGPASSWORD"),
        host=os.getenv("PGHOST"),
        port=os.getenv("DBPORT"),
        sslmode="require",
    )


def create_table():
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute("DROP TABLE IF EXISTS documentos;")
        conn.commit()

        cur.execute("""
            CREATE TABLE documentos ( -- Removido IF NOT EXISTS para sempre recriar
                id SERIAL PRIMARY KEY,
                texto TEXT,
                embedding VECTOR(768)
            );
        """)
        conn.commit()
        print("Tabela 'documentos' verificada/recriada com sucesso!")
    except Exception as e:
        conn.rollback()
        print(f"Erro ao criar/verificar tabela 'documentos': {e}")
        raise
    finally:
        cur.close()
        conn.close()


def insert_chunks_and_embeddings(chunks, embeddings):
    conn = get_connection()
    cur = conn.cursor()
    try:
        for chunk, emb in zip(chunks, embeddings):
            emb_str = ",".join(map(str, emb))
            cur.execute(
                "INSERT INTO documentos (texto, embedding) VALUES (%s, %s)",
                (chunk, f"[{emb_str}]"),
            )
        conn.commit()
    except Exception as e:
        conn.rollback()
        print(f"Erro ao inserir chunks e embeddings: {e}")
        raise
    finally:
        cur.close()
        conn.close()
