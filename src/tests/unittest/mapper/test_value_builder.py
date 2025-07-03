
import unittest

from src.core.mapper.value.value_builder import ValueBuilder
from src.tests.utils.runner import run_test
import lxml.etree as etree 

class TestValueBuilder(unittest.TestCase):
    def setUp(self):
        self._value_builder = ValueBuilder()

    def test_build(self):
        tree = etree.Element("root")
        final_tree = self._value_builder.build(tree)
        # print(etree.tostring(tree, encoding='unicode'))
        etree.dump(tree)

if __name__ == "__main__":
    # unittest.main()
    
    run_test(TestValueBuilder, "test_build")
