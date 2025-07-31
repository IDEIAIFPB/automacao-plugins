from enum import Enum


class SourceType(Enum):
    STATIC = "static"
    RANDOM = "random"
    VARIABLE = "variable"
    PARAMETER = "parameter"
    XML_PROPERTY = "xmlProperty"
