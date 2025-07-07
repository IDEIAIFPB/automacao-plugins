from sentence_transformers import SentenceTransformer

model = SentenceTransformer("intfloat/multilingual-e5-base")


def generate_embeddings(chunks):
    """
    Gera embeddings para uma lista de chunks de texto usando o modelo SentenceTransformer.
    Args:
        chunks (list): Uma lista de strings, onde cada string é um chunk de texto.
    Returns:
        numpy.ndarray: Um array NumPy contendo os embeddings para cada chunk.
                       A forma do array será (número_de_chunks, dimensão_do_embedding).
    """
    return model.encode(chunks)
