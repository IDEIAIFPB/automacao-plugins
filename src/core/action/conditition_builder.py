import lxml.etree as etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder
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
        response_tag: _Element,
        targets_tags: dict,
        target_key: str = "xpath",
    ):
        conditions_tree = etree.SubElement(tree, self._tag)
        self._build(conditions_tree, conditions_map, response_tag, targets_tags, target_key)
        return tree

    def _build(
        self,
        tree: _Element,
        conditions_map: dict,
        response_tag: _Element,
        targets_tags: dict,
        target_key: str = "xpath",
    ):
        for condition in conditions_map.get("conditions", []):
            comparison = condition.get("comparison") or ""

            target_tag_key = condition.get("target_tag_key") or ""

            if target_tag_key:
                xpath = format_result(create_xpath(response_tag, targets_tags.get(target_tag_key, target_tag_key)))
            else:
                xpath = condition.get("xpath")
            # xpath_from_condition = condition.get(target_key) or ""
            # if targets_tags and xpath_from_condition:
            #     xpath = format_result(
            #         create_xpath(response_tag, targets_tags.get(xpath_from_condition, xpath_from_condition))
            #     )
            # else:
            #     xpath = xpath_from_condition

            etree.SubElement(
                tree,
                self._inner_tag,
                attrib={
                    "comparison": comparison,
                    "xpath": xpath or "",
                },
            )
        return tree
