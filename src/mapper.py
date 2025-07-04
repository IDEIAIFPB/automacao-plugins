from typing import Optional
import xmlschema
from lxml.etree import _Element

from src.core.mapper import PropertiesBuilder
from src.core.mapper.data import JsonProperties
from src.core.mapper.mapper_builder import MapperBuilder
from src.core.utils.xml_utils import get_xml, export_xml_to_file

class Mapper:
    def __init__(self, root_element: str, plugin_id: str, xsd_path: str, output_file: str):
        self._mapper_builder = MapperBuilder()
        self._root_element = root_element
        self._schema = xmlschema.XMLSchema(xsd_path)
        self._output_file = output_file
        self._plugin_id = plugin_id
    
    def build_to_file(self, path: str) -> tuple[_Element, str]:
        tree = self.build()
        xml = self.build_xml()
        export_xml_to_file(xml, path)

        return tree, xml

    def build(self) -> _Element:
        xsd_element = self._schema.elements.get(self._root_element)
        
        if xsd_element is None:
            raise ValueError(f"Elemento '{self._root_element}' não achado no schema.")
        
        tree = self._mapper_builder.build(
            self._plugin_id,
            xsd_element
        )

        return tree

    def build_xml(self, tree: _Element) -> str:
        return get_xml(tree)
    
    def export_xml_to_file(self, xml: str, path: str):
        export_xml_to_file(xml, path)
