from typing import Any

import lxml.etree as etree
from lxml.etree import _Element

from src.core import ElementBuilder
from src.core.mapper.data import JsonProperties
from src.core.mapper.enum import SourceType


class SourceBuilder(ElementBuilder):
    def __init__(self):
        super().__init__()
        self._tag = "sources"
        self._props = JsonProperties()
        self._source_keys = {
            SourceType.XML_PROPERTY: ["xpath"],
            SourceType.RANDOM: ["rangeStart", "rangeEnd"],
            SourceType.PARAMETER: ["name"],
            SourceType.STATIC: ["value"],
            SourceType.VARIABLE: ["variableId"],
        }

    def build(self, parent: _Element, source_args: dict[str:Any], source_type: SourceType) -> _Element:
        sources_element = etree.SubElement(parent, self._tag)
        source_args = self._treat_args(source_args, source_type)
        etree.SubElement(sources_element, source_type.value, **source_args)

        return parent

    def _validate_keys(self, required: list[str], source_args: dict) -> None:
        missing = [key for key in required if key not in source_args]
        if missing:
            expected = ", ".join(f'"{key}"' for key in required)
            received = ", ".join(f'"{key}"' for key in source_args.keys())
            raise ValueError(f"Argumentos inválidos: esperado {expected}, recebido: {received}")

    def _treat_args(self, source_args: dict, source_type: SourceType) -> dict:
        required = self._source_keys.get(source_type)

        if not required:
            raise ValueError(f"Tipo de source não é válido: {source_type.value}")

        self._validate_keys(required, source_args)

        if source_type == SourceType.XML_PROPERTY:
            value = source_args["xpath"]
            return {"xpath": self._props.get(value)}

        return source_args
