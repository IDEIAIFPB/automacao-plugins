from lxml import etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder
from src.core.utils.constants import DETAILS_IDS, KEYS_TAGS
from src.core.utils.xml_utils import create_xpath, format_result


class DetailsBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "details"
        self._inner_tag = "message"

    def build(self, tree: _Element, response_element: _Element, targets_tags: dict):
        details = etree.SubElement(tree, self._tag, {"optional": "false"})
        self._build(details, response_element, targets_tags)
        return tree

    def _build(self, tree: _Element, response_element: _Element, targets_tags: dict):
        for index, (detail_id) in enumerate(DETAILS_IDS):
            if targets_tags and KEYS_TAGS[index] in targets_tags.keys():
                xpath_value = format_result(create_xpath(response_element, targets_tags[KEYS_TAGS[index]]))
                if not xpath_value:
                    continue

                etree.SubElement(tree, self._inner_tag, {"id": detail_id, "type": "ERROR", "xpath": xpath_value})
