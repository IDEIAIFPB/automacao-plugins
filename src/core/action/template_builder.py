import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder


class TemplateBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "template"

    def build(self, tree: _Element, operation_tag: str, wsdl: _Element, final_envelope_tag: str = None):
        template = etree.SubElement(tree, self._tag)
        self._build(template, operation_tag, wsdl)
        return tree

    def _build(self, tree: _Element, operation_tag: str, wsdl: _Element):
        return tree

    def _get_envelope():
        pass
