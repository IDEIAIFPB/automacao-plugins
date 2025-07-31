from unittest import TestCase, main

import lxml.etree as etree
from xmlschema import XMLSchema

from src.core.action.response import ConditionBuilder
from src.core.utils.constants import CONDITTIONS_MAP
from src.core.utils.xml_utils import get_xml


class TestConditionBuilder(TestCase):
    def setUp(self):
        self._builder = ConditionBuilder()
        self._schema = XMLSchema("resources/xsd-files/nfse-v2-04.xsd")
        self._root = etree.Element("teste")
        self._targets_tags = {
            "data_hora": "DataHora",
        }
        self._file_type = "cancelamento"
        self._status_type = "cancelled"

        # String de condições para status cancelled no action de cancelamento
        self._conditions_str = """<teste>
  <conditions>
    <condition comparison="EXISTS" xpath="/CancelarNfseResposta/RetCancelamento/NfseCancelamento/Confirmacao/DataHora"/>
  </conditions>
</teste>
"""

    def test_build(self):
        response_tag = self._schema.elements.get("CancelarNfseResposta")

        tree = self._builder.build(
            self._root,
            CONDITTIONS_MAP[self._file_type][self._status_type],
            self._status_type,
            response_tag,
            self._targets_tags,
        )
        s_tree = get_xml(tree)
        self.assertEqual(s_tree, self._conditions_str)


if __name__ == "__main__":
    main()
