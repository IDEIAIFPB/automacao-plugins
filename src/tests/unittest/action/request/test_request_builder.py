from unittest import TestCase, main

import lxml.etree as etree

from src.core.action import ActionBuilder
from src.core.action.request import RequestBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, get_xml


class TestRequestBuilder(TestCase):
    def setUp(self):
        self._builder = RequestBuilder()
        self._action_builder = ActionBuilder()
        self._xsd_file = "resources/xsd-files/nfse-v2-04.xsd"
        output_file = build_output_file_path("cli.xml")
        self._final_envelope_tag = "GerarNfseEnvio"
        parser = Mapper(self._final_envelope_tag, "teste", self._xsd_file, output_file)
        parser.build()
        self._signatures = parser._mapper_builder.metadata.signature
        self._operation_tag = "GerarNfse"
        self._wsdl_path = "resources/wsdl-files/nfse04.wsdl"
        self._file_type = "emissao"
        self._root = etree.Element("teste")
        self._wsdl_tree = etree.parse(self._wsdl_path)
        self._wsdl_root = self._wsdl_tree.getroot()
        self._namespaces = self._wsdl_root.nsmap
        self._wsdl_schema_root = self._action_builder._parse_wsdl_schema(self._wsdl_root, self._namespaces)
        self.maxDiff = None
        self._request_str = """<teste>
  <request>
    <endpoint>
      <urlParameterName>url-endpoint-emissao</urlParameterName>
      <method>POST</method>
      <tls>TLSv1.2</tls>
    </endpoint>
    <headers>
      <commonHeader name="Content-Type" value="text/xml;charset=UTF-8"/>
      <commonHeader name="SOAPAction" value="https://tributosmunicipais.com.br/nfse/api/GerarNfse"/>
    </headers>
    <body>
      <input>
        <document-mapper>emissao-mapper.xml</document-mapper>
        <signatures>
          <signature target="InfDeclaracaoPrestacaoServico" type="ELEMENT" parent="Rps" attribute="id"/>
        </signatures>
      </input>
      <content>
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
      </content>
    </body>
  </request>
</teste>
"""

        self._binding_operation_expected = self._wsdl_root.find(
            f"./wsdl:binding/wsdl:operation[@name='{self._operation_tag}']",
            namespaces=self._namespaces,
        )
        self._soap_action_expected = "https://tributosmunicipais.com.br/nfse/api/GerarNfse"

    def test_build(self):
        tree = self._builder.build(
            self._root,
            self._signatures,
            self._operation_tag,
            self._final_envelope_tag,
            self._file_type,
            self._wsdl_root,
            self._namespaces,
            self._wsdl_schema_root,
        )
        s_tree = get_xml(tree)
        self.assertEqual(s_tree, self._request_str)

    def test_get_binding_operation(self):
        binding_operation = self._builder._get_binding_operation(self._wsdl_root, self._operation_tag, self._namespaces)
        self.assertIsNotNone(binding_operation)
        self.assertEqual(binding_operation, self._binding_operation_expected)

    def test_get_soap_action(self):
        binding_operation = self._builder._get_binding_operation(self._wsdl_root, self._operation_tag, self._namespaces)
        soap_action = self._builder._get_soap_action(binding_operation, self._namespaces)
        self.assertEqual(soap_action, self._soap_action_expected)


if __name__ == "__main__":
    main()
