from __future__ import unicode_literals

tokens = [
    'FLOAT',
    'INTEGER',
    'STRING',
    'VARIABLE',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LPAREN',
    'RPAREN',
    'NIL',
    'GE',
    'LE',
    'GT',
    'LT',
    'NE',
    'EQ',
    'FUNCTION',
    'PARAMETER',
    'PYTHON_FUNCTION',
    'FALSE',
    'TRUE',
    'LOGICAL',
]

# Reserved
reserved_words = {}

# Tokens
tokens += reserved_words.values()

# Ignored characters
t_ignore = " \t"

""" Macros """
MACRO_BACKTICKS = 'exec'
MACRO_IF_ELSE = 'if-else'
MACRO_LET = 'let'
MACRO_EXPORT = 'export'
MACRO_PIPE = 'pipe'
MACRO_COMMENT = 'comment'
MACRO_RAW = 'raw'
MACRO_FOR = 'for'
MACRO_VAR = 'var'
MACRO_ARRAY = 'array'

""" Operators """
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_EQ = r'=='
t_NE = r'!='
t_GT = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_LPAREN = r'\('
t_RPAREN = r'\)'

""" Constants """
t_NIL = r'nil'
t_TRUE = r'true'
t_FALSE = r'false'


def t_PARAMETER(t):
    r'\~{1,2}[a-zA-Z0-9_]+[\-]*[a-zA-Z0-9_]*'
    t.value = t.value.replace('~', '-')
    return t


def t_LOGICAL(t):
    r'@[a-z]{2}\?'
    t.value = t.value.strip('@?')
    return t


def t_FUNCTION(t):
    r'@[a-zA-Z_]+[\-a-zA-Z0-9_]*'
    t.value = t.value.replace('@', '')
    return t


def t_PYTHON_FUNCTION(t):
    r':[a-zA-Z_\.]+[\.a-zA-Z0-9_]*'
    t.value = t.value.lstrip(':')
    return t


def t_VARIABLE(t):
    r'[a-zA-Z_\.][a-zA-Z0-9_\.]*'
    if t.value in reserved_words:
        t.type = reserved_words[t.value]
    if t.value == t_NIL:
        t.value = 'nil'
    elif t.value == t_TRUE:
        t.value = 'true'
    elif t.value == t_FALSE:
        t.value = 'false'
    return t


def t_STRING(t):
    r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    return t


def t_FLOAT(t):
    r'[\-]*\d+\.\d*'
    try:
        t.value = float(t.value)
    except TypeError:
        raise TypeError('Could not parse float: %s' % t.value)
    return t


def t_INTEGER(t):
    r'[\-]*\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        raise ValueError('Could not parse integer: %s' % t.value)
    return t


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")


def t_error(t):
    print(
        "Line {}: Illegal character '{}'".format(
            t.lineno,
            t.value[0]
        )
    )
    t.lexer.skip(1)
