#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from lxml import etree
from src.xsd_parser import XsdParser, XsdElement


class MapperGenerator:
    """Classe para gerar documentos de mapeamento XML a partir de um XSD."""

    def __init__(
        self,
        xsd_parser: XsdParser,
        template_xpath_prefix: str = "/SynchroId/PedidoEnvioRPS/RPS",
        properties_file: str = None,
    ):
        """
        Inicializa o gerador de mapper.

        Args:
            xsd_parser: Parser XSD já inicializado.
            template_xpath_prefix: Prefixo para os caminhos XPath no documento de mapeamento.
            properties_file: Caminho para o arquivo properties.json com mapeamentos de XPath.
        """
        self.xsd_parser = xsd_parser
        self.template_xpath_prefix = template_xpath_prefix
        self.id_variables = {}
        self.properties_map = {}

        # Carregar mapeamentos de XPath de properties.json, se disponível
        if properties_file:
            try:
                import json

                with open(properties_file, "r", encoding="utf-8") as f:
                    self.properties_map = json.load(f)
            except Exception as e:
                print(
                    f"Aviso: Não foi possível carregar o arquivo properties.json: {str(e)}"
                )
                self.properties_map = {}

    def generate_mapper(
        self, root_element_name: str, mapper_id: str = "auto-generated"
    ) -> etree._Element:
        """
        Gera um documento de mapeamento XML.

        Args:
            root_element_name: Nome do elemento raiz para iniciar o mapeamento.
            mapper_id: Identificador para o documento de mapeamento.

        Returns:
            Elemento XML do documento de mapeamento.
        """
        root_element = self.xsd_parser.get_element_by_name(root_element_name)

        if not root_element:
            raise ValueError(
                f"Elemento raiz '{root_element_name}' não encontrado no XSD."
            )

        # Limpar variáveis de ID antes de cada geração
        self.id_variables = {}

        # Criar a raiz do documento de mapeamento com namespaces definidos corretamente
        nsmap = {
            "xsi": "http://www.w3.org/2001/XMLSchema-instance",
        }
        mapper_root = etree.Element("document-mapper", nsmap=nsmap)
        mapper_root.set("id", mapper_id)
        mapper_root.set(
            "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation",
            "../../../schemas/document-mapping.xsd",
        )

        # Realizar um pré-processamento para identificar todos os atributos "Id"
        self._collect_id_attributes(root_element)

        # Adicionar seção de variáveis, se houver IDs coletados
        if self.id_variables:
            variables = etree.SubElement(mapper_root, "variables")
            for var_name, element_name in self.id_variables.items():
                variable = etree.SubElement(variables, "variable")
                variable.set("id", var_name)
                value = etree.SubElement(variable, "value")
                sources = etree.SubElement(value, "sources")
                random = etree.SubElement(sources, "random")
                random.set("rangeStart", "100000000")
                random.set("rangeEnd", "999999999")

        # Criar o nó de propriedades
        properties = etree.SubElement(mapper_root, "properties")

        # Adicionar propriedades mapeadas a partir do elemento raiz
        self._add_property_for_element(
            properties, root_element, root_element_name, "", root_element_name
        )

        return mapper_root

    def _collect_id_attributes(
        self, element: XsdElement, element_path: str = "", parent_name: str = ""
    ):
        """
        Coleta todos os atributos 'Id' em um elemento e seus filhos, recursivamente.

        Args:
            element: O elemento XSD para examinar.
            element_path: O caminho do elemento atual.
            parent_name: Nome do elemento pai (usado para criar nomes de variáveis).
        """
        element_name = parent_name if not element_path else element.name

        # Verificar atributos neste elemento
        for attr in element.attributes:
            if attr.name in ("Id", "id"):
                # Criar um nome de variável baseado no nome do elemento
                var_name = f"id{element_name.capitalize()}"
                self.id_variables[var_name] = element_name

        # Se o elemento for complexo, examinar seus filhos
        if element.is_complex:
            for child in element.children:
                child_path = (
                    f"{element_path}/{child.name}" if element_path else child.name
                )
                self._collect_id_attributes(child, child_path, element_name)

            # Examinar elementos em choices também
            for choice_group in element.choices:
                for choice_element in choice_group:
                    choice_path = (
                        f"{element_path}/{choice_element.name}"
                        if element_path
                        else choice_element.name
                    )
                    self._collect_id_attributes(
                        choice_element, choice_path, element_name
                    )

    def _add_property_for_element(
        self,
        parent_node: etree._Element,
        element: XsdElement,
        property_name: str,
        path_prefix: str = "",
        root_element_name: str = "",
    ):
        """
        Adiciona uma propriedade de mapeamento para um elemento.

        Args:
            parent_node: O nó pai onde adicionar a propriedade.
            element: O elemento XSD para mapear.
            property_name: O nome da propriedade no mapeamento.
            path_prefix: O prefixo do caminho para elementos filhos.
            root_element_name: Nome do elemento raiz do mapeamento.
        """
        property_node = etree.SubElement(parent_node, "property")
        property_node.set("name", property_name)

        # Se o elemento tiver atributos, adicionar um nó attributes
        if element.attributes:
            attributes_node = etree.SubElement(property_node, "attributes")

            # Adicionar cada atributo do elemento
            for attr in element.attributes:
                attribute_node = etree.SubElement(attributes_node, "attribute")
                attribute_node.set("name", attr.name)

                # Adicionar valor do atributo
                value_node = etree.SubElement(attribute_node, "value")
                sources_node = etree.SubElement(value_node, "sources")

                # Para atributos "Id", usar a variável criada em vez de xpath
                if attr.name in ("Id", "id") and self.id_variables:
                    # Encontrar a variável para este elemento
                    var_name = f"id{element.name.capitalize()}"
                    if var_name in self.id_variables:
                        # Usar a variável id
                        variable_node = etree.SubElement(sources_node, "variable")
                        variable_node.set("variableId", var_name)
                    else:
                        # Fallback para xpath se não tiver variável
                        xml_property = etree.SubElement(sources_node, "xmlProperty")
                        attr_xpath = (
                            f"{self.template_xpath_prefix}/{path_prefix}/@{attr.name}"
                            if path_prefix
                            else f"{self.template_xpath_prefix}/@{attr.name}"
                        )
                        xml_property.set("xpath", attr_xpath)
                else:
                    # Para outros atributos, inserir "TODO" como texto
                    sources_node.text = "TODO"

        # Se o elemento for complexo, adicionar propriedades para seus filhos
        if element.is_complex:
            properties_node = etree.SubElement(property_node, "properties")

            # Adicionar propriedades para cada filho
            for child in element.children:
                child_path = (
                    f"{path_prefix}/{child.name}" if path_prefix else child.name
                )
                self._add_property_for_element(
                    properties_node,
                    child,
                    child.name,
                    child_path,
                    root_element_name or property_name,
                )

            # Processar choices também
            for choice_group in element.choices:
                for choice_element in choice_group:
                    choice_path = (
                        f"{path_prefix}/{choice_element.name}"
                        if path_prefix
                        else choice_element.name
                    )
                    self._add_property_for_element(
                        properties_node,
                        choice_element,
                        choice_element.name,
                        choice_path,
                        root_element_name or property_name,
                    )
        else:
            # Elemento simples - criar nó de valor
            value_node = etree.SubElement(property_node, "value")
            sources_node = etree.SubElement(value_node, "sources")

            # Construir chave para buscar no mapeamento properties.json
            properties_key = (
                f"{root_element_name}/{path_prefix}"
                if path_prefix
                else root_element_name
            )

            # Verificar se existe um mapeamento para este elemento no properties.json
            if properties_key in self.properties_map:
                # Usar o xpath definido no properties.json
                xml_property = etree.SubElement(sources_node, "xmlProperty")
                xml_property.set("xpath", self.properties_map[properties_key])
            else:
                # Se não encontrar o caminho no properties.json, adicionar TODO
                sources_node.text = "TODO - Caminho não encontrado no properties.json"

    def generate_mapper_xml(
        self, root_element_name: str, mapper_id: str = "auto-generated"
    ) -> str:
        """
        Gera o XML do documento de mapeamento como string.

        Args:
            root_element_name: Nome do elemento raiz para iniciar o mapeamento.
            mapper_id: Identificador para o documento de mapeamento.

        Returns:
            String XML do documento de mapeamento.
        """
        mapper_root = self.generate_mapper(root_element_name, mapper_id)

        # Converter o elemento XML para string formatada
        return etree.tostring(
            mapper_root, pretty_print=True, encoding="utf-8", xml_declaration=True
        ).decode("utf-8")

    def save_mapper_to_file(
        self,
        output_path: str,
        root_element_name: str,
        mapper_id: str = "auto-generated",
    ) -> None:
        """
        Salva o documento de mapeamento em um arquivo.

        Args:
            output_path: Caminho para salvar o arquivo XML.
            root_element_name: Nome do elemento raiz para iniciar o mapeamento.
            mapper_id: Identificador para o documento de mapeamento.
        """
        xml_content = self.generate_mapper_xml(root_element_name, mapper_id)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(xml_content)
