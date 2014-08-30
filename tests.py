#!/usr/bin/env python
import unittest
import re
from quickbash.lexer import *

class MockToken(object):
    value = None
    def __init__(self, value):
        self.value = value

class TestLexer(unittest.TestCase):
    def test_parameter(self):
        tokens = [ 'avz', 'n', '8', 'b7', '(']
        for token in tokens:
            parameter = MockToken('~' + token)
            r = re.compile(t_PARAMETER.__doc__)
            self.assertIsNotNone(r.match(parameter.value))
            self.assertEqual(parameter.value.replace('~', '-'), t_PARAMETER(parameter).value)


if __name__=="__main__":
    unittest.main(verbosity=2)
