from lxml import etree
from lxml.etree import _Element

from src.core.element_mapper import ElementBuilder
from src.core.utils.xml_utils import create_xpath, format_result

DETAILS_IDS = ["codigo", "mensagem", "correcao"]
KEYS_TAGS = ["codigo_details", "mensagens_detail", "correcao_details"]


class DetailsBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "details"
        self._inner_tag = "message"

    def build(self, tree: _Element, response_element: _Element, targets_tags: dict):
        details = etree.SubElement(tree, self._tag)
        self._build(details, response_element, targets_tags)
        return tree

    def _build(self, tree: _Element, response_element: _Element, targets_tags: dict):
        index = 0
        for detail_id in DETAILS_IDS:
            if targets_tags and KEYS_TAGS[index] in targets_tags.keys():
                xpath_value = format_result(create_xpath(response_element, targets_tags[KEYS_TAGS[index]]))
            else:
                xpath_value = ""

            etree.SubElement(tree, self._inner_tag, {"id": detail_id, "type": "ERROR", "xpath": xpath_value})
            index += 1
