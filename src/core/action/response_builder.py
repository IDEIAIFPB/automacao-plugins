import lxml.etree as etree
from lxml.etree import _Element
from xmlschema import XMLSchema

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

    def build(self, tree: _Element, parsed_xsd: XMLSchema, response_tag: str, plugin_id: str, targets_element: list):
        response = self._build(parsed_xsd, response_tag, plugin_id.split("-")[0], targets_element or [])
        tree.append(response)
        return tree

    def _build(self, parsed_xsd: XMLSchema, response_tag: str, file_type: str, targets_element: list):
        response = etree.Element(self._tag)

        body = etree.SubElement(response, "body")

        input_elem = etree.SubElement(body, "input")
        etree.SubElement(input_elem, "content", xpath=self._get_main_xpath(parsed_xsd, response_tag))

        status = self._status_builder.build(parsed_xsd, file_type, response_tag, targets_element)
        body.append(status)

        details = self._details_builder.build(parsed_xsd, file_type, response_tag, targets_element)
        body.append(details)

        parameters = self._parameters_builder.build(file_type, response_tag, targets_element)
        body.append(parameters)

        return response

    def _get_main_xpath(self, response_tag: str):
        return f"/Envelope/Body/{response_tag}"
