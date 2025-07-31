import lxml.etree as etree
from lxml.etree import _Element
from xmlschema import XMLSchema

from src.core.action.response.details_builder import DetailsBuilder
from src.core.action.response.parameters_builder import ParametersBuilder
from src.core.action.response.status_builder import StatusBuilder
from src.core.element_builder import ElementBuilder
from src.core.utils.constants import CONDITTIONS_MAP
from src.core.utils.xml_utils import get_element_by_message_name


class ResponseBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "response"
        self._parameters_builder = ParametersBuilder()
        self._status_builder = StatusBuilder()
        self._details_builder = DetailsBuilder()

    def build(
        self,
        tree: _Element,
        parsed_xsd: XMLSchema,
        response_tag: str,
        operation_tag: str,
        file_type: str,
        mapper_root: _Element,
        wsdl_root: _Element,
        namespaces: dict,
        wsdl_schema_root: _Element,
        targets_tags: dict,
    ):
        response = self._build(
            parsed_xsd,
            response_tag,
            operation_tag,
            file_type,
            mapper_root,
            wsdl_root,
            namespaces,
            wsdl_schema_root,
            targets_tags or [],
        )
        tree.append(response)
        return tree

    def _build(
        self,
        parsed_xsd: XMLSchema,
        response_tag: str,
        operation_tag: str,
        file_type: str,
        mapper_root: _Element,
        wsdl_root: _Element,
        namespaces: dict,
        wsdl_schema_root: _Element,
        targets_tags: dict,
    ):
        response = etree.Element(self._tag)

        body = etree.SubElement(response, "body")

        input_elem = etree.SubElement(body, "input")
        etree.SubElement(
            input_elem, "content", xpath=self._get_output_xpath(operation_tag, wsdl_root, namespaces, wsdl_schema_root)
        )

        return_tag = etree.SubElement(body, "return")

        response_element = parsed_xsd.elements.get(response_tag)

        self._status_builder.build(file_type, return_tag, CONDITTIONS_MAP, response_element, targets_tags)

        self._details_builder.build(return_tag, response_element, targets_tags)

        self._parameters_builder.build(return_tag, file_type, response_element, mapper_root, targets_tags)

        return response

    def _get_output_xpath(self, operation_tag: str, wsdl_root: _Element, namespaces: dict, wsdl_schema_root: _Element):
        operation = wsdl_root.find(
            f"./wsdl:portType/wsdl:operation[@name='{operation_tag}']",
            namespaces=namespaces,
        )
        output = operation.find("wsdl:output", namespaces=namespaces)
        output_message = output.get("message").split(":")[-1]
        output_element_name = get_element_by_message_name(output_message, wsdl_root, namespaces)
        element = wsdl_schema_root.find(
            f"./xsd:element[@name='{output_element_name}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        output_xpath = self._mount_output_xpath(element, wsdl_schema_root)

        return output_xpath

    def _mount_output_xpath(self, element, xsd):
        output_xpath = f"Envelope/Body/{element.get('name')}"
        if element.get("type") is not None:
            type = element.get("type").split(":")[-1]
            complex_type = xsd.find(
                f"./xsd:complexType[@name='{type}']", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            )
            if complex_type is not None:
                output_xpath = self._map_complex_type(complex_type, output_xpath, xsd)
        return output_xpath

    def _map_complex_type(self, complex_type, output_xpath, xsd):
        element = complex_type.find(".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"})
        output_xpath += f"/{element.get('name')}"
        if element.get("type") is not None:
            type = element.get("type").split(":")[-1]
            complex_type = xsd.find(
                f"./xsd:complexType[@name='{type}']", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
            )
            if complex_type is not None:
                output_xpath = self._map_complex_type(complex_type, output_xpath, xsd)
        return output_xpath
