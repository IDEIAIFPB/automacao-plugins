from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.utils.xml_utils import create_xpath, format_result, get_element_by_message_name, get_xml


class TestXmlUtils(TestCase):
    def setUp(self):
        self._tree = etree.Element("teste")
        self._tree.text = "Teste get_xml"
        self._tree_str = """<teste>Teste get_xml</teste>
"""
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._initial_element = self._schema.elements.get("CancelarNfseResposta")
        self._final_element = "Codigo"
        self._return_create_xpath = ["CancelarNfseResposta", "ListaMensagemRetorno", "MensagemRetorno", "Codigo"]

        self._formated_xpath = "/CancelarNfseResposta/ListaMensagemRetorno/MensagemRetorno/Codigo"

        wsdl_tree = etree.parse("resources/wsdl-files/nfse04.wsdl")
        self._wsdl_root = wsdl_tree.getroot()
        self._namespaces = self._wsdl_root.nsmap
        self._element_expected = "CancelarNfseRequest"
        self._message_name = "CancelarNfseRequest"

    def test_get_xml(self):
        s_tree = get_xml(self._tree)
        self.assertEqual(s_tree, self._tree_str)

    def test_create_xpath(self):
        result = create_xpath(self._initial_element, self._final_element)
        self.assertEqual(result, self._return_create_xpath)

    def test_format_result(self):
        result = format_result(self._return_create_xpath)
        self.assertEqual(result, self._formated_xpath)

    def test_get_element_by_message_name(self):
        element = get_element_by_message_name(self._message_name, self._wsdl_root, self._namespaces)
        self.assertEqual(element, self._element_expected)


if __name__ == "__main__":
    main()
