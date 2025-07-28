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
            self._emissao_tree = file.read().replace("\n", "")

    def test_build(self):
        xml = self._builder.build(self._plugin_id, self._root)

        with open("teste.xml", "w") as file:
            file.write(get_xml(xml))


if __name__ == "__main__":
    main()
