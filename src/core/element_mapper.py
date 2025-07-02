from typing import Optional
import lxml.etree as etree

class ElementMapper():
    def __init__(self):
        self._tree = None
        self._tag = str()
    
    def build(self, tree: etree._Element) -> etree: 
        raise NotImplementedError