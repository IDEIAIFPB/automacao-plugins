import lxml.etree as etree
from lxml.etree import _Element
from xmlschema.validators import XsdElement

from src.core.element_builder import ElementBuilder


class SignaturesBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "signatures"
        self._inner_tag = "signature"

    def build(self, tree: _Element, signatures: list):
        signatures_element = etree.SubElement(tree, self._tag)
        self._build(signatures_element, signatures)
        return tree

    def _build(self, tree: _Element, signatures: XsdElement):
        for signature in signatures:
            etree.SubElement(
                tree,
                self._inner_tag,
                signature,
                attribute="Id",
            )
        return tree
