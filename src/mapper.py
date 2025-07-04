from typing import Optional
import xmlschema
from lxml.etree import _Element

from src.core.mapper import PropertiesBuilder
from src.core.mapper.data import JsonProperties
from src.core.mapper.mapper_builder import MapperBuilder
from src.core.utils import get_xml, export_xml_to_file

class Mapper:
    # variaveis -> ids
    # id do mapper 
    def __init__(self, root_element: str, xsd_path: str, output_file: str):
        self._mapper_builder = MapperBuilder()
        self._root_element = root_element
        self._xsd_path = xsd_path
        self._output_file = output_file
        self._tree: Optional[_Element] = None
    
    def build(self) -> _Element:
        self._tree = self._mapper_builder.build()
    

    def build_xml(self) -> str:
        return self._build_xml(self.root_element)
