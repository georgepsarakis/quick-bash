import os
import operator
from pipes import quote
from functools import partial
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
]

TYPE_ARRAY = 1

OPERATOR_MAP = {
    '+'  : operator.add,
    '-'  : operator.sub,
    '/'  : operator.div,
    '*'  : operator.mul,
    '>'  : operator.gt,
    '<'  : operator.lt,
    '>=' : operator.ge,
    '<=' : operator.le,
    '!=' : operator.ne,
    '==' : operator.eq,
}

INVERSE_OPERATOR_MAP = dict(zip(OPERATOR_MAP.values(), OPERATOR_MAP.keys()))


def startswith_any(iterable, s):
    return filter(lambda x: s.startswith(x + ' ') or s == x, iterable)


def read_source_file(path):
    if not os.path.exists(path):
        raise Exception('File "%s" does not exist.' % path)
    with open(path, 'r') as f:
        return f.read()


def quoted_string(argument):
    argument = str(argument)
    quoted = argument.startswith("'") and argument.endswith("'")
    quoted = quoted or (argument.startswith('"') and argument.endswith('"'))
    return quoted


def quote(argument):    
    if quoted_string(argument):
        return argument
    return '"%s"' % (
        argument
        .replace('\\', '\\\\')
        .replace('"', '\\"')
        .replace('$', '\\$')
        .replace('`', '\\`')
    )


def shell_quote(expression):
    if isinstance(expression, dict):
        if expression['type'] == TYPE_ARRAY:
            return expression['value']
    expression = str(expression)
    return quote(expression) 


def import_module(module_name):
    try:
        globals()[module_name] = __import__(module_name)
    except ImportError:
        return None
    else:
        return globals()[module_name]
        
