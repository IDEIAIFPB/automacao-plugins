import lxml.etree as etree
from lxml.etree import _Element

from src.core.action import SignaturesBuilder, TemplateBuilder
from src.core.element_mapper import ElementBuilder


class RequestBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "request"
        self._signatures_builder = SignaturesBuilder()
        self._template_builder = TemplateBuilder()

    def build(
        self,
        tree: _Element,
        signatures: list,
        operation_tag: str,
        wsdl_path: str,
        final_envelope_tag: str,
        file_type: str,
    ):
        request = etree.SubElement(tree, self._tag)
        self._build(request, signatures, operation_tag, wsdl_path, final_envelope_tag, file_type)
        return tree

    def _build(
        self,
        tree: _Element,
        signatures: list,
        operation_tag: str,
        wsdl_path: str,
        final_envelope_tag: str,
        file_type: str,
    ):
        endpoint = etree.SubElement(tree, "endpoint")

        url_parameter_name = etree.SubElement(endpoint, "urlParameterName")
        url_parameter_name.text = f"url-endpoint-{file_type}"

        method = etree.SubElement(endpoint, "method")
        method.text = "POST"

        tls = etree.SubElement(endpoint, "tls")
        tls.text = "TLSv1.2"

        headers = etree.SubElement(tree, "headers")

        etree.SubElement(headers, "commonHeader", name="Content-Type", value="text/xml;charset=UTF-8")
        wsdl_tree = etree.parse(wsdl_path)
        root = wsdl_tree.getroot()
        namespaces = root.nsmap
        binding_operation = self._get_binding_operation(root, operation_tag, namespaces)

        soap_action = self._get_soap_action(binding_operation, namespaces)

        etree.SubElement(headers, "commonHeader", name="SOAPAction", value=soap_action)

        if signatures:
            signatures_element = etree.SubElement(endpoint, "signatures")
            for signature in signatures:
                etree.SubElement(signatures_element, "signature")
        self._template_builder.build(tree, operation_tag, wsdl_tree, final_envelope_tag)

        return tree

    def _get_binding_operation(self, root: _Element, operation_tag: str, namespaces: dict):
        bindig_operation_name = operation_tag
        bindig_operation = root.find(
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
