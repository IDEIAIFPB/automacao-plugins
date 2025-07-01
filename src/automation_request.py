from lxml import etree as ET


def montar_envelope(
    elemento, pai, xsd, xsd_root, tag_final=None, target_namespace=None
):
    elementos = elemento.findall(
        ".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
    )
    name = elemento.get("name")
    if name is None or name == tag_final:
        pai.text = "REQUEST_CONTENT"
        return
    pai = ET.SubElement(pai, ET.QName(target_namespace, name))

    if xsd_root.get("elementFormDefault") != "qualified":
        target_namespace = None
    for elemento_interno in elementos:
        montar_envelope(
            elemento_interno, pai, xsd, xsd_root, tag_final, target_namespace
        )
        return

    if elemento.get("type") is not None:
        tipo = elemento.get("type").split(":")[-1]
        tipo_complexo = xsd.find(
            f"./xsd:complexType[@name='{tipo}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )

        if tipo_complexo is not None:
            atributo = tipo_complexo.find(
                "./xsd:attribute",
                namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
            )

            if atributo is not None:
                pai.set(atributo.get("name"), "?")

        if tipo_complexo is not None:
            percorre_tipo_complexo(
                tipo_complexo, pai, xsd, xsd_root, tag_final, target_namespace
            )
            return

    pai.text = "?"


def percorre_tipo_complexo(
    tipo_complexo, pai, xsd, xsd_root, tag_final, target_namespace=None
):
    elementos = tipo_complexo.findall(
        ".//xsd:element", namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"}
    )
    for elemento in elementos:
        montar_envelope(elemento, pai, xsd, xsd_root, tag_final, target_namespace)


def montar_header(
    xsd, xsd_root, header, nsmap, envelope, root, namespaces, target_namespace=None
):
    tag_header = ET.SubElement(envelope, ET.QName(nsmap["soapenv"], "Header"))
    if header is not None:
        message_name = header.get("message").split(":")[-1]
        element_name = get_element_by_message_name(message_name, root, namespaces)
        elemento = xsd.find(
            f"./xsd:element[@name='{element_name}']",
            namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
        )
        montar_envelope(
            elemento, tag_header, xsd, xsd_root, target_namespace=target_namespace
        )


def get_element_by_message_name(message_name, root, namespaces):
    message = root.find(
        f"./wsdl:message[@name='{message_name}']", namespaces=namespaces
    )

    if message is None:
        print("Message não encontrado")
        exit()

    part = message.find("./wsdl:part", namespaces=namespaces)

    return part.get("element").split(":")[-1]


def parse_wsdl(wsdl):
    tree = ET.parse(wsdl)
    root = tree.getroot()
    namespaces = root.nsmap

    return tree, root, namespaces


def parse_xsd(tree, namespaces):
    schema = tree.find("./wsdl:types/xsd:schema", namespaces=namespaces)

    if schema is None:
        print("Schema não encontrado")
        exit()

    xsd_importado = schema.find("./xsd:import", namespaces=namespaces)
    initial_xsd = (
        xsd_importado.get("schemaLocation") if xsd_importado is not None else None
    )

    if initial_xsd is None:
        with open("schema_extraido.xsd", "wb") as f:
            f.write(ET.tostring(schema))
        initial_xsd = "schema_extraido.xsd"

    return ET.parse(initial_xsd)


def mapeia_wsdl(wsdl, operacao, tag_final):
    tree, root, namespaces = parse_wsdl(wsdl)

    xsd = parse_xsd(tree, namespaces)

    xsd_root = xsd.getroot()
    target_namespace = xsd_root.get("targetNamespace")

    nsmap = {
        "soapenv": "http://schemas.xmlsoap.org/soap/envelope/",
        "tns": target_namespace,
        "xd": "http://www.w3.org/2000/09/xmldsig#",
    }

    envelope = ET.Element(ET.QName(nsmap["soapenv"], "Envelope"), nsmap=nsmap)

    bindig_operation_name = operacao
    bindig_operation = root.find(
        f"./wsdl:binding/wsdl:operation[@name='{bindig_operation_name}']",
        namespaces=namespaces,
    )

    if bindig_operation is None:
        print("BOperation não encontrada")
        exit()

    soap_action = bindig_operation.find("soap:operation", namespaces=namespaces).get(
        "soapAction"
    )

    header = bindig_operation.find("wsdl:input/soap:header", namespaces=namespaces)

    montar_header(
        xsd, xsd_root, header, nsmap, envelope, root, namespaces, target_namespace
    )

    operation = root.find(
        f"./wsdl:portType/wsdl:operation[@name='{bindig_operation_name}']",
        namespaces=namespaces,
    )

    if operation is None:
        print("Operation não encontrada")
        exit()

    input = operation.find("wsdl:input", namespaces=namespaces)

    if input is None:
        print("Input não encontrado")
        exit()

    message_name = input.get("message").split(":")[-1]

    element_name = get_element_by_message_name(message_name, root, namespaces)

    body = ET.SubElement(envelope, ET.QName(nsmap["soapenv"], "Body"))
    elemento = xsd.find(
        f"./xsd:element[@name='{element_name}']",
        namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
    )
    montar_envelope(elemento, body, xsd, xsd_root, tag_final, target_namespace)

    xml_content = ET.tostring(
        envelope, pretty_print=True, encoding="utf-8", xml_declaration=True
    ).decode("utf-8")

    output = operation.find("wsdl:output", namespaces=namespaces)
    output_message = output.get("message").split(":")[-1]
    output_element_name = get_element_by_message_name(output_message, root, namespaces)
    elemento = xsd.find(
        f"./xsd:element[@name='{output_element_name}']",
        namespaces={"xsd": "http://www.w3.org/2001/XMLSchema"},
    )

    return xml_content, soap_action
