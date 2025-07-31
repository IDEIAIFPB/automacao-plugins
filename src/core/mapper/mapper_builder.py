import lxml.etree as etree
from lxml.etree import _Element
from xmlschema.validators import XsdElement

from src.core.element_builder import ElementBuilder
from src.core.mapper.properties_builder import PropertiesBuilder


class MapperBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "document-mapper"
        self._properties_builder = PropertiesBuilder()

    @property
    def metadata(self):
        return self._properties_builder.metadata

    def build(self, plugin_id: str, xsd_element: _Element):
        xml_root = etree.Element(
            "document-mapper",
            {
                "id": plugin_id,
                "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": "../../../schemas/document-mapping.xsd",
            },
            nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"},
        )

        self._build(xml_root, xsd_element)
        return xml_root

    def _build(self, xml_root: _Element, xsd_element: XsdElement):
        self._properties_builder.build(xml_root, xsd_element)
