import lxml.etree as etree
from lxml.etree import _Element

from src.core.action.enum import FileType
from src.core.element_mapper import ElementBuilder
from src.core.utils.constants import DEFAULT_PARAMS, PARAMETERS_EMISSAO
from src.core.utils.xml_utils import create_xpath, format_result


class ParametersBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "parameters"
        self._inner_tag = "parameter"

    def build(
        self,
        tree: _Element,
        file_type: str,
        response_element: _Element,
        mapper_root: _Element,
        targets_tags: dict = None,
    ):
        parameters_tree = etree.SubElement(tree, self._tag)
        self._build(parameters_tree, file_type, response_element, mapper_root, targets_tags)
        return tree

    def _build(
        self,
        tree: _Element,
        file_type: str,
        response_element: _Element,
        mapper_root: _Element,
        targets_tags: dict = None,
    ):
        if file_type == FileType.CANCELAMENTO:
            return tree

        for key, value in DEFAULT_PARAMS.items():
            if value[1][0] != "/":
                xpath_value = (
                    format_result(create_xpath(response_element, targets_tags[value[1]]))
                    if targets_tags and targets_tags[value[1]]
                    else ""
                )
            etree.SubElement(
                tree,
                self._inner_tag,
                attrib={
                    "id": key,
                    "origin": value[0],
                    "xpath": value[1] if value[1][0] == "/" else xpath_value,
                },
            )

        if file_type == FileType.EMISSAO:
            for key, value in PARAMETERS_EMISSAO.items():
                if value[1][0] != "/":
                    if key == "AliquotaAtividade":
                        xpath_value = self._create_xpath_by_mapper(mapper_root, targets_tags[value[1]])
                    else:
                        xpath_value = (
                            format_result(create_xpath(response_element, targets_tags[value[1]]))
                            if targets_tags and targets_tags[value[1]]
                            else ""
                        )
                etree.SubElement(
                    tree,
                    self._inner_tag,
                    attrib={
                        "id": key,
                        "origin": value[0],
                        "xpath": xpath_value if value[1][0] != "/" and xpath_value else value[1],
                    },
                )

        return tree

    def _create_xpath_by_mapper(self, element: _Element, target_element: str, current_path=""):
        local_name = element.get("name")

        current_path += f"/{local_name}"
        if local_name == target_element:
            return current_path

        properties = element.findall(".//property")
        for property in properties:
            result = self._create_xpath_by_mapper(property, target_element, current_path)
            if result:
                return result

        return None
