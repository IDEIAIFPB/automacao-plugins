import re
import unittest

from lxml import etree

from src.core.mapper.enum.source_type import SourceType
from src.core.mapper.value.value_builder import ValueBuilder
from src.core.utils.xml_utils import build_output_file_path, get_xml


class TestValueBuilder(unittest.TestCase):
    def setUp(self):
        self._value_builder = ValueBuilder()
        self._output_file = build_output_file_path("value_builder_test.xml")
        self._xpath = "ConsultarNfseRpsEnvio/Prestador/InscricaoMunicipal"

        # args
        self._static_args = {"value": "teste"}
        self._random_args = {"rangeStart": 100000000, "rangeEnd": 999999999}
        self._variable_args = {"variableId": "teste"}
        self._parameter_args = {"name": "teste"}
        self._xml_args = {"xpath": self._xpath}

        self._unindent = lambda x: re.sub(r"\r?\n[ \t]+", "", x)

        # xml
        self._xml_property = self._unindent("""
        <root>
            <value>
                <sources>
                    <xmlProperty xpath="/SynchroId/PedidoConsultaNFe/Detalhe/ChaveRPS/InscricaoPrestador"/>
                </sources>
            </value>
        </root>
        """)

        self._static = self._unindent("""
        <root>
            <value>
                <sources>
                    <static value="teste"/>
                </sources>
            </value>
        </root>
        """)

        self._random = self._unindent("""
        <root>
            <value>
                <sources>
                    <random rangeEnd="999999999" rangeStart="100000000"/>
                </sources>
            </value>
        </root>
        """)

        self._variable = self._unindent("""
        <root>
            <value>
                <sources>
                    <variable variableId="teste"/>
                </sources>
            </value>
        </root>
        """)

        self._parameter = self._unindent("""
        <root>
            <value>
                <sources>
                    <parameter name="teste"/>
                </sources>
            </value>
        </root>
        """)

    def test_build_xml_prop(self):
        tree = etree.Element("root")
        self._value_builder.build(tree, SourceType.XML_PROPERTY, self._xml_args)
        xml = self._unindent(get_xml(tree))
        # xml = get_xml(tree)
        print(etree.fromstring(xml))
        print(etree.fromstring(self._xml_property))

        xml: etree._Element = etree.fromstring(xml)

        teste = xml.__eq__(etree.fromstring(self._xml_property))

        print(teste)
        # self.assertEqual(etree.fromstring(self._xml_property), etree.fromstring(xml))

    # def test_build_param(self):
    #     tree = etree.Element("root")
    #     self._value_builder.build(tree, SourceType.PARAMETER, self._parameter_args)
    #     xml = get_xml(final_tree)
    #     export_xml_to_file(xml, self._output_file)

    # def test_build_static(self):
    #     tree = etree.Element("root")
    #     self._value_builder.build(tree, SourceType.STATIC, self._static_args)
    #     xml = get_xml(final_tree)
    #     export_xml_to_file(xml, self._output_file)

    # def test_build_random(self):
    #     tree = etree.Element("root")
    #     self._value_builder.build(tree, SourceType.RANDOM, self._random_args)
    #     xml = get_xml(final_tree)
    #     export_xml_to_file(xml, self._output_file)

    # def test_build_variable(self):
    #     tree = etree.Element("root")
    #     self._value_builder.build(tree, SourceType.VARIABLE, self._variable_args)
    #     xml = get_xml(final_tree)
    #     export_xml_to_file(xml, self._output_file)


if __name__ == "__main__":
    unittest.main()
