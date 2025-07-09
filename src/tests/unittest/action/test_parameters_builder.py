from unittest import TestCase, main

import lxml.etree as etree

from src.core.action import ParametersBuilder
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestParametersBuilder(TestCase):
    def setUp(self):
        self._builder = ParametersBuilder()
        self._output_file = build_output_file_path("parameters_builder_test_consulta.xml")

    def test_build(self):
        root = etree.Element("root")
        tree = self._builder.build(root, "Consulta")
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)

    def test_build_emissao(self):
        self._output_file = build_output_file_path("parameters_builder_test_emissao.xml")
        root = etree.Element("root")
        tree = self._builder.build(root, "Emissao")
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
