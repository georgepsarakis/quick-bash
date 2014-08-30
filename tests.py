#!/usr/bin/env python
import unittest
import os
import sys
import re
from StringIO import StringIO
from quickbash.lexer import *
from quickbash.quickbash import qsh
from quickbash.helpers import *

class MockToken(object):
    value = None
    def __init__(self, value):
        self.value = value

class TestHelpers(unittest.TestCase):
    def test_read_source_file(self):
        path = os.path.abspath(__file__)
        self.assertIn('class MockToken', read_source_file(path))
        self.assertRaises(Exception, read_source_file, path + '_')

    def test_startswith_any(self):
        self.assertIsInstance(startswith_any([], ''), list)
        self.assertEqual(['qwe',], startswith_any(['qwe', 'rty'], 'qwe rty'))
        self.assertEqual([], startswith_any(['qwe', 'rty'], 'qwerty'))

    def test_quoted_string(self):
        self.assertFalse(quoted_string('qwerty'))
        self.assertTrue(quoted_string('"qwerty"'))
        self.assertFalse(quoted_string('qwerty"'))
        self.assertTrue(quoted_string("'qwerty'"))

    def test_import_module(self):
        from types import ModuleType as module
        self.assertIsNone(import_module('abcdef'))
        self.assertIsNotNone(import_module('datetime'))
        self.assertIsInstance(import_module('datetime'), module)

class TestLexer(unittest.TestCase):
    def apply_lexer_function_test(self, f_lexer, tokens, transform=None):
        if transform is None:
            transform = str
        R = re.compile(f_lexer.__doc__)
        for token in tokens.keys():
            parameter = MockToken(transform(token))
            self.assertIsNotNone(R.match(parameter.value))
            self.assertEqual(f_lexer(parameter).value, tokens[token])

    def generate_tokens(self, base_tokens, transform):
        return dict([ (_, transform(_),) for _ in base_tokens ])

    def test_logical(self):
        tokens = self.generate_tokens(['eq','gt','ge','le','lt','ne'], str)
        self.apply_lexer_function_test(t_LOGICAL, tokens, lambda x: '@' + x + '?')

    def test_parameter(self):
        tokens = self.generate_tokens(['avz', 'n', '8', 'b7',], lambda x: '-' + x)
        self.apply_lexer_function_test(t_PARAMETER, tokens, lambda x: '~' + x)

    def test_variable(self):
        tokens = self.generate_tokens([ 'a1', 'B2', 'XYZ', 'var_1',], str)
        self.apply_lexer_function_test(t_VARIABLE, tokens, str)

    def test_string(self):
        test = r'"hello world"'
        R = re.compile(t_STRING.__doc__)
        self.assertIsNotNone(R.match(test))
        test_token = MockToken(test)
        self.assertEqual(t_STRING(test_token).value, test)
        
class TestCompiler(unittest.TestCase):
    def setUp(self):
        self.capture_output()

    def capture_output(self):
        sys.stdout.flush()
        self.redirect = StringIO()
        sys.stdout = self.redirect

    def test_logical(self):        
        self.assertEqual('"1" -eq "2"', qsh('(@eq? 1 2)'))
        self.assertEqual('"$A" -gt "2"', qsh('(@gt? "$A" 2)'))
        self.assertNotEqual('"$A" -gt "2"', qsh('(@gtt? "$A" 2)'))
    
    def test_atom(self):
        self.assertEqual('None', qsh('(nil)'))
        self.assertEqual('false', qsh('(false)'))
        self.assertEqual('true', qsh('(true)'))
        self.assertEqual('1.1', qsh('(1.1)'))
        self.assertEqual('1', qsh('(1)'))

    def test_operations(self):
        self.assertEqual(2, int(qsh('(+ 1 1)')))

if __name__=="__main__":
    unittest.main(verbosity=2)
