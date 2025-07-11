import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder
from src.core.utils.xml_utils import create_xpath, format_result


class ConditionBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "conditions"
        self._inner_tag = "condition"

    def build(self, tree: _Element, _dict: dict, response_tag: _Element, targets_tags: dict, xpath_key: str = "xpath"):
        conditions_tree = etree.SubElement(tree, self._tag)
        self._build(conditions_tree, _dict, response_tag, targets_tags, xpath_key)
        return tree

    def _build(self, tree: _Element, _dict: dict, response_tag: _Element, targets_tags: dict, xpath_key: str = "xpath"):
        for condition in _dict.get("conditions", []):
            comparison = condition.get("comparison") or ""

            xpath_from_condition = condition.get(xpath_key) or ""
            if targets_tags and xpath_from_condition:
                xpath = format_result(
                    create_xpath(response_tag, targets_tags.get(xpath_from_condition, xpath_from_condition))
                )
            else:
                xpath = xpath_from_condition

            etree.SubElement(
                tree,
                self._inner_tag,
                attrib={
                    "comparison": comparison,
                    "xpath": xpath or "",
                },
            )
        return tree
