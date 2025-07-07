# services/document_service.py
import os
from dotenv import load_dotenv
import google.generativeai as genai

from src.ingestion.file_reader import extract_text_from_file
from src.processing.chunker import chunk_text_by_tokens
from src.processing.embedder import generate_embeddings
from src.repository.document_repository import DocumentRepository

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("A variável de ambiente GOOGLE_API_KEY não está definida.")

genai.configure(api_key=GOOGLE_API_KEY)
gemini_model = genai.GenerativeModel("gemini-1.5-flash")


class DocumentService:
    def __init__(self):
        self.document_repository = DocumentRepository()

    def process_and_store_document(self, file_path: str) -> bool:
        """
        Processa um documento (PDF, XML, JSON), extrai texto, cria chunks,
        gera embeddings e os armazena.
        """
        try:
            # Chama a função unificada para extrair o texto
            text_content = extract_text_from_file(file_path)
            chunks = chunk_text_by_tokens(text_content)
            embeddings = generate_embeddings(chunks)
            self.document_repository.store_document_chunks_and_embeddings(
                chunks, embeddings
            )
            return True
        except (ValueError, FileNotFoundError) as e:
            # Erros específicos do file_reader
            print(f"Erro ao processar e armazenar o documento '{file_path}': {e}")
            return False
        except Exception as e:
            # Outros erros inesperados
            print(f"Erro inesperado no serviço de documento para '{file_path}': {e}")
            return False

    def get_rag_response(self, question: str) -> str:
        """
        Orquestra o processo RAG: recupera documentos e gera uma resposta do LLM.
        """
        try:
            relevant_docs = self.document_repository.retrieve_relevant_documents(
                question, k=3
            )

            if not relevant_docs:
                return "Não consegui encontrar informações relevantes para sua pergunta nos documentos."

            answer = self._generate_llm_response(question, relevant_docs)
            return answer
        except Exception as e:
            print(f"Erro ao gerar resposta RAG: {e}")
            return "Desculpe, ocorreu um erro ao processar sua solicitação."

    def _generate_llm_response(
        self, question: str, context_documents: list[str]
    ) -> str:
        """
        Gera uma resposta à pergunta usando o LLM (Google Gemini),
        baseada nos documentos de contexto fornecidos, com foco na geração de XPaths.
        """
        context_str = "\n\n".join(context_documents)
        prompt = f"""Você é um assistente avançado especializado em analisar informações de diversos tipos de documentos (como manuais em Markdown, configurações em XML, mapeamentos em JSON) para responder perguntas e, crucialmente, **gerar XPaths (para XML/HTML) ou JSONPaths (para JSON)**.
        Use as seguintes informações de contexto para responder à pergunta do usuário. Seu objetivo principal é identificar e fornecer o **XPath/JSONPath mais preciso e relevante** para o elemento ou funcionalidade que o usuário está perguntando. Se a pergunta implicar um XPath para XML ou JSONPath para JSON, forneça o caminho correspondente.
        **Diretrizes de Resposta:**
        1.  **Se a pergunta solicitar um XPath/JSONPath e o contexto fornecer um correspondente:** Forneça *apenas o XPath/JSONPath*, sem texto adicional. Exemplo: `//div[@id='minhaDiv']/span[@class='texto']` ou `$.users[0].name`.
        2.  **Se a pergunta solicitar um XPath/JSONPath, mas não houver um correspondente direto ou exato no contexto:** Tente *inferir* um XPath/JSONPath lógico baseado na descrição do elemento e nos padrões vistos no contexto. Se não for possível inferir um caminho com alta certeza, diga "Não foi possível gerar um XPath/JSONPath preciso com base nas informações fornecidas." e sugira o que poderia ser útil (ex: mais contexto HTML/XML/JSON).
        3.  **Se a pergunta for geral ou não solicitar um XPath/JSONPath:** Responda concisamente usando o contexto disponível.
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
