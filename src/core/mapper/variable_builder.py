from typing import Any

import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder
from src.core.mapper.enum import SourceType
from src.core.mapper.value import ValueBuilder


class VariableBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "variable"
        self._value_builder = ValueBuilder()

    def build(
        self,
        tree: _Element,
        variable_id: str,
        source_type: SourceType,
        source_args: dict[str:Any],
    ):
        variable_tree = etree.SubElement(tree, self._tag, {"id": variable_id})
        self._value_builder.build(variable_tree, source_type, source_args)
