import os

import google.generativeai as genai
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector

from database.database import get_connection
from processing.embedder import generate_embeddings

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida.")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def retrieve_relevant_documents(query_text: str, k: int = 3):
    """
    Recupera os k documentos mais relevantes do banco de dados vetorial
    para uma dada consulta.

    Args:
        query_text (str): A pergunta do usuário.
        k (int): O número de documentos mais relevantes a serem recuperados.

    Returns:
        list: Uma lista de strings, onde cada string é um chunk de texto relevante.
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
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
    return documents


def generate_llm_response(question: str, context_documents: list):
    """
    Gera uma resposta à pergunta usando o LLM (Google Gemini neste exemplo),
    baseada nos documentos de contexto fornecidos.

    Args:
        question (str): A pergunta original do usuário.
        context_documents (list): Uma lista de strings, onde cada string é um chunk de contexto.

    Returns:
        str: A resposta gerada pelo LLM.
    """
    context_str = "\n\n".join(context_documents)

    prompt = f"""Use as seguintes informações de contexto para responder à pergunta.
    Se você não souber a resposta, diga que não sabe, não tente inventar uma resposta.

    Contexto:
    {context_str}

    Pergunta: {question}

    Resposta concisa em português:"""

    try:
        response = gemini_model.generate_content(
            contents=[prompt],
            generation_config={"temperature": 0.7, "max_output_tokens": 1000},
        )
        return response.text
    except Exception as e:
        print(f"Erro ao gerar resposta com LLM: {e}")
        return "Desculpe, não foi possível gerar uma resposta no momento. Por favor, tente novamente."


def run_rag_query(question: str):
    """
    Orquestra o processo RAG: recupera documentos e gera uma resposta.

    Args:
        question (str): A pergunta do usuário.

    Returns:
        str: A resposta final do sistema RAG.
    """
    print(f"\n--- Processando Consulta: '{question}' ---")

    relevant_docs = retrieve_relevant_documents(question, k=3)

    if not relevant_docs:
        print("Nenhum documento relevante encontrado no banco de dados.")
        return "Não consegui encontrar informações relevantes para sua pergunta no documento."

    print("\n--- Contexto Recuperado (Apenas Trechos Iniciais) ---")
    for i, doc_content in enumerate(relevant_docs):
        snippet = doc_content[:150] + ("..." if len(doc_content) > 150 else "")
        print(f"Documento {i + 1}: {snippet}\n")
    print("----------------------------------------------------\n")

    answer = generate_llm_response(question, relevant_docs)

    print("\n" + "=" * 20 + " RESPOSTA FINAL " + "=" * 20)
    print(answer)
    print("=" * 56 + "\n")

    return answer


if __name__ == "__main__":
    test_question_1 = "Quem é responsável pela emissão da NFSe?"
    run_rag_query(test_question_1)

    print("\n" + "=" * 70 + "\n")

    test_question_2 = "Como funciona a geração de nfse?"
    run_rag_query(test_question_2)

    print("\n" + "=" * 70 + "\n")

    test_question_3 = "Quem foi Napoleão Bonaparte?"
    run_rag_query(test_question_3)
