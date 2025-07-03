from unittest import TestCase, main

import xmlschema
from src.core.mapper import MapperBuilder
import lxml.etree as etree

from src.tests.utils.constants import build_output_file_path

class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = MapperBuilder()
        self._schema = xmlschema.XMLSchema("xsd-files/NFSE.xsd.XSD")
        self._root = "EnviarLoteRpsEnvio"
        self._plugin_id = "emissao-itaperuna"
        self._output_file = build_output_file_path("mapper_builder_test.xml")

    def test_build(self):
        tree = self._builder.build(self._root, self._plugin_id, self._schema)
        s_tree = etree.tostring(tree, encoding='unicode', pretty_print = True)
        with open(self._output_file, "w") as f:
            f.write(s_tree)

if __name__ == "__main__":
    main()