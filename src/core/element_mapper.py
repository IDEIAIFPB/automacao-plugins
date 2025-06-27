import lxml.etree as etree
from abc import ABCMeta
class ElementMapper():
    def __init__(self, tree: etree = etree):
        self._tree = tree
    
    def build(self) -> etree: 
        raise NotImplementedError

    def build_xml(self) -> str:
        raise NotImplementedError
