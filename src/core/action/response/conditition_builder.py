import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_builder import ElementBuilder
from src.core.utils.xml_utils import create_xpath, format_result


class ConditionBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "conditions"
        self._inner_tag = "condition"

    def build(
        self,
        tree: _Element,
        conditions_map: dict,
        status_type: str,
        response_tag: _Element,
        targets_tags: dict,
    ):
        conditions_tree = etree.SubElement(tree, self._tag)
        if status_type == "conflict":
            conditions_tree.attrib["type"] = "OR"
        self._build(conditions_tree, conditions_map, response_tag, targets_tags)
        return tree

    def _build(
        self,
        tree: _Element,
        conditions_map: dict,
        response_tag: _Element,
        targets_tags: dict,
    ):
        for condition in conditions_map.get("conditions", []):
            target_tag_key = None
            if "target_tag_key" in condition.keys():
                target_tag_key = condition.pop("target_tag_key") or ""

            if target_tag_key and "xpath" not in condition.keys():
                xpath = format_result(create_xpath(response_tag, targets_tags.get(target_tag_key, target_tag_key)))
                if not xpath:
                    continue
                condition["xpath"] = xpath

            etree.SubElement(
                tree,
                self._inner_tag,
                condition,
            )
        return tree
