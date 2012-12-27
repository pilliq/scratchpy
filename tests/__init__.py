import unittest

from tests.parsing import ParsingTests

def all_tests():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(ParsingTests))
    return suite
