from src.core.element_mapper import ElementMapper
from lxml import etree

class ValueBuilder(ElementMapper):
    def __init__(self, tree = ...):
        super().__init__(tree)
    
    def build(self) -> etree:
        return super().build()
    
    def build_xml(self):
        return super().build_xml()

    def _build_source(): pass