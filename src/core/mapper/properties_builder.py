from dataclasses import dataclass
from typing import Optional
from xmlschema.validators import XsdElement, XsdGroup, XsdAttribute

from src.core.element_mapper import ElementBuilder
import lxml.etree as etree
from lxml.etree import _Element

from src.core.mapper.enum import SourceType
from src.core.mapper.value import ValueBuilder
from src.core.mapper.attributes_builder import AttributesBuilder

@dataclass
class PropertiesMetadata:
    # parent tag (str), target (str)
    signature = list()
    # 
    variable = dict()

class PropertiesBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "properties"
        self._inner_tag = "property"
        self._value_builder = ValueBuilder()
        self._visited = set()
        self._attributes_builder = AttributesBuilder()
        self._metada = PropertiesMetadata()

    @property
    def metadata(self) -> PropertiesMetadata:
        return self._metada

    def _get_element_name(self, element: XsdElement) -> str:
        return element.local_name

    def _build_xpath(self, element: XsdElement, xpath: str):
        name = self._get_element_name(element)
        if not xpath:
            return f"{name}"
        return f"{xpath}/{name}"
    
    def build(self, tree: _Element, xsd_element: XsdElement):
        properties = etree.SubElement(tree, self._tag)
        self._build(xsd_element, properties)
        return tree

    def _is_element_available(self, xsd_element: XsdElement) -> bool:
        if self._get_element_name(xsd_element) == "Signature":
            return False
        if xsd_element in self._visited:
            return False
        return True

    def _build(self, xsd_element: XsdElement, tree: Optional[_Element] = None, xpath = ""):
        name = self._get_element_name(xsd_element)
        if self._get_element_name(xsd_element) == "Signature":
            path_broken = xpath.split("/")
            target = path_broken[-1]
            if len(path_broken) > 1:
                parent = path_broken[-2]
                self._metada.signature.append({"parent": parent, "target": target, "type": "ELEMENT"})
                return tree
            self._metada.signature.append({"target": target, "type": "ELEMENT"})
            return tree
        if xsd_element in self._visited:
            return tree

        # if not self._is_element_available(xsd_element):
        #     return tree

        property: _Element = etree.SubElement(tree, "property", {"name": name})

        current_path = self._build_xpath(xsd_element, xpath)
        
        self._visited.add(current_path)

        xsd_type = xsd_element.type
        attributes = xsd_element.attributes

        if attributes:
            self._attributes_builder.build(property, attributes)

        is_not_group = not isinstance(xsd_element, XsdGroup)
        has_no_content = not getattr(xsd_type, 'content', False) # tipos anonimos

        if is_not_group and has_no_content:
            self._value_builder.build(property, SourceType.XML_PROPERTY, {"xpath": current_path})
            return tree

        properties = etree.SubElement(property, self._tag)
        for sub_element in xsd_element:
            self._build(sub_element, properties, current_path)

        return tree