from unittest import TestCase, main

import lxml.etree as etree

from src.core.action import ActionBuilder
from src.core.action.request.template_builder import TemplateBuilder
from src.core.utils.xml_utils import get_xml


class TestTemplateBuilder(TestCase):
    def setUp(self):
        self._builder = TemplateBuilder()
        self._action_builder = ActionBuilder()
        self._xsd_file = "resources/xsd-files/nfse-v2-04.xsd"
        self._final_envelope_tag = "GerarNfseEnvio"
        self._operation_tag = "GerarNfse"
        self._wsdl_path = "resources/wsdl-files/nfse04.wsdl"
        self._root = etree.Element("teste")
        self._wsdl_tree = etree.parse(self._wsdl_path)
        self._wsdl_root = self._wsdl_tree.getroot()
        self._namespaces = self._wsdl_root.nsmap
        self._wsdl_schema_root = self._action_builder._parse_wsdl_schema(self._wsdl_root, self._namespaces)
        self.maxDiff = None
        self._template_str = """<teste>
  <template inputResultVariable="REQUEST_CONTENT"><![CDATA[<?xml version='1.0' encoding='utf-8'?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="https://tributosmunicipais.com.br/nfse/api/" xmlns:xd="http://www.w3.org/2000/09/xmldsig#">
  <soapenv:Header/>
  <soapenv:Body>
    <tns:GerarNfseRequest>
      <nfseCabecMsg>
        <cabecalho>
          <versaoDados>?</versaoDados>
        </cabecalho>
      </nfseCabecMsg>
      <nfseDadosMsg>REQUEST_CONTENT</nfseDadosMsg>
    </tns:GerarNfseRequest>
  </soapenv:Body>
</soapenv:Envelope>
]]></template>
</teste>
"""

        self._binding_operation = self._wsdl_root.find(
            f"./wsdl:binding/wsdl:operation[@name='{self._operation_tag}']",
            namespaces=self._namespaces,
        )

    def test_build(self):
        tree = self._builder.build(
            self._root,
            self._wsdl_root,
            self._binding_operation,
            self._final_envelope_tag,
            self._namespaces,
            self._wsdl_schema_root,
        )
        s_tree = get_xml(tree)
        self.assertEqual(s_tree, self._template_str)


if __name__ == "__main__":
    main()
