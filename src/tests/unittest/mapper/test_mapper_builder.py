from unittest import TestCase, main

import xmlschema

from src.core.mapper import MapperBuilder


class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = MapperBuilder()
        self._schema = xmlschema.XMLSchema("resources/xsd-files/nfse-v2-02.xsd")
        self._root = self._schema.elements.get("EnviarLoteRpsEnvio")
        self._plugin_id = "emissao-itaperuna"

    def test_build(self):
        pass


if __name__ == "__main__":
    main()
