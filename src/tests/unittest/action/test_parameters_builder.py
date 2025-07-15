from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action import ParametersBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, create_xpath, export_xml_to_file, format_result, get_xml


class TestParametersBuilder(TestCase):
    def setUp(self):
        self._builder = ParametersBuilder()
        self._output_file = build_output_file_path("parameters_builder_test_consulta.xml")
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-02.xsd")

    def test_build(self):
        root = etree.Element("root")
        response_tag = self._schema.elements.get("ConsultarLoteRpsResposta")
        targets_element = ["Numero", "CodigoVerificacao", "Aliquota"]
        tree = self._builder.build(root, "Consulta", response_tag, targets_element)
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)

    def test_build_emissao(self):
        xsd_file = "resources/xsd-files/NFSE.xsd.XSD"
        output_file = build_output_file_path("cli.xml")
        root_element = "EnviarLoteRpsEnvio"
        plugin_name = "teste"
        parser = Mapper(root_element, plugin_name, xsd_file, output_file)

        tree = parser.build()

        mapper_root = tree.find(".//property")
        self._output_file = build_output_file_path("parameters_builder_test_emissao.xml")
        root = etree.Element("root")
        response_tag = self._schema.elements.get("EnviarLoteRpsResposta")
        targets_element = {
            "numero_param": "NumeroLote",
            "protocolo_param": "Protocolo",
            "aliquota_param": "Aliquota",
            "codigo_verificacao_param": "CodigoVerificacao",
        }
        tree = self._builder.build(root, "Emissao", response_tag, mapper_root, targets_element)
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)

    def test_create_xpath(self):
        response_tag = self._schema.elements.get("EnviarLoteRpsResposta")
        end_tag = "Codigo"
        xpath = create_xpath(response_tag, end_tag)
        xpath_formatted = format_result(xpath)
        self.assertEqual(xpath_formatted, "/EnviarLoteRpsResposta/ListaMensagemRetorno/MensagemRetorno/Codigo")


if __name__ == "__main__":
    main()
