from src.core.element_mapper import ElementMapper
import lxml.etree as etree
from lxml.etree import _Element

from src.core.mapper import ValueBuilder

class VariableBuilder(ElementMapper):
    def __init__(self):
        super().__init__()
        self._tag = "variables"
        self._value_builder = ValueBuilder()

    def build(self, id: str, tree: _Element):
        return super().build(tree)