from ingestion.pdf_reader import extract_text_from_pdf
from processing.chunker import chunk_text_by_tokens
from processing.embedder import generate_embeddings
from database.database import create_table, insert_chunks_and_embeddings

pdf_path = "../NFS.pdf"

texto = extract_text_from_pdf(pdf_path)

chunks = chunk_text_by_tokens(texto)

embeddings = generate_embeddings(chunks)

create_table()
insert_chunks_and_embeddings(chunks, embeddings)

print("PDF processado e dados inseridos no banco com sucesso!")
