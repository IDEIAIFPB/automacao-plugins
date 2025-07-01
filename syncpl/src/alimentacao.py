import xml.etree.ElementTree as ET
import json
import os
import sys


def extract_properties_with_full_path(element, current_path="", collected=None):
    if collected is None:
        arquivo = open("properties.json", "r")
        collected = json.load(arquivo)

    for prop in element.findall("./property"):
        name = prop.get("name")
        if not name:
            continue

        # Constrói o caminho completo
        full_path = f"{current_path}/{name}" if current_path else name

        # Verifica se possui xmlProperty diretamente no <value>
        value = prop.find("value")
        if value is not None:
            sources = value.find("sources")
            if sources is not None:
                xml_prop = sources.find("xmlProperty")
                if xml_prop is not None and xml_prop.get("xpath"):
                    if full_path not in collected:
                        collected[full_path] = xml_prop.get("xpath")

        # Processa recursivamente subpropriedades
        subprops_container = prop.find("properties")
        if subprops_container is not None:
            extract_properties_with_full_path(subprops_container, full_path, collected)

    return collected


# Inicia a extração a partir da raiz <properties>
xml_file_path = sys.argv[1]

if not os.path.isfile(xml_file_path):
    print(f"Arquivo não encontrado: {xml_file_path}")
    exit

tree = ET.parse(xml_file_path)
root = tree.getroot()

properties_root = root.find("properties")
properties_dict = extract_properties_with_full_path(properties_root)

# Exibe o resultado como JSON
properties_json = open("properties.json", "w+")
properties_json.write(json.dumps(properties_dict, indent=2, ensure_ascii=False))
