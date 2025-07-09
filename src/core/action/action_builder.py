import lxml.etree as etree
from lxml.etree import _Element
from xmlschema import XMLSchema

from src.core.action.request_builder import RequestBuilder
from src.core.action.response_builder import ResponseBuilder
from src.core.element_mapper import ElementBuilder


class ActionBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "document-action"
        self._request_builder = RequestBuilder()
        self._response_builder = ResponseBuilder()

    def build(
        self,
        plugin_id: str,
        signatures: list,
        operation_tag: str,
        wsdl_path: str,
        final_envelope_tag: str,
        parsed_xsd: XMLSchema,
        response_tag: str,
    ) -> _Element:
        xml_root = etree.Element(
            self._tag,
            {
                "id": plugin_id,
                "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation": "../../../schemas/document-action.xsd",
            },
            nsmap={"xsi": "http://www.w3.org/2001/XMLSchema-instance"},
        )
        file_type = plugin_id.split("-")[0]
        self._build(
            xml_root, signatures, operation_tag, wsdl_path, final_envelope_tag, file_type, parsed_xsd, response_tag
        )
        return xml_root

    def _build(
        self,
        xml_root: _Element,
        signatures: list,
        operation_tag: str,
        wsdl_path: str,
        final_envelope_tag: str,
        file_type: str,
        parsed_xsd: XMLSchema,
        response_tag: str,
    ):
        self._request_builder.build(xml_root, signatures, operation_tag, wsdl_path, final_envelope_tag, file_type)
        self._response_builder.build(xml_root, parsed_xsd, response_tag, file_type)
