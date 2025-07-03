from unittest import TestCase, main

import xmlschema
from src.core.mapper import PropertiesBuilder
import lxml.etree as etree

class TestPropertiesBuilder(TestCase):
    def setUp(self):
        self._builder = PropertiesBuilder()
        _schema = xmlschema.XMLSchema("xsd-files/NFSE.xsd.XSD")
        self._xsd_element = (_schema.elements.get("EnviarLoteRpsEnvio")) 

    def test_build(self):
        root = etree.Element("root")
        tree = self._builder.build(root, self._xsd_element)
        s_tree = etree.tostring(tree, encoding='unicode')
        with open("./src/tests/temp/teste.xml", "w") as f:
            f.write(s_tree)

if __name__ == "__main__":
    main()