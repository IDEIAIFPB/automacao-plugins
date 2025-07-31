from unittest import TestCase, main

import xmlschema
from lxml import etree

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
        schema_attr = xmlschema.XMLSchema(xml_content)

        self._attribute_group = schema_attr.attribute_groups["meuGrupoAtributos"]

    def test_build(self):
        tree = etree.Element("root")
        self._builder.build(tree, self._attribute_group)

        expected = """<root>
  <attributes>
    <attribute name="id">
      <value>
        <sources>
          <random rangeStart="100000000" rangeEnd="999999999"/>
        </sources>
      </value>
    </attribute>
    <attribute name="nome">
      <value>
        <sources>
          <static value="TODO"/>
        </sources>
      </value>
    </attribute>
    <attribute name="ativo">
      <value>
        <sources>
          <static value="true"/>
        </sources>
      </value>
    </attribute>
  </attributes>
</root>
"""

        self.assertEqual(expected, get_xml(tree))


if __name__ == "__main__":
    main()
