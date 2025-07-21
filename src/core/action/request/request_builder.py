import lxml.etree as etree
from lxml.etree import _Element

from src.core.action.request import ContentBuilder, SignaturesBuilder
from src.core.element_mapper import ElementBuilder


class RequestBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "request"
        self._signatures_builder = SignaturesBuilder()
        self._content_builder = ContentBuilder()

    def build(
        self,
        tree: _Element,
        signatures: list,
        operation_tag: str,
        final_envelope_tag: str,
        file_type: str,
        wsdl_root: _Element,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        request = etree.SubElement(tree, self._tag)
        self._build(
            request, signatures, operation_tag, final_envelope_tag, file_type, wsdl_root, namespaces, wsdl_schema_root
        )
        return tree

    def _build(
        self,
        tree: _Element,
        signatures: list,
        operation_tag: str,
        final_envelope_tag: str,
        file_type: str,
        wsdl_root: _Element,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        self._build_endpoint(tree, file_type)

        binding_operation = self._get_binding_operation(wsdl_root, operation_tag, namespaces)

        self._build_headers(tree, wsdl_root, operation_tag, namespaces, binding_operation)

        body = self._build_body(tree, file_type, signatures)

        self._content_builder.build(
            body, wsdl_root, binding_operation, final_envelope_tag, namespaces, wsdl_schema_root
        )

        return tree

    def _get_binding_operation(self, wsdl_root: _Element, operation_tag: str, namespaces: dict):
        bindig_operation_name = operation_tag
        bindig_operation = wsdl_root.find(
            f"./wsdl:binding/wsdl:operation[@name='{bindig_operation_name}']",
            namespaces=namespaces,
        )

        if bindig_operation is None:
            raise ValueError("Binding Operation não encontrada")

        return bindig_operation

    def _get_soap_action(self, bindig_operation: _Element, namespaces: dict):
        soap_action = bindig_operation.find("./soap:operation", namespaces=namespaces)
        if soap_action is None:
            raise ValueError("SOAP Action não encontrada")

        return soap_action.get("soapAction")

    def _build_endpoint(self, tree: _Element, file_type: str):
        endpoint = etree.SubElement(tree, "endpoint")

        url_parameter_name = etree.SubElement(endpoint, "urlParameterName")
        url_parameter_name.text = f"url-endpoint-{file_type}"

        method = etree.SubElement(endpoint, "method")
        method.text = "POST"

        tls = etree.SubElement(endpoint, "tls")
        tls.text = "TLSv1.2"

    def _build_headers(
        self, tree: _Element, wsdl_root: _Element, operation_tag: str, namespaces: dict, binding_operation: _Element
    ):
        headers = etree.SubElement(tree, "headers")

        etree.SubElement(headers, "commonHeader", name="Content-Type", value="text/xml;charset=UTF-8")

        soap_action = self._get_soap_action(binding_operation, namespaces)

        etree.SubElement(headers, "commonHeader", name="SOAPAction", value=soap_action)

    def _build_body(self, tree, file_type, signatures):
        body = etree.SubElement(tree, "body")
        input = etree.SubElement(body, "input")
        document_mapper = etree.SubElement(input, "document-mapper")
        document_mapper.text = f"{file_type}-mapper.xml"

        input = self._signatures_builder.build(input, signatures)

        return body
