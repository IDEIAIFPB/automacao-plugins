import os
from dotenv import load_dotenv
from pgvector.psycopg2 import register_vector
from processing.embedder import generate_embeddings
from database.database import get_connection

import google.generativeai as genai

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida.")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


def retrieve_relevant_documents(query_text: str, k: int = 3) -> list[str]:
    """
    Recupera os k documentos mais relevantes do banco de dados vetorial
    para uma dada consulta.

    Esta função permanece largely a mesma, pois ela busca chunks de texto
    (agora podendo ser Markdown de PDFs, ou texto formatado de JSON/XML).

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


def generate_llm_response(question: str, context_documents: list[str]) -> str:
    """
    Gera uma resposta à pergunta usando o LLM (Google Gemini),
    baseada nos documentos de contexto fornecidos, com foco na geração de XPaths.

    A grande mudança está no prompt, que agora instrui o modelo a
    identificar e gerar XPaths quando apropriado.

    Args:
        question (str): A pergunta original do usuário.
        context_documents (list): Uma lista de strings, onde cada string é um chunk de contexto.
                                  Estes chunks podem vir de PDFs (Markdown), JSON formatado, ou XML.

    Returns:
        str: A resposta gerada pelo LLM, que pode ser um XPath, uma explicação, etc.
    """
    context_str = "\n\n".join(context_documents)

    prompt = f"""Você é um assistente avançado especializado em analisar informações de diversos tipos de documentos (como manuais em Markdown, configurações em XML, mapeamentos em JSON) para responder perguntas e, crucialmente, **gerar XPaths**.

    Use as seguintes informações de contexto para responder à pergunta do usuário. Seu objetivo principal é identificar e fornecer o **XPath mais preciso e relevante** para o elemento ou funcionalidade que o usuário está perguntando.

    **Diretrizes de Resposta:**
    1.  **Se a pergunta solicitar um XPath e o contexto fornecer um correspondente:** Forneça *apenas o XPath*, sem texto adicional. Exemplo: `//div[@id='minhaDiv']/span[@class='texto']`.
    2.  **Se a pergunta solicitar um XPath, mas não houver um correspondente direto ou exato no contexto:** Tente *inferir* um XPath lógico baseado na descrição do elemento e nos padrões vistos no contexto. Se não for possível inferir um XPath com alta certeza, diga "Não foi possível gerar um XPath preciso com base nas informações fornecidas." e sugira o que poderia ser útil (ex: mais contexto HTML/XML).
    3.  **Se a pergunta for geral ou não solicitar um XPath:** Responda concisamente usando o contexto disponível.
    4.  **Se o contexto não contiver informações relevantes:** Diga "Não tenho informações suficientes para responder a essa pergunta com o contexto fornecido."

    **Contexto Disponível:**
    ```
    {context_str}
    ```

    **Pergunta do Usuário:** {question}

    **Sua Resposta:**"""

    try:
        response = gemini_model.generate_content(
            contents=[prompt],
            generation_config={
                "temperature": 0.3,
                "max_output_tokens": 200,
            },
        )
        return response.text.strip()
    except Exception as e:
        print(f"Erro ao gerar resposta com LLM: {e}")
        return "Desculpe, não foi possível gerar uma resposta no momento. Por favor, tente novamente."


def run_rag_query(question: str) -> str:
    """
    Orquestra o processo RAG: recupera documentos e gera uma resposta.

    Esta função é o ponto de entrada para suas consultas.

    Args:
        question (str): A pergunta do usuário.

    Returns:
        str: A resposta final do sistema RAG.
    """
    print(f"\n--- Processando Consulta: '{question}' ---")

    relevant_docs = retrieve_relevant_documents(question, k=3)

    if not relevant_docs:
        print("Nenhum documento relevante encontrado no banco de dados.")
        return "Não consegui encontrar informações relevantes para sua pergunta nos documentos."

    print("\n--- Contexto Recuperado (Apenas Trechos Iniciais) ---")
    for i, doc_content in enumerate(relevant_docs):
        snippet = doc_content[:200].replace("\n", " ") + (
            "..." if len(doc_content) > 200 else ""
        )
        print(f"Documento {i + 1}: {snippet}\n")
    print("----------------------------------------------------\n")

    answer = generate_llm_response(question, relevant_docs)

    print("\n" + "=" * 20 + " RESPOSTA FINAL " + "=" * 20)
    print(answer)
    print("=" * 56 + "\n")

    return answer


if __name__ == "__main__":
    print("--- Testando com Perguntas de XPath ---")
    test_question_1 = "Qual é o XPath para o campo 'CPFCNPJContrib' no contexto de 'NFeLoteBaixarArquivo'?"
    run_rag_query(test_question_1)
