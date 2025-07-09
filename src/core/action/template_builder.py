import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder


class TemplateBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "template"

    def build(self, tree: _Element, operation_tag: str, wsdl: _Element, final_envelope_tag: str = None):
        template = etree.SubElement(tree, self._tag)
        self._build(template, operation_tag, wsdl, final_envelope_tag)
        return tree

    def _build(self, tree: _Element, operation_tag: str, wsdl: _Element, final_envelope_tag: str = None):
        envelope = self._get_envelope(wsdl, operation_tag, final_envelope_tag)
        if envelope is not None:
            tree.append(envelope)
        return tree

    def _get_envelope(self, wsdl: _Element, operation_tag: str, final_envelope_tag: str = None):
        namespaces = wsdl.getroot().nsmap
        port_type = wsdl.find("./wsdl:portType", namespaces=namespaces)

        if port_type is None:
            return None

        operation = port_type.find(f"./wsdl:operation[@name='{operation_tag}']", namespaces=namespaces)
        if operation is None:
            return None

        envelope = etree.Element(final_envelope_tag or "Envelope")
        etree.SubElement(envelope, "Header")
        body = etree.SubElement(envelope, "Body")
        etree.SubElement(body, operation_tag)

        return envelope
