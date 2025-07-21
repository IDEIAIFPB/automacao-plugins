from lxml import etree
from lxml.etree import _Element

from src.core.action.enum import FileType
from src.core.action.response.conditition_builder import ConditionBuilder
from src.core.element_mapper import ElementBuilder


class StatusBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "status"
        self._cancelled = "cancelled"
        self._conflict = "conflict"
        self._rejected = "rejected"
        self._accepted = "accepted"
        self._condition_builder = ConditionBuilder()

    def build(
        self,
        file_type: str,
        tree: _Element,
        conditions_map: dict,
        response_element: _Element,
        targets_tags: dict,
    ):
        status_tree = etree.SubElement(tree, self._tag)
        self._build(file_type, status_tree, conditions_map, response_element, targets_tags)
        return tree

    def _build(
        self,
        file_type: str,
        tree: _Element,
        conditions_map: dict,
        response_element: _Element,
        targets_tags: dict,
    ):
        type_actions = {
            FileType.EMISSAO.value: [self._accepted, self._conflict, self._rejected],
            FileType.CANCELAMENTO.value: [self._cancelled, self._rejected],
            FileType.CONSULTA.value: [self._conflict, self._rejected],
        }

        status_types = type_actions.get(file_type, [])
        for status_type in status_types:
            self._inner_status(tree, conditions_map[file_type], response_element, targets_tags, status_type)

        etree.SubElement(
            tree,
            "default",
            attrib={
                "status": "UNKNOWN",
            },
        )

        return tree

    def _inner_status(
        self, tree: _Element, conditions_map: dict, response_element: _Element, targets_tags: dict, status_type: str
    ):
        innner_status = etree.SubElement(tree, status_type)
        return self._condition_builder.build(
            innner_status, conditions_map[status_type], status_type, response_element, targets_tags
        )
