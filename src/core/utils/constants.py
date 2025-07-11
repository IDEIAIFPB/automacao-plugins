TEMP_PATH = "./src/tests/temp"

CONDITTIONS_MAP = {
    "consulta": {
        "conflict": {},
        "accepted": {
            "conditions": [
                {"comparison": "EXISTS", "xpath_key": "numero_consulta"},
                {"comparison": "NOT_EXISTS", "xpath_key": "codigo_cancelamento_consulta"},
            ]
        },
        "cancelled": {"conditions": [{"comparison": "EXISTS", "xpath_key": "codigo_cancelamento_consulta"}]},
        "rejected": {"conditions": [{"comparison": "EXISTS", "xpath_key": "codigo_consulta"}]},
    },
    "cancelamento": {
        "accepted": {},
        "conflict": {},
        "cancelled": {"conditions": [{"comparison": "EXISTS", "xpath_key": "data_hora"}]},
        "rejected": {"conditions": [{"comparison": "EXISTS", "xpath_key": "codigo_cancelamento"}]},
    },
    "emissao": {
        "conflict": {
            "conditions": [
                {"comparison": "CONTAINS", "value": "L018", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "218", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "E10", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "E405", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "E163", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "E179", "xpath": "Codigo"},
                {"comparison": "CONTAINS", "value": "PERMITE A CONSULTA", "xpath": "/"},
                {"comparison": "CONTAINS", "value": "RPS.*J.*EXISTE", "xpath": "/"},
                {
                    "comparison": "CONTAINS",
                    "value": "mero de recibo informado j.*outra NF-E.*11.549/2017",
                    "xpath": "/",
                },
                {"comparison": "CONTAINS", "value": "RPS.*j.*convertido na NFS-e", "xpath": "/"},
                {"comparison": "CONTAINS", "value": "RPS.*j.*informado", "xpath": "/"},
            ]
        },
        "accepted": {"conditions": [{"comparison": "EXISTS", "xpath_key": "numero_emissao"}]},
        "rejected": {"conditions": [{"comparison": "EXISTS", "xpath_key": "codigo_emissao"}]},
        "cancelled": {},
    },
}


def build_output_file_path(file_name: str) -> str:
    return f"{TEMP_PATH}/{file_name}"
