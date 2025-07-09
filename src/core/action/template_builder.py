import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder


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
    ):
        template = etree.SubElement(tree, self._tag)
        self._build(template, wsdl_root, binding_operation, final_envelope_tag, namespaces)
        return tree

    def _build(
        self,
        tree: _Element,
        wsdl_root: _Element,
        binding_operation: _Element,
        envelope_final_tag: str,
        namespaces: dict,
    ):
        envelope = self._get_envelope(wsdl_root, binding_operation, envelope_final_tag, namespaces)
        tree.text = etree.CDATA(envelope)

        return tree

    def _parse_xsd(self, tree: _Element, namespaces: dict):
        schema = tree.find("./wsdl:types/xsd:schema", namespaces=namespaces)

        if schema is None:
            raise ValueError("Schema não encontrado")

        xsd_importado = schema.find("./xsd:import", namespaces=namespaces)
        initial_xsd = xsd_importado.get("schemaLocation") if xsd_importado is not None else None

        if initial_xsd is None:
            with open("schema_extraido.xsd", "wb") as f:
                f.write(etree.tostring(schema))
            initial_xsd = "schema_extraido.xsd"

        return etree.parse(initial_xsd)

    def _get_element_by_message_name(self, message_name: str, wsdl_root: _Element, namespaces: dict):
        message = wsdl_root.find(f"./wsdl:message[@name='{message_name}']", namespaces=namespaces)

        if message is None:
            raise ValueError("Message não encontrado")

        part = message.find("./wsdl:part", namespaces=namespaces)

        return part.get("element").split(":")[-1]

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
        if wsdl_header is not None:
            message_name = wsdl_header.get("message").split(":")[-1]
            element_name = self._get_element_by_message_name(message_name, wsdl_root, namespaces)
            elemento = xsd_root.find(
                f"./xsd:element[@name='{element_name}']",
                namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
            )
            self._mount_envelope(elemento, header_tag, xsd_root, target_namespace=target_namespace)

    def _get_envelope(
        self, wsdl_root: _Element, binding_operation: _Element, envelope_final_tag: str, namespaces: dict
    ):
        xsd = self._parse_xsd(wsdl_root, namespaces)

        xsd_root = xsd.getroot()
        target_namespace = xsd_root.get("targetNamespace")

        envelope_nsmap = {
            "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
            "tns": target_namespace,
            "xd": "http://www.w3.org/2000/09/xmldsig#",
        }

        envelope = etree.Element(etree.QName(envelope_nsmap["soapenv"], "Envelope"), nsmap=envelope_nsmap)
        wsdl_header = binding_operation.find("wsdl:input/soap:header", namespaces=namespaces)

        self._mount_header(xsd_root, wsdl_header, envelope_nsmap, envelope, wsdl_root, namespaces, target_namespace)

        bindig_operation_name = binding_operation.get("name")

        operation = wsdl_root.find(
            f"./wsdl:portType/wsdl:operation[@name='{bindig_operation_name}']",
            namespaces=namespaces,
        )

        if operation is None:
            raise ValueError("Operation não encontrada")

        input = operation.find("wsdl:input", namespaces=namespaces)

        if input is None:
            raise ValueError("Input não encontrado")

        message_name = input.get("message").split(":")[-1]

        element_name = self._get_element_by_message_name(message_name, wsdl_root, namespaces)

        body = etree.SubElement(envelope, etree.QName(envelope_nsmap["soapenv"], "Body"))
        element = xsd.find(
            f"./xsd:element[@name='{element_name}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        self._mount_envelope(element, body, xsd_root, envelope_final_tag, target_namespace)

        return etree.tostring(envelope, pretty_print=True, encoding="utf-8", xml_declaration=True).decode("utf-8")

    def _map_complex_type(self, complex_type, parent, xsd_root, tag_final, target_namespace=None):
        elements = complex_type.findall(".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})
        for element in elements:
            self._mount_envelope(element, parent, xsd_root, tag_final, target_namespace)

    def _mount_envelope(
        self,
        element: _Element,
        parent: _Element,
        xsd_root: _Element,
        envelope_final_tag: str = None,
        target_namespace: str = None,
    ):
        elements = element.findall(".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})
        name = element.get("name")
        if name is None or name == envelope_final_tag:
            parent.text = "REQUEST_CONTENT"
            return
        parent = etree.SubElement(parent, etree.QName(target_namespace, name))

        if xsd_root.get("elementFormDefault") != "qualified":
            target_namespace = None
        for internal_element in elements:
            self._mount_envelope(internal_element, parent, xsd_root, envelope_final_tag, target_namespace)
            return

        if element.get("type") is not None:
            type = element.get("type").split(":")[-1]
            complex_type = xsd_root.find(
                f"./xsd:complexType[@name='{type}']", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            )

            if complex_type is not None:
                atributo = complex_type.find("./xsd:attribute", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})

                if atributo is not None:
                    parent.set(atributo.get("name"), "?")

            if complex_type is not None:
                self._map_complex_type(complex_type, parent, xsd_root, envelope_final_tag, target_namespace)
                return

        parent.text = "?"
