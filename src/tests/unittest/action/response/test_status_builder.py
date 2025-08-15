from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response import StatusBuilder
from src.core.utils.constants import CONDITTIONS_MAP
from src.core.utils.xml_utils import build_output_file_path, get_xml


class TestStatusBuilder(TestCase):
    def setUp(self):
        self._builder = StatusBuilder()
        self._output_file = build_output_file_path("status_builder_test.xml")
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-02.xsd")
        self._root = etree.Element("teste")
        self._response_tag = self._schema.elements.get("CancelarNfseResposta")
        self._targets_tags = {
            "data_hora": "DataHora",
            "codigo_cancelamento": "Codigo",
        }
        self._file_type = "cancelamento"
        self._status_str = """<teste>
  <status>
    <cancelled>
      <conditions>
        <condition comparison="EXISTS" xpath="/CancelarNfseResposta/RetCancelamento/NfseCancelamento/Confirmacao/DataHora"/>
      </conditions>
    </cancelled>
    <rejected>
      <conditions>
        <condition comparison="EXISTS" xpath="/CancelarNfseResposta/ListaMensagemRetorno/MensagemRetorno/Codigo"/>
      </conditions>
    </rejected>
    <default status="UNKNOWN"/>
  </status>
</teste>
"""

    def test_build(self):
        tree = self._builder.build(self._file_type, self._root, CONDITTIONS_MAP, self._response_tag, self._targets_tags)
        s_tree = get_xml(tree)
        self.assertEqual(s_tree, self._status_str)


if __name__ == "__main__":
    main()
