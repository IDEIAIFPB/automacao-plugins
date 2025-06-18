import tiktoken


def chunk_text_by_tokens(text, max_tokens=500, model_name="gpt-3.5-turbo"):
    encoder = tiktoken.encoding_for_model(model_name)
    tokens = encoder.encode(text)

    chunks = []
    for i in range(0, len(tokens), max_tokens):
        chunk_tokens = tokens[i : i + max_tokens]
        chunk_text = encoder.decode(chunk_tokens)
        chunks.append(chunk_text)
    return chunks
