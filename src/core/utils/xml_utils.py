import lxml.etree as etree
from lxml.etree import _Element


def get_xml(tree: _Element) -> str:
    return etree.tostring(tree, encoding="unicode", pretty_print=True)


def export_xml_to_file(xml: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(xml)
