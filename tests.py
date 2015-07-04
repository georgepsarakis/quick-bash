#!/usr/bin/env python
from __future__ import unicode_literals
import unittest
import os
import sys
import re
from StringIO import StringIO
from quickbash.quickbash import qsh
from quickbash.lexer import (
    t_LOGICAL,
    t_PARAMETER,
    t_STRING,
    t_VARIABLE
)
from quickbash.helpers import (
    import_module,
    quoted_string,
    read_source_file,
    startswith_any
)


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
        self.assertFalse(startswith_any('', []))
        self.assertTrue(
            startswith_any(
                'qwerty',
                [
                    re.compile('qwe'),
                    re.compile('rty')
                ]
            )
        )
        self.assertFalse(startswith_any('qqwerty', [re.compile('qwe')]))

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
        return dict([(token, transform(token),) for token in base_tokens])

    def test_logical(self):
        tokens = self.generate_tokens(
            ['eq', 'gt', 'ge', 'le', 'lt', 'ne'],
            unicode
        )
        self.apply_lexer_function_test(
            t_LOGICAL,
            tokens,
            lambda x: '@' + x + '?'
        )

    def test_parameter(self):
        tokens = self.generate_tokens(
            ['avz', 'n', '8', 'b7'],
            lambda x: '-' + x
        )
        self.apply_lexer_function_test(
            t_PARAMETER,
            tokens,
            lambda x: '~' + x
        )

    def test_variable(self):
        tokens = self.generate_tokens(['a1', 'B2', 'XYZ', 'var_1'], str)
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
        self.assertEqual('1 -eq 2', qsh('(@eq? 1 2)'))
        self.assertEqual('"$A" -gt 2', qsh('(@gt? (@var A) 2)'))
        self.assertNotEqual('"$A" -gt "2"', qsh('(@gtt? "$A" 2)'))
        self.assertEqual("'hello' -eq 'world'", qsh("(@eq? 'hello' 'world')"))
        if_else_qsh = "(@let A 1)(@if-else (@gt? (@var A) 2) "\
                      "(@export X 2) (@export Y 3))"
        if_else_compiled = """
A=1
if [ "$A" -gt 2 ]; then
    export X=2
else
    export Y=3
fi
        """
        self.assertEqual(qsh(if_else_qsh), if_else_compiled.strip())

    def test_atom(self):
        self.assertEqual('nil', qsh('(nil)'))
        self.assertEqual('false', qsh('(false)'))
        self.assertEqual('true', qsh('(true)'))
        self.assertEqual('1.1', qsh('(1.1)'))
        self.assertEqual('1', qsh('(1)'))

    def test_operations(self):
        self.assertEqual('$((1 + 1))', qsh('(+ 1 1)'))

    def test_array(self):
        self.assertEqual(
            qsh("(@array (@var A) (@var B))"),
            '("$A" "$B")'
        )

    def test_utilities(self):
        self.assertEqual(
            "grep '--max-count' '4' '--regexp' '[a-z][0-9]' 'a.txt'",
            qsh("(@grep ~~max-count 4 ~~regexp '[a-z][0-9]' a.txt)")
        )
        self.assertEqual(
            "gzip '-9' 'a.txt'",
            qsh("(@gzip ~9 a.txt)")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2, failfast=True, buffer=False)
