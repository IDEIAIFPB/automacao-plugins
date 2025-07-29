from unittest import TestCase, main

import xmlschema

from src.core.mapper import MapperBuilder


class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = MapperBuilder()
        self._schema = xmlschema.XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = self._schema.elements.get("GerarNfseEnvio")
        self._plugin_id = "emissao-teste"
        with open("src/tests/resources/mapper.xml") as file:
            self._emissao_tree = file.read()  # carrega uma request gerada pela automação

    # def test_build(self):
    #     tree = self._builder.build(self._plugin_id, self._root)

    #     try:
    #         self._schema.validate(self._emissao_tree)
    #     except XMLSchemaValidationError as e:  # apenas para tornar o lançamernto da exceção mais semântico
    #         raise AssertionError(f"O XML não é compatível com o schema: {e.message}")


if __name__ == "__main__":
    main()
