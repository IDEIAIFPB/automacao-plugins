from xmlschema.validators import XsdElement, XsdGroup, XsdAttribute

from src.core.element_mapper import ElementMapper
import lxml.etree as etree

from src.core.mapper.value_builder import ValueBuilder

class PropertiesBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._tag = "properties"
        self._value_builder = ValueBuilder()

    def build_xml(self):
        return super().build_xml()
    
    def build(self, tree: etree._Element, xsd_element: XsdElement, xpath = ""):
        if not isinstance(xsd_element, XsdGroup):
            self._value_builder.build(tree, xsd_element, xpath)

        properties = tree.SubElement(tree, "properties")
        for sub_element in xsd_element:
            self.build(properties, sub_element)
        
        self._tree = tree
        return tree