from lxml import etree
from lxml.etree import _Element
from xmlschema import XMLSchema
from xmlschema.validators import XsdElement

from src.core.action.details_builder import DetailsBuilder
from src.core.action.parameters_builder import ParametersBuilder
from src.core.action.status_builder import StatusBuilder
from src.core.element_mapper import ElementBuilder


class ResponseBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "response"
        self._parameters_builder = ParametersBuilder()
        self._status_builder = StatusBuilder()
        self._details_builder = DetailsBuilder()

    def build(self, tree: _Element, parsed_xsd: XMLSchema, response_tag: str, plugin_id: str):
        response = etree.SubElement(tree, self._tag)
        self._build(response, plugin_id, parsed_xsd, response_tag)
        return response

    def _build(self, xml_root: _Element, xsd_element: XsdElement):
        pass
