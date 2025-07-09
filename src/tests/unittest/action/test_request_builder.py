from unittest import TestCase, main

import lxml.etree as etree

from src.core.action import RequestBuilder
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestRequestBuilder(TestCase):
    def setUp(self):
        self._builder = RequestBuilder()
        self._signatures = [
            {"parent": "parent1", "target": "target1", "type": "type1"},
            {"parent": "parent2", "target": "target2", "type": "type2"},
        ]
        self._output_file = build_output_file_path("request_builder_test.xml")
        self._operation_tag = "RecepcionarLoteRps"
        self._wsdl_path = "wsdl-files/nfse04.wsdl"
        self._final_envelope_tag = "EnviarLoteRpsEnvio"
        self._file_type = "emissao"

    def test_build(self):
        root = etree.Element("teste")
        tree = self._builder.build(
            root, self._signatures, self._operation_tag, self._wsdl_path, self._final_envelope_tag, self._file_type
        )
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
