from unittest import TestCase, main

import xmlschema

from src.core.mapper import MapperBuilder
from src.core.utils.xml_utils import get_xml


class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = MapperBuilder()
        self._schema = xmlschema.XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = self._schema.elements.get("GerarNfseEnvio")
        self._plugin_id = "emissao-teste"
        with open("src/tests/resources/mapper.xml") as file:
            self._emissao_tree = file.read()  # carrega uma request gerada pela automação

    def test_build(self):
        tree = self._builder.build(self._plugin_id, self._root)

        self.assertEqual(self._emissao_tree, get_xml(tree))


if __name__ == "__main__":
    main()
