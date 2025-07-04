from typing import Optional
from xmlschema.validators import XsdAttributeGroup

from src.core.element_mapper import ElementBuilder
import lxml.etree as etree

from src.core.mapper.enum import SourceType
from src.core.mapper.value import ValueBuilder

from lxml.etree import _Element

class AttributesBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "attributes"
        self._value_builder = ValueBuilder()
        self._inner_tag = "attribute"

    def build(self, property: _Element, attributes: XsdAttributeGroup):
        attrs_root = etree.SubElement(property, self._tag)
        self._build(attrs_root, attributes, property)
        return property

    def _build(self, root: _Element, attributes: XsdAttributeGroup, property: _Element):
        for attribute in attributes:
            if attribute in ("id", "Id"):
                name = f'id{property.attrib["name"]}'
                source_type = SourceType.RANDOM
                source_args = {"rangeStart" : "100000000", "rangeEnd": "999999999"}
            else:
                name = attribute
                source_type = SourceType.STATIC
                source_args = {"value" : "TODO"}
            attr = etree.SubElement(root, self._inner_tag, {"name" : name})
            self._value_builder.build(attr, source_type, source_args)
        
        return root