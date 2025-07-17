import os
from flask import Blueprint, request, jsonify
from src.service.document_service import DocumentService

document_bp = Blueprint("document", __name__)
document_service = DocumentService()


PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "resources")


@document_bp.route("/documents/update", methods=["POST"])
def process_document():
    data = request.get_json()
    file_path_relative = data.get("file_path")  # Renomeado para clareza

    if not file_path_relative:
        return jsonify({"error": "O caminho do documento é obrigatório."}), 400

    full_file_path = os.path.join(PROJECT_ROOT, file_path_relative)

    print(f"DEBUG: file_path recebido (relativo): {file_path_relative}")
    print(f"DEBUG: full_file_path construído: {full_file_path}")
    print(f"DEBUG: os.path.exists({full_file_path}): {os.path.exists(full_file_path)}")
    print(
        f"DEBUG: file_path_relative.startswith('resources/'): {file_path_relative.startswith('resources/')}"
    )

    if not file_path_relative.startswith("resources/") or not os.path.exists(
        full_file_path
    ):
        return jsonify(
            {"error": "Caminho do documento inválido ou não permitido."}
        ), 400

    success = document_service.process_and_store_document(full_file_path)

    if success:
        return jsonify(
            {
                "message": f"Documento '{file_path_relative}' processado e dados inseridos no banco com sucesso!"
            }
        ), 200
    else:
        return jsonify(
            {"error": f"Falha ao processar o documento '{file_path_relative}'."}
        ), 500


@document_bp.route("/query", methods=["POST"])
def query_rag():
    data = request.get_json()
    question = data.get("question")

    if not question:
        return jsonify({"error": "A pergunta é obrigatória."}), 400

    response = document_service.get_rag_response(question)
    return jsonify({"answer": response}), 200
