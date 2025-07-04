from enum import Enum


class SourceType(Enum):
    RANDOM = "random"
    VARIABLE = "variable"
    XML_PROPERTY = "xmlProperty"
    PARAMETER = "parameter"
    STATIC = "static"
