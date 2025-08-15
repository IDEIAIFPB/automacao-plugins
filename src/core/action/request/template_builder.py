import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_builder import ElementBuilder
from src.core.utils.xml_utils import get_element_by_message_name


class TemplateBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "template"

    def build(
        self,
        tree: _Element,
        wsdl_root: _Element,
        binding_operation: _Element,
        final_envelope_tag: str,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        template = etree.SubElement(tree, self._tag, {"inputResultVariable": "REQUEST_CONTENT"})
        self._build(template, wsdl_root, binding_operation, final_envelope_tag, namespaces, wsdl_schema_root)
        return tree

    def _build(
        self,
        tree: _Element,
        wsdl_root: _Element,
        binding_operation: _Element,
        envelope_final_tag: str,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        envelope = self._get_envelope(wsdl_root, binding_operation, envelope_final_tag, namespaces, wsdl_schema_root)
        tree.text = etree.CDATA(envelope)

        return tree

    def _mount_header(
        self,
        xsd_root: _Element,
        wsdl_header: _Element,
        envelope_nsmap: dict,
        envelope: _Element,
        wsdl_root: _Element,
        namespaces: dict,
        target_namespace: str = None,
    ):
        header_tag = etree.SubElement(envelope, etree.QName(envelope_nsmap["soapenv"], "Header"))
        if wsdl_header is None:
            return
        message_name = wsdl_header.get("message").split(":")[-1]
        element_name = get_element_by_message_name(message_name, wsdl_root, namespaces)
        elemento = xsd_root.find(
            f"./xsd:element[@name='{element_name}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        self._mount_envelope(elemento, header_tag, xsd_root, target_namespace=target_namespace)

    def _get_envelope(
        self,
        wsdl_root: _Element,
        binding_operation: _Element,
        envelope_final_tag: str,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        target_namespace = wsdl_schema_root.get("targetNamespace")

        envelope_nsmap = {
            "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            "tns": target_namespace,
            "xd": "http://www.w3.org/2000/09/xmldsig#",
        }

        envelope = etree.Element(etree.QName(envelope_nsmap["soapenv"], "Envelope"), nsmap=envelope_nsmap)
        wsdl_header = binding_operation.find("wsdl:input/soap:header", namespaces=namespaces)

        self._mount_header(
            wsdl_schema_root, wsdl_header, envelope_nsmap, envelope, wsdl_root, namespaces, target_namespace
        )

        operation = self._find_operation(binding_operation, wsdl_root, namespaces)

        input = operation.find("wsdl:input", namespaces=namespaces)

        if input is None:
            raise ValueError("Input não encontrado")

        message_name = input.get("message").split(":")[-1]

        element_name = get_element_by_message_name(message_name, wsdl_root, namespaces)

        body = etree.SubElement(envelope, etree.QName(envelope_nsmap["soapenv"], "Body"))
        element = wsdl_schema_root.find(
            f"./xsd:element[@name='{element_name}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        self._mount_envelope(element, body, wsdl_schema_root, envelope_final_tag, target_namespace)

        return self._export_template_xml(envelope)

    def _find_operation(self, binding_operation: _Element, wsdl_root: _Element, namespaces: dict):
        bindig_operation_name = binding_operation.get("name")

        operation = wsdl_root.find(
            f"./wsdl:portType/wsdl:operation[@name='{bindig_operation_name}']",
            namespaces=namespaces,
        )

        if operation is None:
            raise ValueError("Operation não encontrada")
        return operation

    def _export_template_xml(self, envelope: _Element) -> str:
        xml_bytes = etree.tostring(envelope, pretty_print=True, encoding="utf-8", xml_declaration=True)
        return xml_bytes.decode("utf-8")

    def _map_complex_type(self, complex_type, parent, wsdl_schema_root, tag_final, target_namespace=None):
        elements = complex_type.findall(".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})
        for element in elements:
            self._mount_envelope(element, parent, wsdl_schema_root, tag_final, target_namespace)

    def _mount_envelope(
        self,
        element: _Element,
        parent: _Element,
        wsdl_schema_root: _Element,
        envelope_final_tag: str = None,
        target_namespace: str = None,
    ):
        elements = element.findall(".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})
        name = element.get("name")
        if name is None or name == envelope_final_tag:
            parent.text = "REQUEST_CONTENT"
            return
        parent = etree.SubElement(parent, etree.QName(target_namespace, name))

        if wsdl_schema_root.get("elementFormDefault") != "qualified":
            target_namespace = None
        for internal_element in elements:
            self._mount_envelope(internal_element, parent, wsdl_schema_root, envelope_final_tag, target_namespace)
            return

        if element.get("type") is not None:
            type = element.get("type").split(":")[-1]
            complex_type = wsdl_schema_root.find(
                f"./xsd:complexType[@name='{type}']", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            )

            if complex_type is not None:
                atributo = complex_type.find("./xsd:attribute", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})

                if atributo is not None:
                    parent.set(atributo.get("name"), "?")

            if complex_type is not None:
                self._map_complex_type(complex_type, parent, wsdl_schema_root, envelope_final_tag, target_namespace)
                return

        parent.text = "?"
