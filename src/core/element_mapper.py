from typing import Optional
import lxml.etree as etree
from lxml.etree import _Element


class ElementBuilder:
    def __init__(self):
        self._tree = None
        self._tag = str()
        self._inner_tag: Optional[str] = None

    def build(self, tree: _Element) -> etree:
        raise NotImplementedError
