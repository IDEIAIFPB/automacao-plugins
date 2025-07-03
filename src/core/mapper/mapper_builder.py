from src.core.element_mapper import ElementMapper
import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.mapper.properties_builder import PropertiesBuilder

class MapperBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._tag = "document-mapper"
        self._properties_builder = PropertiesBuilder()
    
    def build(self, root: str, plugin_id: str, schema: XMLSchema):
        xml_root = etree.Element("document-mapper", {"id" : plugin_id, "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation" : "../../../schemas/document-mapper.xsd"}, nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"})
        xsd_element = schema.elements.get(root)
        self._properties_builder.build(xml_root, xsd_element)
        return xml_root

    # def _build():