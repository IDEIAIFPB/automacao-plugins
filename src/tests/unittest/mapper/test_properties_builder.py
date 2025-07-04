from unittest import TestCase, main

import xmlschema
from src.core.mapper import PropertiesBuilder
import lxml.etree as etree
from src.tests.utils import build_output_file_path


class TestPropertiesBuilder(TestCase):
    def setUp(self):
        self._builder = PropertiesBuilder()
        _schema = xmlschema.XMLSchema("resources/xsd-files/NFSE.xsd.XSD")
        self._xsd_element = _schema.elements.get("EnviarLoteRpsEnvio")
        self._output_file = build_output_file_path("properties_builder_test.xml")

    def test_build(self):
        root = etree.Element("root")
        tree = self._builder.build(root, self._xsd_element)
        s_tree = etree.tostring(tree, encoding="unicode")
        with open(self._output_file, "w") as f:
            f.write(s_tree)


if __name__ == "__main__":
    main()
