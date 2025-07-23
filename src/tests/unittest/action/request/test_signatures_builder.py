from unittest import TestCase, main

import lxml.etree as etree

from src.core.action.request import SignaturesBuilder
from src.mapper import Mapper
from src.tests.utils import build_output_file_path, get_xml


class TestSignaturesBuilder(TestCase):
    def setUp(self):
        self._builder = SignaturesBuilder()
        self._xsd_file = "resources/xsd-files/nfse-v2-04.xsd"
        output_file = build_output_file_path("cli.xml")
        self._final_envelope_tag = "GerarNfseEnvio"
        parser = Mapper(self._final_envelope_tag, "teste", self._xsd_file, output_file)
        parser.build()
        self._signatures = parser._mapper_builder.metadata.signature
        self._root = etree.Element("teste")
        self._signatures_expected = """<teste>
  <signatures>
    <signature attribute="Id" parent="Rps" target="InfDeclaracaoPrestacaoServico" type="ELEMENT"/>
  </signatures>
</teste>
"""

    def test_build(self):
        tree = self._builder.build(self._root, self._signatures)
        s_tree = get_xml(tree)
        self.assertEqual(s_tree, self._signatures_expected)


if __name__ == "__main__":
    main()
