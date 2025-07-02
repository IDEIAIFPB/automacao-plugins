import json
import xmlschema
from xmlschema.validators import XsdElement, XsdGroup, XsdAttribute
import lxml.etree as etree

from src.core.mapper import PropertiesBuilder


class Mapper:
    # variaveis -> ids
    # id do mapper 
    def __init__(self, root_element: str, xsd_path: str, properties: str, output_file: str):
        self.props = json.load(open(properties, 'r'))
        self.schema = xmlschema.XMLSchema(xsd_path)
        self.root_element = (self.schema.elements.get(root_element)) 
        self.arquivo = open(output_file, "w")

    def _indent(self, spaces: int = 4, offset: int = 0) -> str:
        return f"{' ' * (spaces + offset)}"

    def _build_xpath(self, full_path: str) -> str:
        return self.props.get(full_path, "TODO")

    def _build_simple_types(self, spaces: int, xpath: str): 
        spaces += 4
        self.arquivo.write(f'{self._indent(spaces)}<value>\n')
        self.arquivo.write(f'{self._indent(spaces, 4)}<sources>\n')
        self.arquivo.write(f'{self._indent(spaces, 8)}<xmlProperty xpath="{xpath}"/>\n') 
        self.arquivo.write(f'{self._indent(spaces, 4)}</sources>\n')
        self.arquivo.write(f'{self._indent(spaces)}</value>\n')
        spaces -= 4
        self.arquivo.write(f'{self._indent(spaces)}</property>\n')

    def build_xml(self):
        return self._build_xml(self.root_element)

    def _build_xml(self, element: XsdElement, spaces: int = 0, current_path=""):
        if not isinstance(element, XsdElement):
            print(f"Elemento desconhecido: {type(element)}")

        if isinstance(element, XsdGroup):
            # Trata sequence, choice, all como grupos
            for sub_element in element:
                self._build_xml(sub_element, spaces, current_path)

        spaces += 4

        # Trata elements nomeados
        name = element.name.split('}')[-1]  # remove namespace

        if name == "Signature":
            return

        self.arquivo.write(f'{self._indent(spaces)}<property name="{name}">\n')
        tipo = element.type

        full_path = f"{current_path}/{name}" if current_path else name

        if hasattr(tipo, 'content') and tipo.content is not None:
            content = tipo.content
            if content.model not in ('sequence', 'choice', 'all'):
                return

            spaces += 4
            self.arquivo.write(f'{self._indent(spaces)}<properties>\n')
            for sub in content:
                self._build_xml(sub, spaces, full_path)
            self.arquivo.write(f'{self._indent(spaces)}</properties>\n')
            spaces -= 4
            self.arquivo.write(f'{self._indent(spaces)}</property>\n')
            return
        
        self._build_simple_types(spaces, self._build_xpath(full_path))
