from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action import ParametersBuilder
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


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
        self._output_file = build_output_file_path("parameters_builder_test_emissao.xml")
        root = etree.Element("root")
        response_tag = self._schema.elements.get("EnviarLoteRpsResposta")
        targets_element = ["NumeroLote", "Protocolo", "Aliquota"]
        tree = self._builder.build(root, "Emissao", response_tag, targets_element)
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)

    def test_create_xpath(self):
        response_tag = self._schema.elements.get("EnviarLoteRpsResposta")
        end_tag = "Codigo"
        xpath = self._builder.create_xpath(response_tag, end_tag)
        xpath_formatted = self._builder._format_result(xpath)
        self.assertEqual(xpath_formatted, "/EnviarLoteRpsResposta/ListaMensagemRetorno/MensagemRetorno/Codigo")


if __name__ == "__main__":
    main()
