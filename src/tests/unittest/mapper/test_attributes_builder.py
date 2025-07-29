from unittest import TestCase, main

import xmlschema

from src.core.mapper import AttributesBuilder
from src.core.utils.xml_utils import get_xml


class TestMapperBuilder(TestCase):
    def setUp(self):
        self._builder = AttributesBuilder()
        xml_content = """
<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">
    <xs:attributeGroup name="meuGrupoAtributos">
        <xs:attribute name="id" type="xs:string" use="required"/>
        <xs:attribute name="nome" type="xs:string" use="optional"/>
        <xs:attribute name="ativo" type="xs:boolean" default="true"/>
    </xs:attributeGroup>
</xs:schema>
"""

        # Criar o schema a partir do XML
        schema = xmlschema.XMLSchema(xml_content)

        # Acessar o attribute group do schema
        attribute_group = schema.all_attributes["meuGrupoAtributos"]
        print(f"Nome do grupo: {attribute_group.name}")
        print(f"Tipo: {type(attribute_group)}")
        print(f"Atributos no grupo: {list(attribute_group.iter_attributes())}")

        self._plugin_id = "emissao-teste"
        with open("src/tests/resources/mapper.xml") as file:
            self._emissao_tree = file.read()  # carrega uma request gerada pela automação

    def test_build(self):
        tree = self._builder.build()

        self.assertEqual(self._emissao_tree, get_xml(tree))


if __name__ == "__main__":
    main()
