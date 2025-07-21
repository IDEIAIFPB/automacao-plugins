from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response import ParametersBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, get_xml


class TestParametersBuilder(TestCase):
    def setUp(self):
        self._builder = ParametersBuilder()
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = etree.Element("teste")
        self._targets_tags = {
            "numero_param": "Numero",
            "protocolo_param": "Protocolo",
            "aliquota_param": "Aliquota",
            "codigo_verificacao_param": "CodigoVerificacao",
        }
        output_file = build_output_file_path("cli.xml")
        self._final_envelope_tag = "GerarNfseEnvio"
        plugin_name = "teste"
        self._xsd_file = "resources/xsd-files/nfse-v2-04.xsd"
        self._response_tag = self._schema.elements.get("GerarNfseResposta")
        parser = Mapper(self._final_envelope_tag, plugin_name, self._xsd_file, output_file)
        self._mapper_tree = parser.build()
        self._mapper_root = self._mapper_tree.find(".//property")
        self.maxDiff = None

        self._parameters_str = """<teste>
  <parameters>
    <parameter id="NumeroNFe" origin="RESPONSE" xpath="/GerarNfseResposta/ListaNfse/CompNfse/Nfse/InfNfse/Numero"/>
    <parameter id="CodigoVerificacao" origin="RESPONSE" xpath="/GerarNfseResposta/ListaNfse/CompNfse/Nfse/InfNfse/CodigoVerificacao"/>
    <parameter id="AliquotaAtividade" origin="REQUEST" xpath="/GerarNfseEnvio/Rps/InfDeclaracaoPrestacaoServico/Servico/Valores/Aliquota"/>
    <parameter id="SistemaOrigem" origin="INPUT" xpath="/SynchroId/SistemaOrigem"/>
    <parameter id="CPFCNPJRemetente" origin="INPUT" xpath="/SynchroId/CpfCnpjPrestador"/>
    <parameter id="CodIBGEMun" origin="INPUT" xpath="/SynchroId/CodIBGEMun"/>
    <parameter id="InscricaoMunicipal" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/InscricaoPrestador"/>
    <parameter id="RazaoSocialPrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/RazaoSocialPrestador"/>
    <parameter id="NomeFantasiaPrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/NomeFantasiaPrestador"/>
    <parameter id="EnderecoPrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/EnderecoPrestador"/>
    <parameter id="CidadePrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/CidadePrestador"/>
    <parameter id="UFPrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/UFPrestador"/>
    <parameter id="EmailPrestador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/EmailPrestador"/>
    <parameter id="SerieRPS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/SerieRPS"/>
    <parameter id="NumeroRPS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ChaveRPS/NumeroRPS"/>
    <parameter id="NomeMunicipioTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/CidadeTomadorDescricao"/>
    <parameter id="BairroTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Bairro"/>
    <parameter id="CidadeTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Cidade"/>
    <parameter id="Uf" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/UF"/>
    <parameter id="CEPTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/CEP"/>
    <parameter id="EmailTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EmailTomador"/>
    <parameter id="TelefoneTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/TelefoneTomador"/>
    <parameter id="InscricaoMunicipalTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/InscricaoMunicipalTomador"/>
    <parameter id="TipoLogradouroTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/TipoLogradouro"/>
    <parameter id="LogradouroTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/Logradouro"/>
    <parameter id="NumeroEnderecoTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/NumeroEndereco"/>
    <parameter id="ComplementoEnderecoTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/EnderecoTomador/ComplementoEndereco"/>
    <parameter id="Tributacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/TributacaoRPS"/>
    <parameter id="CodigoAtividade" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/CodigoTributacaoMunicipio"/>
    <parameter id="TipoRecolhimento" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/TipoRecolhimento"/>
    <parameter id="RazaoSocialTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/RazaoSocialTomador"/>
    <parameter id="DiscriminacaoServico" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/Discriminacao"/>
    <parameter id="OptanteSimplesNacional" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/OptanteSimplesNacional"/>
    <parameter id="BaseCalculo" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/BaseCalculo"/>
    <parameter id="ValorLiquidoNfse" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorLiquidoNfse"/>
    <parameter id="ValorINSS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorINSS"/>
    <parameter id="ValorIss" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorIss"/>
    <parameter id="ValorPIS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorPIS"/>
    <parameter id="ValorCOFINS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorCOFINS"/>
    <parameter id="ValorIR" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorIR"/>
    <parameter id="ValorCSLL" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorCSLL"/>
    <parameter id="ValorTotalServicos" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorServicos"/>
    <parameter id="ValorTotalDeducoes" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorDeducoes"/>
    <parameter id="DescricaoMunicipioPrestacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/DescricaoMunicipioPrestacao"/>
    <parameter id="MunicipioPrestacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/MunicipioPrestacao"/>
    <parameter id="CodigoMunicipio" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/CodigoMunicipio"/>
    <parameter id="DataEmissao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/DataEmissao"/>
    <parameter id="HoraEmissao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/HoraEmissao"/>
    <parameter id="CNPJTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/CPFCNPJTomador/CNPJ"/>
    <parameter id="CPFTomador" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/CPFCNPJTomador/CPF"/>
    <parameter id="DocTomadorEstrangeiro" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/DocTomadorEstrangeiro"/>
    <parameter id="CodigoServico" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/CodigoServico"/>
    <parameter id="DescricaoCodServico" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/DescricaoCodServico"/>
    <parameter id="TipoRPS" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/TipoRPS"/>
    <parameter id="LocalPrestacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/DescricaoMunicipioPrestacao"/>
    <parameter id="ISSRetido" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ISSRetido"/>
    <parameter id="NaturezaOperacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/NaturezaOperacao"/>
    <parameter id="OutrasInformacoes" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/OutrasInformacoes"/>
    <parameter id="ValorIssRetido" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/ValorIssRetido"/>
    <parameter id="OutrasRetencoes" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/OutrasRetencoes"/>
    <parameter id="RegimeEspecialTributacao" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/RegimeEspecialTributacao"/>
    <parameter id="Competencia" origin="INPUT" xpath="/SynchroId/PedidoEnvioRPS/RPS/Competencia"/>
  </parameters>
</teste>
"""

    def test_build(self):
        tree = self._builder.build(self._root, "emissao", self._response_tag, self._mapper_root, self._targets_tags)
        s_tree = get_xml(tree)

        self.assertEqual(s_tree, self._parameters_str)


if __name__ == "__main__":
    main()
