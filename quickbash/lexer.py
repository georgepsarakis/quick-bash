from helpers import FUNCTIONS

tokens = (
    'FLOAT', 'INTEGER', 'STRING', 'VARIABLE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 
    'LPAREN', 'RPAREN', 'NIL',
    'GE', 'LE', 'GT', 'LT', 'NE', 'EQ',    
    'FUNCTION', 'BUILTINS', 'PARAMETER',
)

# Tokens
""" Macros """
MACRO_BACKTICKS = 'exec'
MACRO_IF_ELSE = 'if-else'
MACRO_LET = 'let'
MACRO_EXPORT = 'export'
MACRO_PIPE = 'pipe'
MACRO_COMMENT = 'comment'
MACRO_RAW = 'raw'
MACRO_FOR = 'for'
MACRO_EQ = '-eq'
MACRO_NE = '-ne'
MACRO_GT = '-gt'
MACRO_GE = '-ge'
MACRO_LT = '-lt'
MACRO_LE = '-le'
MACRO_LOGICAL = [
    MACRO_EQ,
    MACRO_NE,
    MACRO_GT,
    MACRO_GE,
    MACRO_LT,
    MACRO_LE,
]

""" Operators """
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_EQ  = r'=='
t_NE  = r'!='
t_GT   = r'>'
t_LT = r'<'
t_GE = r'>='
t_LE = r'<='
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
#t_EOL = r'\s*\n\s*'

""" Constants """
t_NIL     = r'nil'

def t_PARAMETER(t):
    r'\~[a-zA-Z0-9_][a-zA-Z0-9_]*'
    t.value = t.value.replace('~', '-')
    return t

def t_BUILTINS(t):
    r'\@[a-zA-Z_\-][\-a-zA-Z0-9_]*'    
    t.value = t.value.replace('@', '')
    return t

def t_FUNCTION(t):
    r'\@[a-zA-Z_\-][\-a-zA-Z0-9_]*'    
    t.value = t.value.replace('@', '')
    return t

def t_VARIABLE(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value == t_NIL:
        t.value = None
    return t

def t_STRING(t):
    r'("(\\"|[^"])*")|(\'(\\\'|[^\'])*\')'
    return t

def t_FLOAT(t):
    r'[\-]*\d+\.\d*'
    try:
        t.value = float(t.value)
    except TypeError:
        raise Exception('Could not parse float: %s' % t.value)
    return t    
    
def t_INTEGER(t):
    r'[\-]*\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        raise Exception('Could not parse integer: %s' % t.value)
    return t

# Ignored characters
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)
    

