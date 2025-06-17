#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from __future__ import annotations
from typing import Dict, List, Optional, Any
from lxml import etree
from dataclasses import dataclass, field


@dataclass
class XsdElement:
    """Representa um elemento do XSD."""

    name: str
    type: str = None
    is_complex: bool = False
    is_simple: bool = False
    min_occurs: int = 1
    max_occurs: int = 1
    children: List[XsdElement] = field(default_factory=list)
    attributes: List[XsdAttribute] = field(default_factory=list)
    choices: List[List[XsdElement]] = field(default_factory=list)
    path: str = ""
    parent: Optional[XsdElement] = None


@dataclass
class XsdAttribute:
    """Representa um atributo do XSD."""

    name: str
    type: str
    required: bool = False


class XsdParser:
    """Classe para analisar documentos XSD."""

    def __init__(self, xsd_path: str):
        """
        Inicializa o parser XSD.

        Args:
            xsd_path (str): Caminho para o arquivo XSD.
        """
        self.xsd_path = xsd_path
        self.base_xsd_path = self._get_base_xsd_path()
        self.root = self._get_root()
        self.namespace_map = self._get_namespaces()

        self.includes: List[XsdParser] = self._get_includes()
        
        self.simple_types: Dict[str, Dict[str, Any]] = {}
        self.complex_types: Dict[str, XsdElement] = {}

        self._process_types()

        if self.includes:
            self._resolve_includes()

        self.elements: Dict[str, XsdElement] = self._get_elements()


    def _process_types(self):
        self.complex_types = self._get_complex_types()
        self.simple_types = self._get_simple_types()

    def _resolve_includes(self):
        for include in self.includes:
            self._process_types()
            if include.includes:
                include._resolve_includes()
            self.complex_types = {**self.complex_types, **include.complex_types}
            self.simple_types  = {**self.simple_types, **include.simple_types}

    def _get_base_xsd_path(self):
        # corta o ultimo item do xpath
        base = "/".join(self.xsd_path.split("/")[0:-1])
        return base

    def _get_root(self):
        try:
            parser = etree.XMLParser(ns_clean=True, recover=True, encoding="utf-8")
            tree = etree.parse(self.xsd_path, parser)
        except Exception as e:
            raise Exception(f"Erro ao extrair raiz do XSD: {str(e)}")
        finally:
            return tree.getroot()

    def _get_namespaces(self):
        try:
            namespaces = {
                prefix: uri
                for prefix, uri in self.root.nsmap.items()
                if prefix is not None
            }
            
            if None in self.root.nsmap:
                namespaces["xsd"] = self.root.nsmap[None]
        except Exception as e:
            raise Exception(f"Erro ao extrair namespaces do XSD: {str(e)}")
        finally:
            return namespaces                                                                                                               

    def _get_includes(self) -> List[XsdParser]:
        # analisar imports e includes
        includes = []
        for include in self.root.xpath("./xsd:include", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}):
            inc_file = include.attrib["schemaLocation"]
            include_schema = f"{self.base_xsd_path}/{inc_file}"
            includes.append(XsdParser(include_schema))
        return includes 

    def _get_simple_types(self) -> Dict[str, Dict[str, Any]]:
        """Extrai todos os tipos simples definidos no XSD."""
        simple_types = {}
        for simple_type in self.root.xpath(
            "./xsd:simpleType", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            name = simple_type.get("name")
            if name:
                restrictions = simple_type.xpath(
                    "./xsd:restriction",
                    namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
                )
                if restrictions:
                    restriction = restrictions[0]
                    base_type = restriction.get("base")

                    # Coletar padrões, enumerações, etc.
                    facets = {}
                    for facet in restriction.getchildren():
                        facet_name = etree.QName(facet).localname
                        facet_value = facet.get("value")
                        if facet_name not in facets:
                            facets[facet_name] = []
                        facets[facet_name].append(facet_value)

                    simple_types[name] = {"base": base_type, "facets": facets}

        return simple_types

    def _get_complex_types(self) -> Dict[str, XsdElement]:
        """Extrai todos os tipos complexos definidos no XSD."""
        complex_types = {}
        for complex_type in self.root.xpath(
            "./xsd:complexType", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            name = complex_type.get("name")
            if name:
                element = XsdElement(name=name, is_complex=True)
                self._process_complex_type_children(complex_type, element)
                complex_types[name] = element

        return complex_types

    def _get_elements(self) -> Dict[str, XsdElement]:
        """Extrai todos os elementos definidos no XSD."""
        elements = {}
        for elem in self.root.xpath(
            "./xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            # Ignorar elementos que são filhos de tipos complexos
            if elem.getparent() is not None and etree.QName(
                elem.getparent()
            ).localname not in ["schema"]:
                continue

            name = elem.get("name")
            type_name = elem.get("type")

            if name:
                element = XsdElement(name=name, type=type_name)

                # Se tiver um tipo definido, verificar se é complexo
                if type_name and type_name in self.complex_types:
                    complex_type = self.complex_types[type_name]
                    element.is_complex = True
                    element.children = complex_type.children.copy()
                    element.attributes = complex_type.attributes.copy()
                    element.choices = complex_type.choices.copy()
                elif type_name and type_name in self.simple_types:
                    element.is_simple = True

                # Verificar se o elemento contém uma definição de tipo complexo anônimo
                complex_type_elems = elem.xpath(
                    "./xsd:complexType",
                    namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
                )
                if complex_type_elems:
                    element.is_complex = True
                    self._process_complex_type_children(complex_type_elems[0], element)

                elements[name] = element

        return elements

    def _process_complex_type_children(self, complex_type_elem, parent_element):
        """
        Processa os filhos de um tipo complexo.

        Args:
            complex_type_elem: O elemento do tipo complexo.
            parent_element: O elemento pai que receberá os filhos.
        """
        # Processar atributos
        for attr in complex_type_elem.xpath(
            "./xsd:attribute", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            name = attr.get("name")
            type_name = attr.get("type")
            required = attr.get("use") == "required"
            if name and type_name:
                parent_element.attributes.append(
                    XsdAttribute(name=name, type=type_name, required=required)
                )

        # Processar elementos filhos de sequence
        for sequence in complex_type_elem.xpath(
            "./xsd:sequence", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            for child in sequence.xpath(
                "./xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            ):
                self._process_child_element(child, parent_element)

        for choice in complex_type_elem.xpath(
            "./xsd:choice", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            choice_elements = []
            for child in choice.xpath(
                "./xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            ):
                choice_element = self._create_element_from_node(child)
                if choice_element:
                    choice_element.parent = parent_element
                    choice_elements.append(choice_element)

            if choice_elements:
                parent_element.choices.append(choice_elements)

        # Processar elementos filhos de choice
        for choice in complex_type_elem.xpath(
            "./xsd:choice", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
        ):
            choice_elements = []
            for sequence in choice.xpath(
                "./xsd:sequence", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            ):
                for child in sequence.xpath(
                    "./xsd:element",
                    namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
                ):
                    choice_element = self._create_element_from_node(child)
                    if choice_element:
                        choice_element.parent = parent_element
                        choice_elements.append(choice_element)

            if choice_elements:
                parent_element.choices.append(choice_elements)

    def _process_child_element(self, element_node, parent_element):
        """
        Processa um elemento filho.

        Args:
            element_node: O nó do elemento.
            parent_element: O elemento pai.
        """
        child_element = self._create_element_from_node(element_node)
        if child_element:
            child_element.parent = parent_element
            child_element.path = (
                f"{parent_element.path}/{child_element.name}"
                if parent_element.path
                else child_element.name
            )
            parent_element.children.append(child_element)

    def _create_element_from_node(self, element_node):
        """
        Cria um objeto XsdElement a partir de um nó de elemento.

        Args:
            element_node: O nó do elemento.

        Returns:
            XsdElement ou None se não for possível criar.
        """
        name = element_node.get("name")
        type_name = element_node.get("type")
        min_occurs = int(element_node.get("minOccurs", "1"))
        max_occurs = element_node.get("maxOccurs", "1")
        max_occurs = int(max_occurs) if max_occurs != "unbounded" else float("inf")

        if name:
            element = XsdElement(
                name=name, type=type_name, min_occurs=min_occurs, max_occurs=max_occurs
            )

            # Se tiver um tipo definido, verificar se é complexo
            if type_name and type_name in self.complex_types:
                complex_type = self.complex_types[type_name]
                element.is_complex = True
                element.children = complex_type.children.copy()
                element.attributes = complex_type.attributes.copy()
                element.choices = complex_type.choices.copy()
            elif type_name and type_name in self.simple_types:
                element.is_simple = True

            # Verificar se o elemento contém uma definição de tipo complexo anônimo
            complex_type_elems = element_node.xpath(
                "./xsd:complexType",
                namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
            )
            if complex_type_elems:
                element.is_complex = True
                self._process_complex_type_children(complex_type_elems[0], element)

            return element

        return None

    def get_root_elements(self) -> List[XsdElement]:
        """
        Retorna a lista de elementos raiz do XSD.

        Returns:
            Lista de elementos raiz.
        """
        return list(self.elements.values())

    def get_element_by_name(self, name: str) -> Optional[XsdElement]:
        """
        Retorna um elemento pelo nome.

        Args:
            name: Nome do elemento.

        Returns:
            O elemento ou None se não encontrado.
        """
        return self.elements.get(name)
