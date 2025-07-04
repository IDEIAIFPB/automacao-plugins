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
    cur.execute("""
        CREATE TABLE IF NOT EXISTS documentos (
            id SERIAL PRIMARY KEY,
            texto TEXT,
            embedding VECTOR(384)
        );
    """)
    conn.commit()
    cur.close()
    conn.close()


def insert_chunks_and_embeddings(chunks, embeddings):
    conn = get_connection()
    cur = conn.cursor()
    for chunk, emb in zip(chunks, embeddings):
        emb_str = ",".join(map(str, emb))
        cur.execute(
            "INSERT INTO documentos (texto, embedding) VALUES (%s, %s)",
            (chunk, f"[{emb_str}]"),
        )
    conn.commit()
    cur.close()
    conn.close()
