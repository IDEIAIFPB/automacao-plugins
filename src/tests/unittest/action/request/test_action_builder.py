from unittest import TestCase, main

from lxml import etree

from src.core.action import ActionBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, get_xml


class TestActionBuilder(TestCase):
    def setUp(self):
        self._builder = ActionBuilder()
        self._plugin_id = "emissao-teste"
        self._operation_tag = "GerarNfse"
        self._wsdl_path = "resources/wsdl-files/nfse04.wsdl"
        self._final_envelope_tag = "GerarNfseEnvio"
        self._response_tag = "GerarNfseResposta"
        self._targets_tags = {
            "numero_param": "Numero",
            "protocolo_param": "Protocolo",
            "aliquota_param": "Aliquota",
            "codigo_verificacao_param": "CodigoVerificacao",
            "codigo_details": "Codigo",
            "mensagem_details": "Mensagem",
            "correcao_details": "Correcao",
            "numero_consulta": "Numero",
            "codigo_cancelamento_consulta": "Codigo",
            "codigo_consulta": "Codigo",
            "data_hora": "DataHora",
            "codigo_cancelamento": "Codigo",
            "codigo_emissao": "Codigo",
            "numero_emissao": "Numero",
        }
        self._xsd_file = "resources/xsd-files/nfse-v2-04.xsd"
        output_file = build_output_file_path("cli.xml")
        plugin_name = "teste"
        parser = Mapper(self._final_envelope_tag, plugin_name, self._xsd_file, output_file)
        self._signatures = parser._mapper_builder.metadata.signature
        self._mapper_tree = parser.build()
        self.maxDiff = None
        self._emissao_tree = """<document-action xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" id="emissao-teste" xsi:noNamespaceSchemaLocation="../../../schemas/document-action.xsd">
  <request>
    <endpoint>
      <urlParameterName>url-endpoint-emissao</urlParameterName>
      <method>POST</method>
      <tls>TLSv1.2</tls>
    </endpoint>
    <headers>
      <commonHeader name="Content-Type" value="text/xml;charset=UTF-8"/>
      <commonHeader name="SOAPAction" value="https://tributosmunicipais.com.br/nfse/api/GerarNfse"/>
    </headers>
    <body>
      <input>
        <document-mapper>emissao-mapper.xml</document-mapper>
        <signatures>
          <signature target="InfDeclaracaoPrestacaoServico" type="ELEMENT" parent="Rps" attribute="id"/>
        </signatures>
      </input>
      <content>
        <template inputResultVariable="REQUEST_CONTENT"><![CDATA[<?xml version='1.0' encoding='utf-8'?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="https://tributosmunicipais.com.br/nfse/api/" xmlns:xd="http://www.w3.org/2000/09/xmldsig#">
  <soapenv:Header/>
  <soapenv:Body>
    <tns:GerarNfseRequest>
      <nfseCabecMsg>
        <cabecalho>
          <versaoDados>?</versaoDados>
        </cabecalho>
      </nfseCabecMsg>
      <nfseDadosMsg>REQUEST_CONTENT</nfseDadosMsg>
    </tns:GerarNfseRequest>
  </soapenv:Body>
</soapenv:Envelope>
]]></template>
      </content>
    </body>
  </request>
  <response>
    <body>
      <input>
        <content xpath="Envelope/Body/GerarNfseResponse/outputXML"/>
      </input>
      <return>
        <status>
          <accepted>
            <conditions>
              <condition comparison="EXISTS" xpath="/GerarNfseResposta/ListaNfse/CompNfse/Nfse/InfNfse/Numero"/>
            </conditions>
          </accepted>
          <conflict>
            <conditions type="OR">
              <condition comparison="CONTAINS" value="L018" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="218" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="E10" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="E405" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="E163" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="E179" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
              <condition comparison="CONTAINS" value="PERMITE A CONSULTA" xpath="/"/>
              <condition comparison="CONTAINS" value="RPS.*J.*EXISTE" xpath="/"/>
              <condition comparison="CONTAINS" value="mero de recibo informado j.*outra NF-E.*11.549/2017" xpath="/"/>
              <condition comparison="CONTAINS" value="RPS.*j.*convertido na NFS-e" xpath="/"/>
              <condition comparison="CONTAINS" value="RPS.*j.*informado" xpath="/"/>
            </conditions>
          </conflict>
          <rejected>
            <conditions>
              <condition comparison="EXISTS" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
            </conditions>
          </rejected>
          <default status="UNKNOWN"/>
        </status>
        <details optional="false">
          <message id="codigo" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
          <message id="mensagem" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Mensagem"/>
          <message id="correcao" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Correcao"/>
        </details>
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
      </return>
    </body>
  </response>
</document-action>
"""

    def test_build(self):
        tree = self._builder.build(
            self._plugin_id,
            self._signatures,
            self._operation_tag,
            self._wsdl_path,
            self._final_envelope_tag,
            self._xsd_file,
            self._response_tag,
            self._mapper_tree,
            self._targets_tags,
        )
        s_tree = get_xml(tree)

        self.assertEqual(s_tree, self._emissao_tree)

    def test_parse_wsdl_schema(self):
        wsdl_tree = etree.parse(self._wsdl_path)
        wsdl_root = wsdl_tree.getroot()
        namespaces = wsdl_root.nsmap
        wsdl_schema_root = self._builder._parse_wsdl_schema(wsdl_root, namespaces)
        self.assertIsNotNone(wsdl_schema_root)


if __name__ == "__main__":
    main()
