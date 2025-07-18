from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response import ConditionBuilder
from src.core.utils.constants import CONDITTIONS_MAP
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestConditionBuilder(TestCase):
    def setUp(self):
        self._builder = ConditionBuilder()
        self._output_file = build_output_file_path("conditions_builder_test.xml")
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-02.xsd")

    def test_build(self):
        root = etree.Element("teste")
        response_tag = self._schema.elements.get("CancelarNfseResposta")
        targets_tags = {
            "data_hora": "DataHora",
            "codigo_cancelamento": "Codigo",
        }
        file_type = "cancelamento"
        status_type = "cancelled"
        tree = self._builder.build(
            root, CONDITTIONS_MAP[file_type][status_type], status_type, response_tag, targets_tags
        )
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
