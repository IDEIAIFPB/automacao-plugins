import lxml.etree as etree
from lxml.etree import _Element
from xmlschema.validators import XsdAttributeGroup

from src.core.element_builder import ElementBuilder
from src.core.mapper.enum import SourceType
from src.core.mapper.value import ValueBuilder


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
        for attribute in attributes.iter_components():
            if isinstance(attribute, XsdAttributeGroup):
                continue
            name = attribute.name
            if name in ("id", "Id"):
                source_type = SourceType.RANDOM
                source_args = {"rangeStart": "100000000", "rangeEnd": "999999999"}
            else:
                source_type = SourceType.STATIC
                source_args = {"value": "TODO" if not attribute.default else attribute.default}
            attr = etree.SubElement(root, self._inner_tag, {"name": name})
            self._value_builder.build(attr, source_type, source_args)

        return root
