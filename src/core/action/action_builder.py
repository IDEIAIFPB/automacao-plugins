import lxml.etree as etree
import xmlschema
from lxml.etree import _Element

from src.core.action.request.request_builder import RequestBuilder
from src.core.action.response.response_builder import ResponseBuilder
from src.core.element_builder import ElementBuilder


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
        xsd_path: str,
        response_tag: str,
        mapper_tree: _Element,
        targets_tags: dict,
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
            xml_root,
            signatures,
            operation_tag,
            wsdl_path,
            final_envelope_tag,
            file_type,
            xsd_path,
            response_tag,
            mapper_tree,
            targets_tags,
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
        xsd_path: str,
        response_tag: str,
        mapper_tree: _Element,
        targets_tags: dict,
    ):
        wsdl_tree = etree.parse(wsdl_path)
        wsdl_root = wsdl_tree.getroot()
        namespaces = wsdl_root.nsmap
        wsdl_schema_root = self._parse_wsdl_schema(wsdl_root, namespaces)
        mapper_root = mapper_tree.find(".//property")

        self._request_builder.build(
            xml_root, signatures, operation_tag, final_envelope_tag, file_type, wsdl_root, namespaces, wsdl_schema_root
        )
        self._response_builder.build(
            xml_root,
            xmlschema.XMLSchema(xsd_path),
            response_tag,
            operation_tag,
            file_type,
            mapper_root,
            wsdl_root,
            namespaces,
            wsdl_schema_root,
            targets_tags,
        )

    def _parse_wsdl_schema(self, tree: _Element, namespaces: dict):
        schema = tree.find("./wsdl:types/xsd:schema", namespaces=namespaces)

        if schema is None:
            raise ValueError("Schema não encontrado")

        xsd_importado = schema.find("./xsd:import", namespaces=namespaces)
        initial_xsd = xsd_importado.get("schemaLocation") if xsd_importado is not None else None

        if initial_xsd is None:
            return schema

        wsdl_schema = etree.parse(initial_xsd)
        return wsdl_schema.getroot()
