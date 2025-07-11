import lxml.etree as etree
from lxml.etree import _Element


def get_xml(tree: _Element) -> str:
    return etree.tostring(tree, encoding="unicode", pretty_print=True)


def export_xml_to_file(xml: str, path: str) -> None:
    with open(path, "w") as f:
        f.write(xml)


def _extract_local_name(name):
    if "}" in name:
        return name.split("}")[-1]
    return name


def create_xpath(element, target_element, current_path=[]):
    local_name = _extract_local_name(element.name)

    current_path = current_path + [local_name]

    if local_name == target_element:
        return current_path

    if element.type.is_complex():
        for child in element.type.content.iter_elements():
            result = create_xpath(child, target_element, current_path)

            if result:
                return result

    return None


def format_result(result):
    result = "/" + "/".join(result) if result else ""
    return result


def get_element_by_message_name(message_name: str, wsdl_root: _Element, namespaces: dict):
    message = wsdl_root.find(f"./wsdl:message[@name='{message_name}']", namespaces=namespaces)

    if message is None:
        raise ValueError("Message não encontrado")

    part = message.find("./wsdl:part", namespaces=namespaces)

    return part.get("element").split(":")[-1]
