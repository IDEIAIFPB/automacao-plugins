import unittest
from dataclasses import dataclass

from lxml import etree

from src.core.mapper.enum.source_type import SourceType
from src.core.mapper.value.value_builder import ValueBuilder
from src.core.utils.xml_utils import build_output_file_path, get_xml


@dataclass
class Source:
    def __init__(self, content: str, args: dict):
        self.content = content
        self.args = args


class TestValueBuilder(unittest.TestCase):
    def setUp(self):
        self._value_builder = ValueBuilder()
        self._output_file = build_output_file_path("value_builder_test.xml")
        self._xpath = "ConsultarNfseRpsEnvio/Prestador/InscricaoMunicipal"

        # args
        self._static_args = {"value": "teste"}
        self._random_args = {"rangeStart": "100000000", "rangeEnd": "999999999"}
        self._variable_args = {"variableId": "teste"}
        self._parameter_args = {"name": "teste"}
        self._xml_args = {"xpath": self._xpath}

        self._xml_property = Source(
            """<root>
  <value>
    <sources>
      <xmlProperty xpath="/SynchroId/PedidoConsultaNFe/Detalhe/ChaveRPS/InscricaoPrestador"/>
    </sources>
  </value>
</root>
""",
            self._xml_args,
        )

        self._static = Source(
            """<root>
  <value>
    <sources>
      <static value="teste"/>
    </sources>
  </value>
</root>
""",
            self._static_args,
        )

        self._random = Source(
            """<root>
  <value>
    <sources>
      <random rangeStart="100000000" rangeEnd="999999999"/>
    </sources>
  </value>
</root>
""",
            self._random_args,
        )

        self._variable = Source(
            """<root>
  <value>
    <sources>
      <variable variableId="teste"/>
    </sources>
  </value>
</root>
""",
            self._variable_args,
        )

        self._parameter = Source(
            """<root>
  <value>
    <sources>
      <parameter name="teste"/>
    </sources>
  </value>
</root>
""",
            self._parameter_args,
        )

        self._sources = {
            SourceType.XML_PROPERTY: self._xml_property,
            SourceType.STATIC: self._static,
            SourceType.PARAMETER: self._parameter,
            SourceType.RANDOM: self._random,
            SourceType.VARIABLE: self._variable,
        }

    def test_build(self):
        for type, source in self._sources.items():
            tree = etree.Element("root")  # reseta a arvore
            self._value_builder.build(tree, type, source.args)
            xml = get_xml(tree)
            self.assertEqual(source.content, xml)


if __name__ == "__main__":
    unittest.main()
