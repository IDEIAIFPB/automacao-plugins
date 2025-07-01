from lxml import etree as ET
from automation_request import get_element_by_message_name, parse_xsd, parse_wsdl

PARAMETERS_CONSULTA = {"NumeroNFe": "", "CodigoVerificacao": ""}
PARAMETERS_EMISSAO = {
    "NumeroNFe": "",
    "CodigoVerificacao": "",
    "AliquotaAtividade": "",
    "SistemaOrigem": "/SynchroId/SistemaOrigem",
    "CPFCNPJRemetente": "/SynchroId/CpfCnpjPrestador",
    "CodIBGEMun": "/SynchroId/CodIBGEMun",
    "InscricaoMunicipal": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/InscricaoPrestador",
    "RazaoSocialPrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/RazaoSocialPrestador",
    "NomeFantasiaPrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/NomeFantasiaPrestador",
    "EnderecoPrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/EnderecoPrestador",
    "CidadePrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/CidadePrestador",
    "UFPrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/UFPrestador",
    "EmailPrestador": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/EmailPrestador",
    "SerieRPS": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/SerieRPS",
    "NumeroRPS": "/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/NumeroRPS",
    "NomeMunicipioTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/CidadeTomadorDescricao",
    "BairroTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Bairro",
    "CidadeTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Cidade",
    "Uf": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/UF",
    "CEPTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/CEP",
    "EmailTomador": "/SynchroId/PedidoEnvioRPS/RPS/EmailTomador",
    "TelefoneTomador": "/SynchroId/PedidoEnvioRPS/RPS/TelefoneTomador",
    "InscricaoMunicipalTomador": "/SynchroId/PedidoEnvioRPS/RPS/InscricaoMunicipalTomador",
    "TipoLogradouroTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/TipoLogradouro",
    "LogradouroTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Logradouro",
    "NumeroEnderecoTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/NumeroEndereco",
    "ComplementoEnderecoTomador": "/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/ComplementoEndereco",
    "Tributacao": "/SynchroId/PedidoEnvioRPS/RPS/TributacaoRPS",
    "CodigoAtividade": "/SynchroId/PedidoEnvioRPS/RPS/CodigoTributacaoMunicipio",
    "TipoRecolhimento": "/SynchroId/PedidoEnvioRPS/RPS/TipoRecolhimento",
    "RazaoSocialTomador": "/SynchroId/PedidoEnvioRPS/RPS/RazaoSocialTomador",
    "DiscriminacaoServico": "/SynchroId/PedidoEnvioRPS/RPS/Discriminacao",
    "OptanteSimplesNacional": "/SynchroId/PedidoEnvioRPS/RPS/OptanteSimplesNacional",
    "BaseCalculo": "/SynchroId/PedidoEnvioRPS/RPS/BaseCalculo",
    "ValorLiquidoNfse": "/SynchroId/PedidoEnvioRPS/RPS/ValorLiquidoNfse",
    "ValorINSS": "/SynchroId/PedidoEnvioRPS/RPS/ValorINSS",
    "ValorIss": "/SynchroId/PedidoEnvioRPS/RPS/ValorIss",
    "ValorPIS": "/SynchroId/PedidoEnvioRPS/RPS/ValorPIS",
    "ValorCOFINS": "/SynchroId/PedidoEnvioRPS/RPS/ValorCOFINS",
    "ValorIR": "/SynchroId/PedidoEnvioRPS/RPS/ValorIR",
    "ValorCSLL": "/SynchroId/PedidoEnvioRPS/RPS/ValorCSLL",
    "ValorTotalServicos": "/SynchroId/PedidoEnvioRPS/RPS/ValorServicos",
    "ValorTotalDeducoes": "/SynchroId/PedidoEnvioRPS/RPS/ValorDeducoes",
    "DescricaoMunicipioPrestacao": "/SynchroId/PedidoEnvioRPS/RPS/DescricaoMunicipioPrestacao",
    "MunicipioPrestacao": "/SynchroId/PedidoEnvioRPS/RPS/MunicipioPrestacao",
    "CodigoMunicipio": "/SynchroId/PedidoEnvioRPS/RPS/CodigoMunicipio",
    "DataEmissao": "/SynchroId/PedidoEnvioRPS/RPS/DataEmissao",
    "HoraEmissao": "/SynchroId/PedidoEnvioRPS/RPS/HoraEmissao",
    "CNPJTomador": "/SynchroId/PedidoEnvioRPS/RPS/CPFCNPJTomador/CNPJ",
    "CPFTomador": "/SynchroId/PedidoEnvioRPS/RPS/CPFCNPJTomador/CPF",
    "DocTomadorEstrangeiro": "/SynchroId/PedidoEnvioRPS/RPS/DocTomadorEstrangeiro",
    "CodigoServico": "/SynchroId/PedidoEnvioRPS/RPS/CodigoServico",
    "DescricaoCodServico": "/SynchroId/PedidoEnvioRPS/RPS/DescricaoCodServico",
    "TipoRPS": "/SynchroId/PedidoEnvioRPS/RPS/TipoRPS",
    "LocalPrestacao": "/SynchroId/PedidoEnvioRPS/RPS/DescricaoMunicipioPrestacao",
    "ISSRetido": "/SynchroId/PedidoEnvioRPS/RPS/ISSRetido",
    "NaturezaOperacao": "/SynchroId/PedidoEnvioRPS/RPS/NaturezaOperacao",
    "OutrasInformacoes": "/SynchroId/PedidoEnvioRPS/RPS/OutrasInformacoes",
    "ValorIssRetido": "/SynchroId/PedidoEnvioRPS/RPS/ValorIssRetido",
    "OutrasRetencoes": "/SynchroId/PedidoEnvioRPS/RPS/OutrasRetencoes",
    "RegimeEspecialTributacao": "/SynchroId/PedidoEnvioRPS/RPS/RegimeEspecialTributacao",
    "Competencia": "/SynchroId/PedidoEnvioRPS/RPS/Competencia",
}


def montar_xpath_saida(elemento, xsd):
    xpath_saida = f"Envelope/Body/{elemento.get('name')}"
    if elemento.get("type") is not None:
        tipo = elemento.get("type").split(":")[-1]
        tipo_complexo = xsd.find(
            f"./xsd:complexType[@name='{tipo}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        if tipo_complexo is not None:
            xpath_saida = percorre_tipo_complexo_saida(tipo_complexo, xpath_saida, xsd)
    return xpath_saida


def percorre_tipo_complexo_saida(tipo_complexo, xpath_saida, xsd):
    elemento = tipo_complexo.find(
        ".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
    )
    xpath_saida += f"/{elemento.get('name')}"
    if elemento.get("type") is not None:
        tipo = elemento.get("type").split(":")[-1]
        tipo_complexo = xsd.find(
            f"./xsd:complexType[@name='{tipo}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        if tipo_complexo is not None:
            xpath_saida = percorre_tipo_complexo_saida(tipo_complexo, xpath_saida, xsd)
    return xpath_saida


def mapeia_wsdl_response(wsdl, bindig_operation_name):
    tree, root, namespaces = parse_wsdl(wsdl)

    xsd = parse_xsd(tree, namespaces)

    operation = root.find(
        f"./wsdl:portType/wsdl:operation[@name='{bindig_operation_name}']",
        namespaces=namespaces,
    )
    output = operation.find("wsdl:output", namespaces=namespaces)
    output_message = output.get("message").split(":")[-1]
    output_element_name = get_element_by_message_name(output_message, root, namespaces)
    elemento = xsd.find(
        f"./xsd:element[@name='{output_element_name}']",
        namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
    )
    xpath_saida = montar_xpath_saida(elemento, xsd)

    return xpath_saida


def monta_status(arquivo, status, path_init, path_end, xsd):
    if arquivo == "consulta":
        status = monta_status_consulta(status, path_init, path_end, xsd)
    if arquivo == "emissao":
        status = monta_status_emissao(status, path_init, path_end, xsd)
    if arquivo == "cancelamento":
        status = monta_status_cancelamento(status, path_init, path_end, xsd)
    return status


def monta_xpath_by_init_end(xsd, path_init, path_end):
    pass
    # tree = ET.parse(xsd)
    # xpath = path_init
    # elemento = tree.find(
    #     f".//xsd:complexType[@name='{path_init}']",
    #     namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
    # )


def monta_status_consulta(status, path_init, path_end, xsd):
    accepted = ET.SubElement(status, "accepted")
    cancelled = ET.SubElement(status, "cancelled")
    rejected = ET.SubElement(status, "rejected")

    accepted_conditions = ET.SubElement(accepted, "conditions")
    cancelled_conditions = ET.SubElement(cancelled, "conditions")
    rejected_conditions = ET.SubElement(rejected, "conditions")

    ET.SubElement(accepted_conditions, "condition", comparison="EXISTS", xpath="")
    ET.SubElement(accepted_conditions, "condition", comparison="NOT_EXISTS", xpath="")
    ET.SubElement(cancelled_conditions, "condition", comparison="EXISTS", xpath="")
    ET.SubElement(rejected_conditions, "condition", comparison="EXISTS", xpath="")

    return status


def monta_status_emissao(status, path_init, path_end, xsd):
    processing = ET.SubElement(status, "processing")
    conflict = ET.SubElement(status, "conflict")
    rejected = ET.SubElement(status, "rejected")

    processing_conditions = ET.SubElement(processing, "conditions")
    conflict_conditions = ET.SubElement(conflict, "conditions")
    rejected_conditions = ET.SubElement(rejected, "conditions")

    ET.SubElement(processing_conditions, "condition", comparison="EXISTS", xpath="")

    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="L018", xpath=""
    )
    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="218", xpath=""
    )
    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="E10", xpath=""
    )
    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="E405", xpath=""
    )
    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="E163", xpath=""
    )
    ET.SubElement(
        conflict_conditions, "condition", comparison="CONTAINS", value="E179", xpath=""
    )
    ET.SubElement(
        conflict_conditions,
        "condition",
        comparison="CONTAINS",
        parser="TEXT",
        xpath="PERMITE A CONSULTA",
    )
    ET.SubElement(
        conflict_conditions,
        "condition",
        comparison="CONTAINS",
        parser="TEXT",
        xpath="RPS.*J.*EXISTE",
    )
    ET.SubElement(
        conflict_conditions,
        "condition",
        comparison="CONTAINS",
        parser="TEXT",
        xpath="mero de recibo informado j.*outra NF-E.*11.549/201",
    )
    ET.SubElement(
        conflict_conditions,
        "condition",
        comparison="CONTAINS",
        parser="TEXT",
        xpath="RPS.*j.*convertido na NFS-e",
    )
    ET.SubElement(
        conflict_conditions,
        "condition",
        comparison="CONTAINS",
        parser="TEXT",
        xpath="RPS.*j.*informado",
    )

    ET.SubElement(rejected_conditions, "condition", comparison="EXISTS", xpath="")

    return status


def monta_status_cancelamento(status, path_init, path_end, xsd):
    cancelled = ET.SubElement(status, "cancelled")
    rejected = ET.SubElement(status, "rejected")

    cancelled_conditions = ET.SubElement(cancelled, "conditions")
    rejected_conditions = ET.SubElement(rejected, "conditions")

    ET.SubElement(cancelled_conditions, "condition", comparison="EXISTS", xpath="")
    ET.SubElement(rejected_conditions, "condition", comparison="EXISTS", xpath="")

    return status


def monta_parameters(arquivo, response_body, path_init, path_end, xsd):
    if arquivo == "consulta":
        parametros = PARAMETERS_CONSULTA
    if arquivo == "emissao":
        parametros = PARAMETERS_EMISSAO
    if arquivo == "cancelamento":
        return
    parameters = ET.SubElement(response_body, "parameters")
    for param in parametros.keys():
        ET.SubElement(
            parameters,
            "parameter",
            id=param,
            origin="RESPONSE",
            xpath=parametros[param],
        )
    return parameters
