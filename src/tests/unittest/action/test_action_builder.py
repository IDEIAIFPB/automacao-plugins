from unittest import TestCase, main

from xmlschema import XMLSchema

from src.core.action import ActionBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, export_xml_to_file, get_xml


class TestActionBuilder(TestCase):
    def setUp(self):
        self._builder = ActionBuilder()
        self._output_file = build_output_file_path("action_builder_test.xml")
        self._plugin_id = "emissao-teste"
        self._signatures = [
            {"parent": "parent1", "target": "target1", "type": "type1"},
            {"parent": "parent2", "target": "target2", "type": "type2"},
        ]
        self._operation_tag = "RecepcionarLoteRps"
        self._wsdl_path = "resources/wsdl-files/nfse04.wsdl"
        self._final_envelope_tag = "EnviarLoteRpsEnvio"
        self._parsed_xsd = XMLSchema("resources/xsd-files/nfse-v2-02.xsd")
        self._response_tag = "EnviarLoteRpsResposta"
        self._targets_tags = {
            "numero_param": "NumeroLote",
            "protocolo_param": "Protocolo",
            "aliquota_param": "Aliquota",
            "codigo_verificacao_param": "CodigoVerificacao",
            "codigo_details": "Codigo",
            "mensagem_detail": "Mensagem",
            "correcao_details": "Correcao",
            "numero_consulta": "NumeroLote",
            "codigo_cancelamento_consulta": "Codigo",
            "codigo_consulta": "Codigo",
            "data_hora": "DataHora",
            "codigo_cancelamento": "Codigo",
            "codigo_emissao": "Codigo",
            "numero_emissao": "NumeroLote",
        }

    def test_build(self):
        xsd_file = "resources/xsd-files/nfse-v2-02.xsd"
        output_file = build_output_file_path("cli.xml")
        root_element = "EnviarLoteRpsEnvio"
        plugin_name = "teste"
        parser = Mapper(root_element, plugin_name, xsd_file, output_file)

        mapper_tree = parser.build()

        tree = self._builder.build(
            self._plugin_id,
            self._signatures,
            self._operation_tag,
            self._wsdl_path,
            self._final_envelope_tag,
            self._parsed_xsd,
            self._response_tag,
            mapper_tree,
            self._targets_tags,
        )
        s_tree = get_xml(tree)
        export_xml_to_file(s_tree, self._output_file)


if __name__ == "__main__":
    main()
