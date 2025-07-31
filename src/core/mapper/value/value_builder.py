from typing import Any

import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_builder import ElementBuilder
from src.core.mapper.enum import SourceType
from src.core.mapper.value import SourceBuilder


class ValueBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "value"
        self._source_builder = SourceBuilder()

    def build(self, tree: _Element, source_type: SourceType, source_args: dict[str:Any]):
        value_element = etree.SubElement(tree, self._tag)
        self._source_builder.build(value_element, source_args, source_type)
        return tree

    def _build_operations(self, tree: _Element) -> etree:
        return tree
