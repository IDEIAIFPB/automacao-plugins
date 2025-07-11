from lxml import etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder

from .conditition_builder import ConditionBuilder


class StatusBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "status"
        self._cancel = "cancelled"
        self._conflict = "conflict"
        self._rejected = "rejected"
        self._accepted = "accepted"
        self._condition_builder = ConditionBuilder()

    def build(self, file_type: str, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None):
        status_tree = etree.SubElement(tree, self._tag)
        self._build(file_type, status_tree, _dict, response_element, targets_tags)
        return tree

    def _build(
        self, file_type: str, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None
    ):
        file_type = file_type.upper()

        type_actions = {
            "EMISSAO": [self.accept, self.conflict, self.reject],
            "CANCELAMENTO": [self.cancel, self.reject],
            "CONSULTA": [self.conflict, self.reject],
        }

        actions = type_actions.get(file_type, [])
        for action in actions:
            action(tree, _dict, response_element, targets_tags)

        etree.SubElement(
            tree,
            "default",
            attrib={
                "status": "unknown",
            },
        )

        return tree

    def conflict(self, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None):
        conflict = etree.SubElement(tree, "conflict")
        return self._condition_builder.build(conflict, _dict, response_element, targets_tags, "xpath")

    def accept(self, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None):
        accepted = etree.SubElement(tree, "accepted")
        return self._condition_builder.build(accepted, _dict, response_element, targets_tags, "xpath_key")

    def reject(self, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None):
        rejected = etree.SubElement(tree, "rejected")
        return self._condition_builder.build(rejected, _dict, response_element, targets_tags, "xpath_key")

    def cancel(self, tree: _Element, _dict: dict, response_element: _Element, targets_tags: dict = None):
        cancelled = etree.SubElement(tree, "cancelled")
        return self._condition_builder.build(cancelled, _dict, response_element, targets_tags, "xpath_key")
