from unittest import TestCase, main

from lxml import etree

from src.core.action import ActionBuilder
from src.core.utils.xml_utils import build_output_file_path, get_xml
from src.mapper import Mapper


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
        with open("src/tests/resources/action.xml") as file:
            self._emissao_tree = file.read().replace("\n", "")

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
        self.assertEqual(s_tree.replace("\n", ""), self._emissao_tree)

    def test_parse_wsdl_schema(self):
        wsdl_tree = etree.parse(self._wsdl_path)
        wsdl_root = wsdl_tree.getroot()
        namespaces = wsdl_root.nsmap
        wsdl_schema_root = self._builder._parse_wsdl_schema(wsdl_root, namespaces)
        self.assertIsNotNone(wsdl_schema_root)


if __name__ == "__main__":
    main()
