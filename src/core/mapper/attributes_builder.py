import lxml.etree as etree
from lxml.etree import _Element
from xmlschema.validators import XsdAttributeGroup

from src.core.element_builder import ElementBuilder
from src.core.mapper.enum import SourceType
from src.core.mapper.value import ValueBuilder
from src.core.mapper.variable_builder import VariableBuilder


class AttributesBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "attributes"
        self._value_builder = ValueBuilder()
        self._variable_builder = VariableBuilder()
        self._inner_tag = "attribute"

    def build(self, property: _Element, attributes: XsdAttributeGroup, variables_tree: _Element):
        attrs_root = etree.SubElement(property, self._tag)
        self._build(attrs_root, attributes, property, variables_tree)
        return property

    def _build(self, root: _Element, attributes: XsdAttributeGroup, property: _Element, variables_tree: _Element):
        for attribute in attributes:
            name = attribute
            attr = etree.SubElement(root, self._inner_tag, {"name": name})
            if attribute in ("id", "Id"):
                variable_name = f"{name}{property.get('name')}"
                source_type = SourceType.RANDOM
                source_args = {"rangeStart": "100000000", "rangeEnd": "999999999"}
                self._variable_builder.build(variables_tree, variable_name, source_type, source_args)
                self._value_builder.build(attr, SourceType.VARIABLE, {"variableId": variable_name})
                continue

            source_type = SourceType.STATIC
            source_args = {"value": "TODO"}
            self._value_builder.build(attr, source_type, source_args)

        return root
