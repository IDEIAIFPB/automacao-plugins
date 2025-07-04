from unittest import TestCase, main

import xmlschema
from src.core.mapper import MapperBuilder

from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = MapperBuilder()
        self._schema = xmlschema.XMLSchema("resources/xsd-files/nfse-v2-02.xsd")
        self._root = "EnviarLoteRpsEnvio"
        self._plugin_id = "emissao-itaperuna"
        self._output_file = build_output_file_path("mapper_builder_test.xml")

    def test_build(self):
        tree = self._builder.build(self._root, self._plugin_id, self._schema)
        teste = self._builder.metadata
        print(teste)
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
