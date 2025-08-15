import fitz


def extract_text_from_pdf(path):
    doc = fitz.open(path)
    texto = "".join([pagina.get_text() for pagina in doc])
    doc.close()
    return texto
