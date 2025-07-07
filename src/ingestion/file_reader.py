import json
import lxml.etree
import fitz


def extract_text_from_file(file_path: str) -> str:
    """
    Extrai o texto de um arquivo baseado em sua extensão (PDF, XML, JSON).

    Args:
        file_path (str): O caminho completo para o arquivo.

    Returns:
        str: O conteúdo textual extraído do arquivo.

    Raises:
        ValueError: Se o tipo de arquivo não for suportado ou se houver um erro de leitura.
        FileNotFoundError: Se o arquivo não for encontrado.
    """
    if not isinstance(file_path, str) or not file_path:
        raise ValueError("O caminho do arquivo deve ser uma string não vazia.")

    file_extension = file_path.lower().split(".")[-1]

    try:
        if file_extension == "pdf":
            doc = fitz.open(file_path)
            text_content = "".join([pagina.get_text() for pagina in doc])
            doc.close()
            return text_content
        elif file_extension == "xml":
            tree = lxml.etree.parse(file_path)
            root = tree.getroot()
            return lxml.etree.tostring(root, pretty_print=True, encoding="unicode")
        elif file_extension == "json":
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            return json.dumps(data, indent=2, ensure_ascii=False)
        else:
            raise ValueError(f"Tipo de arquivo não suportado: .{file_extension}")
    except FileNotFoundError:
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")
    except Exception as e:
        raise ValueError(f"Erro ao extrair texto do arquivo '{file_path}': {e}")
