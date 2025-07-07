from lxml.etree import _Element
from xmlschema.validators import XsdElement

from src.core.element_mapper import ElementBuilder


class RequestBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = ""

    def build(self, plugin_id: str, signatures: list, operation_tag: str, wsdl_path: str):
        pass

    def _build(self, xml_root: _Element, xsd_element: XsdElement):
        pass
