from enum import Enum

class SourceType(Enum, str):
    RANDOM = "random"
    VARIABLE = "variable"
    XML_PROPERTY = "xml_property"