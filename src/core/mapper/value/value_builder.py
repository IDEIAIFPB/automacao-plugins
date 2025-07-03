from typing import Any
from xmlschema.validators import XsdElement
from src.core.element_mapper import ElementMapper
from lxml import etree
from src.core.mapper.enum import SourceType  

from src.core.mapper.data.properties_loader import JsonProperties
from src.core.mapper.value import SourceBuilder

class ValueBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._tag = "value"
        self._source_builder = SourceBuilder()
    
    def build(self, tree: etree._Element, source_type: SourceType, source_args: dict[str: Any]):
        value_element = etree.SubElement(tree, self._tag)
        self._source_builder.build(value_element, source_args, source_type)
        return tree

    def _build_operations(self, tree: etree._Element) -> etree: return tree