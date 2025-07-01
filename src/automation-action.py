from lxml import etree as ET
from automation_request import mapeia_wsdl
from automation_response import mapeia_wsdl_response, monta_status, monta_parameters

arquivo = "consulta"
wsdl = "nfse04.wsdl"
operacao = "ConsultarNfsePorRps"
tag_final = "ConsultarNfseRpsEnvio"
init_envelope_resposta = "ConsultarNfseRpsResposta"
lista_fins_resposta = ["Codigo", "Mensagem", "Correcao"]
xsd = "schema_extraido.xsd"
plugin = "itaperuna"

nsmap = {"xsi": "http://www.w3.org/2001/XMLSchema-instance"}

document_action = ET.Element("document-action", nsmap=nsmap, id=f"consulta-{plugin}")

document_action.attrib[
    "{http://www.w3.org/2001/XMLSchema-instance}noNamespaceSchemaLocation"
] = "../../../schemas/document-action.xsd"

request = ET.SubElement(document_action, "request")

endpoint = ET.SubElement(request, "endpoint")

url_parameter_name = ET.SubElement(endpoint, "urlParameterName")
url_parameter_name.text = f"url-endpoint-{arquivo}"

method = ET.SubElement(endpoint, "method")
method.text = "POST"

tls = ET.SubElement(endpoint, "tls")
tls.text = "TLSv1.2"

headers = ET.SubElement(request, "headers")

envelope, soap_action = mapeia_wsdl(wsdl, operacao, tag_final)

common_header = ET.SubElement(
    headers, "commonHeader", name="Content-Type", value="text/xml;charset=UTF-8"
)
common_header2 = ET.SubElement(
    headers, "commonHeader", name="SOAPAction", value=soap_action
)

body = ET.SubElement(request, "body")

input = ET.SubElement(body, "input", encoder="STRING")

document_mapper = ET.SubElement(input, "document-mapper")
document_mapper.text = f"{arquivo}-mapper.xml"

content = ET.SubElement(input, "content")

template = ET.SubElement(content, "template", inputResultVariable="REQUEST_CONTENT")
template.text = ET.CDATA(envelope)

xpath_saida = mapeia_wsdl_response(wsdl, operacao)

response = ET.SubElement(document_action, "response")
response_body = ET.SubElement(response, "body")
response_input = ET.SubElement(response_body, "input")
response_content = ET.SubElement(response_input, "content", xpath=xpath_saida)

status = ET.SubElement(response_body, "status", optional="false")
status = monta_status(arquivo, status, init_envelope_resposta, lista_fins_resposta, xsd)
ET.SubElement(status, "default", status="UNKNOWN")

details = ET.SubElement(response_body, "details", optional="false")
ET.SubElement(details, "message", id="codigo", type="ERROR", xpath="")
ET.SubElement(details, "message", id="mensagem", type="ERROR", xpath="")
ET.SubElement(details, "message", id="correcao", type="ERROR", xpath="")

parameters = monta_parameters(
    arquivo, response_body, init_envelope_resposta, lista_fins_resposta, xsd
)

response = ET.SubElement(document_action, "checksum")
response = ET.SubElement(document_action, "signature")

xml_content = ET.tostring(
    document_action, pretty_print=True, encoding="utf-8", xml_declaration=True
).decode("utf-8")

with open(f"{arquivo}2-action.xml", "w", encoding="utf-8") as f:
    f.write(xml_content)
