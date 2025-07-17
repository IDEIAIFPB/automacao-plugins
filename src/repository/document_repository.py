from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from src.processing.embedder import generate_embeddings
from src.database.database import (
    get_connection,
    create_table,
    insert_chunks_and_embeddings,
)

load_dotenv()


class DocumentRepository:
    """
    Repositório para operações de banco de dados relacionadas a documentos.
    """

    def __init__(self):
        create_table()

    def retrieve_relevant_documents(self, query_text: str, k: int = 3) -> list[str]:
        """
        Recupera os k documentos mais relevantes do banco de dados vetorial
        para uma dada consulta.
        """
        query_embedding = generate_embeddings([query_text])[0].tolist()
        conn = None
        cursor = None
        documents = []
        try:
            conn = get_connection()
            register_vector(conn)
            cursor = conn.cursor()
            cursor.execute(
                "SELECT texto FROM documentos ORDER BY embedding <-> %s LIMIT %s;",
                (str(query_embedding), k),
            )
            results = cursor.fetchall()
            documents = [row[0] for row in results]
        except Exception as e:
            print(f"Erro ao recuperar documentos: {e}")
            raise
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
        return documents

    def store_document_chunks_and_embeddings(
        self, chunks: list[str], embeddings: list
    ) -> None:
        """
        Insere chunks e seus embeddings no banco de dados.
        """
        try:
            insert_chunks_and_embeddings(chunks, embeddings)
        except Exception as e:
            print(f"Erro ao inserir dados no banco de dados: {e}")
            raise  # Re-lança a exceção
