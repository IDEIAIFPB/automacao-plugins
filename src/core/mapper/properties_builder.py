from typing import Optional
from xmlschema.validators import XsdElement, XsdGroup, XsdAttribute

from src.core.element_mapper import ElementMapper
import lxml.etree as etree

from src.core.mapper.value_builder import ValueBuilder

class PropertiesBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._tag = "properties"
        self._value_builder = ValueBuilder()
        self._visited = set()

    def _get_element_name(self, element: XsdElement) -> str:
        return element.local_name

    def _build_xpath(self, element: XsdElement, xpath: str):
        name = self._get_element_name(element)
        if not xpath:
            return f"/{name}"
        return f"{xpath}/{name}"
    
    def build(self, tree: etree._Element, xsd_element: XsdElement):
        root = etree.SubElement(tree, "properties")
        self._build(xsd_element, root)
        return tree # props !document-mapper

    def _is_element_available(self, xsd_element: XsdElement) -> bool:
        if self._get_element_name(xsd_element) == "Signature":
            return False
        if xsd_element in self._visited:
            return False
        return True
    def _build(self, xsd_element: XsdElement, tree: Optional[etree._Element] = None, xpath = ""):
        name = self._get_element_name(xsd_element)
        if not self._is_element_available(xsd_element):
            return tree

        self._visited.add(xsd_element)

        property = etree.SubElement(tree, "property", {"name": name})

        current_path = self._build_xpath(xsd_element, xpath)

        xsd_type = xsd_element.type

        is_not_group = not isinstance(xsd_element, XsdGroup)
        has_no_content = not getattr(xsd_type, 'content', False) # tipos anonimos

        if is_not_group and has_no_content:
            self._value_builder.build(property, current_path)
            return tree

        properties = etree.SubElement(property, "properties")
        for sub_element in xsd_element:
            self._build(sub_element, properties, current_path)

        return tree