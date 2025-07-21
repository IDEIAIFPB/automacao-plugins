from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response.details_builder import DetailsBuilder
from src.tests.utils import get_xml


class TestParametersBuilder(TestCase):
    def setUp(self):
        self._builder = DetailsBuilder()
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = etree.Element("teste")
        self._targets_tags = {
            "codigo_details": "Codigo",
            "mensagem_details": "Mensagem",
            "correcao_details": "Correcao",
        }
        self._response_tag = self._schema.elements.get("GerarNfseResposta")
        self.maxDiff = None

        self._details_str = """<teste>
  <details optional="false">
    <message id="codigo" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Codigo"/>
    <message id="mensagem" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Mensagem"/>
    <message id="correcao" type="ERROR" xpath="/GerarNfseResposta/ListaNfse/ListaMensagemAlertaRetorno/MensagemRetorno/Correcao"/>
  </details>
</teste>
"""

    def test_build(self):
        tree = self._builder.build(self._root, self._response_tag, self._targets_tags)
        s_tree = get_xml(tree)

        self.assertEqual(s_tree, self._details_str)


if __name__ == "__main__":
    main()
