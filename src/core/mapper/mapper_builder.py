from src.core.element_mapper import ElementBuilder
import lxml.etree as etree
from lxml.etree import _Element
from xmlschema import XMLSchema
from xmlschema.validators import XsdElement

from src.core.mapper.properties_builder import PropertiesBuilder


class MapperBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "document-mapper"
        self._properties_builder = PropertiesBuilder()
    
    @property
    def metadata(self):
        return self._properties_builder.metadata

    def build(self, root: str, plugin_id: str, schema: XMLSchema):
        xml_root = etree.Element(
            "document-mapper",
            {
                "id": plugin_id,
                "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": "../../../schemas/document-mapper.xsd",
            },
            nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"},
        )
        xsd_element = schema.elements.get(root)
        if xsd_element is None:
            raise ValueError(f"Elemento '{root}' não achado no schema.")
        self._build(xml_root, xsd_element)
        return xml_root

    def _build(self, xml_root: _Element, xsd_element: XsdElement):
        self._properties_builder.build(xml_root, xsd_element)
