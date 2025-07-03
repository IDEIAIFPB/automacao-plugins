from unittest import TestCase


def run_test(test: TestCase.__init__, test_case: str = "runTest"):
    test_suite: TestCase = test(test_case)
    test_suite.run()
