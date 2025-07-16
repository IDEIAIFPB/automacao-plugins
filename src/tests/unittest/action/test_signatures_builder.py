from unittest import TestCase, main

import lxml.etree as etree

from src.core.action.request import SignaturesBuilder
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestSignaturesBuilder(TestCase):
    def setUp(self):
        self._builder = SignaturesBuilder()
        self._signatures = [
            {"parent": "parent1", "target": "target1", "type": "type1"},
            {"parent": "parent2", "target": "target2", "type": "type2"},
        ]
        self._output_file = build_output_file_path("signatures_builder_test.xml")

    def test_build(self):
        root = etree.Element("root")
        tree = self._builder.build(root, self._signatures)
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
