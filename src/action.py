from lxml.etree import _Element
from xmlschema import XMLSchema

from src.core.action.action_builder import ActionBuilder
from src.core.utils.xml_utils import export_xml_to_file, get_xml


class Action:
    def __init__(
        self,
        operation_tag: str,
        response_tag: str,
        wsdl_path: str,
        output_file: str,
        signatures: list,
        plugin_id: str,
        parsed_xsd: XMLSchema,
    ):
        self._action_builder = ActionBuilder()
        self._operation_tag = operation_tag
        self._wsdl_path = wsdl_path
        self._output_file = output_file
        self._response_tag = response_tag
        self._plugin_id = plugin_id
        self._signatures = signatures
        self._parsed_xsd = parsed_xsd

    def build_to_file(self, path: str) -> tuple[_Element, str]:
        tree = self.build()
        xml = self.build_xml()
        export_xml_to_file(xml, path)

        return tree, xml

    def build(self) -> _Element:
        tree = self._action_builder.build(
            self._plugin_id,
            self._signatures,
            self._operation_tag,
            self._wsdl_path,
            self._parsed_xsd,
            self._response_tag,
        )

        return tree

    def build_xml(self, tree: _Element) -> str:
        return get_xml(tree)

    def export_xml_to_file(self, xml: str, path: str):
        export_xml_to_file(xml, path)
