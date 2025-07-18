from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response import ConditionBuilder
from src.core.utils.constants import CONDITTIONS_MAP
from src.tests.utils import get_xml


class TestConditionBuilder(TestCase):
    def setUp(self):
        self._builder = ConditionBuilder()
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = etree.Element("teste")

        # String de condições para status cancelled no action de cancelamento
        self._cancealmento_cancelled_str = """<teste>
  <conditions>
    <condition comparison="EXISTS" xpath="/CancelarNfseResposta/RetCancelamento/NfseCancelamento/Confirmacao/DataHora"/>
  </conditions>
</teste>
"""

    def test_build_cancealmento_cancelled(self):
        response_tag = self._schema.elements.get("CancelarNfseResposta")
        targets_tags = {
            "data_hora": "DataHora",
        }
        file_type = "cancelamento"
        status_type = "cancelled"
        tree = self._builder.build(
            self._root, CONDITTIONS_MAP[file_type][status_type], status_type, response_tag, targets_tags
        )
        s_tree = get_xml(tree)
        self.assertEqual(self, s_tree, self._cancealmento_cancelled_str)


if __name__ == "__main__":
    main()
