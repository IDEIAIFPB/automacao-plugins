from xmlschema.validators import XsdElement
from src.core.element_mapper import ElementMapper
from lxml import etree

from src.core.mapper.data.properties_loader import JsonProperties

class ValueBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._props = JsonProperties()
        self._tag = "value"
    
    def build(self, tree: etree._Element, xpath: str):
        value_element = etree.SubElement(tree, self._tag)
        self._build_source(value_element, xpath)

        return tree

    def _build_source(self, parent: etree._Element, xpath: str) -> etree._Element: 
        sources_tag = "sources"
        sources_element = etree.SubElement(parent, sources_tag)
        xml_property = etree.SubElement(sources_element, "xmlProperty", {"xpath": self._props.get(xpath)})
        return parent

    def _build_operations(self, tree: etree._Element) -> etree: return tree