from lxml import etree
from lxml.etree import _Element

from src.core.action.request import TemplateBuilder
from src.core.element_mapper import ElementBuilder


class ContentBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "content"
        self._template_builder = TemplateBuilder()

    def build(
        self,
        tree: _Element,
        wsdl_root: _Element,
        binding_operation: _Element,
        final_envelope_tag: str,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        content = etree.SubElement(tree, self._tag)
        self._build(content, wsdl_root, binding_operation, final_envelope_tag, namespaces, wsdl_schema_root)

    def _build(
        self,
        tree: _Element,
        wsdl_root: _Element,
        binding_operation: _Element,
        final_envelope_tag: str,
        namespaces: dict,
        wsdl_schema_root: _Element,
    ):
        self._template_builder.build(
            tree, wsdl_root, binding_operation, final_envelope_tag, namespaces, wsdl_schema_root
        )
