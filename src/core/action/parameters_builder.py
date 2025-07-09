import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder

TIPO_EMISSAO = "EMISSAO"
TIPO_CANCELAMENTO = "CANCELAMENTO"
TIPO_CONSULTA = "CONSULTA"

DEFAULT_PARAMS = {
    "NumeroNFe": "",
    "CodigoVerificacao": "",
}
PARAMETERS_EMISSAO = {
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


class ParametersBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "parameters"
        self._inner_tag = "parameter"

    def build(self, tree: _Element, file_type: str, response_tag: _Element, targets_element: list):
        parameters_tree = etree.SubElement(tree, self._tag)
        return self._build(parameters_tree, file_type, response_tag, targets_element)

    def _build(self, tree: _Element, file_type: str, response_tag: _Element, targets_element: list):
        file_type = file_type.upper()

        if file_type == TIPO_CANCELAMENTO:
            return tree

        i = 0
        for key, value in DEFAULT_PARAMS.items():
            etree.SubElement(
                tree,
                self._inner_tag,
                attrib={
                    "id": key,
                    "origin": "RESPONSE",
                    "xpath": value
                    if value != ""
                    else self._format_result(self.create_xpath(response_tag, targets_element[i])),
                },
            )
            i += 1

        if file_type == TIPO_EMISSAO:
            for key, value in PARAMETERS_EMISSAO.items():
                etree.SubElement(
                    tree,
                    self._inner_tag,
                    attrib={
                        "id": key,
                        "origin": "REQUEST" if key == "AliquotaAtividade" else "INPUT",
                        "xpath": value,
                    },
                )

        return tree

    def extract_local_name(self, name):
        if "}" in name:
            return name.split("}")[-1]
        return name

    def create_xpath(self, element, target_element, current_path=None):
        local_name = self.extract_local_name(element.name)

        if current_path is None:
            current_path = [local_name]
        else:
            current_path = current_path + [local_name]

        if local_name == target_element:
            return current_path

        if element.type.is_complex():
            for child in element.type.content.iter_elements():
                result = self.create_xpath(child, target_element, current_path)

                if result:
                    return result

        return None

    def _format_result(self, result):
        result = "/" + "/".join(result) if result else ""
        return result
