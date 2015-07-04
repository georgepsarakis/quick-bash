from __future__ import unicode_literals
import os
import re
import operator
from pipes import quote
from itertools import chain

__all__ = [
    'TYPE_ARRAY',
    'OPERATOR_MAP',
    'INVERSE_OPERATOR_MAP',
    'startswith_any',
    'read_source_file',
    'quoted_string',
    'quote',
    'shell_quote',
    'import_module',
    'wrap',
    'create_array'
]

TYPE_ARRAY = 1

OPERATOR_MAP = {
    '+': operator.add,
    '-': operator.sub,
    '/': operator.div,
    '*': operator.mul,
    '>': operator.gt,
    '<': operator.lt,
    '>=': operator.ge,
    '<=': operator.le,
    '!=': operator.ne,
    '==': operator.eq,
}
INVERSE_OPERATOR_MAP = dict(
    zip(
        OPERATOR_MAP.values(),
        OPERATOR_MAP.keys()
    )
)


def create_array(iterable):
    return '({})'.format(
        ' '.join(
            map(
                unicode,
                chain.from_iterable(iterable)
            )
        )
    )


def startswith_any(string, prefix_regexes):
    return any(
        map(
            lambda prefix_regex: prefix_regex.match(string) is not None,
            prefix_regexes
        )
    )


def read_source_file(path):
    if not os.path.exists(path):
        raise Exception('File "%s" does not exist.' % path)
    with open(path, 'r') as f:
        return f.read()


def quoted_string(argument):
    return re.match(r'(\'.*\')|(".*")$', argument) is not None


def wrap(string, wrap_string):
    if not all([
        string.startswith(wrap_string),
        string.endswith(wrap_string)
    ]):
        return '{wrap_string}{string}{wrap_string}'.format(
            string=string,
            wrap_string=wrap_string
        )
    else:
        return string


def shell_quote(expression):
    if not isinstance(expression, basestring):
        return unicode(expression)
    expression = unicode(expression).strip('\'"')
    if not re.match(r'^\$[a-z_0-9]+$', expression, re.I) is None:
        return wrap(expression, '"')
    return wrap(quote(expression), "'")


def import_module(module_name):
    try:
        globals()[module_name] = __import__(module_name)
    except ImportError:
        return None
    else:
        return globals()[module_name]
