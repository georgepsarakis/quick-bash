import operator
from helpers import FUNCTIONS
from tokens import *
from functools import partial
from itertools import chain

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

# Parsing rules
precedence = ()

def p_sexprs(t):
    """
    sexprs : sexprs sexpr
    sexprs : sexpr
    """
    if len(t) == 2:    
        t[0] = [ t[1] ]
    else:
        if isinstance(t[1], list):
            t[0] = t[1]
            t[0].append(t[2])
        else:
            t[0] = t[2] 

def p_sexpr(t):
    """
    sexpr : atom
          | LPAREN sexpr RPAREN
          | LPAREN sexprs RPAREN
    """
    index = None
    if len(t) == 2:
        index = 1
    else:
        index = 2
    t[0] = t[index]

def p_atom(t):
    """
    atom : NIL
         | VARIABLE
         | INTEGER
         | FLOAT         
         | STRING 
         | PARAMETER
    """
    t[0] = t[1]

def p_apply_function(t):
    """
    sexpr : LPAREN function sexprs RPAREN
    sexpr : LPAREN function sexpr RPAREN
    """
    f = t[2]
    if hasattr(f, '__name__'):
        fname = f.__name__
    else:
        fname = f
    if callable(f):
        t[0] = f(*t[3])
    elif isinstance(f, basestring):
        if f == MACRO_FOR:
            loop_variable, iterable, body = t[3]
            t[0] = """for %s in $( %s ); do
                %s
            done""" % ( loop_variable, iterable, body, )
        elif f == MACRO_BACKTICKS:
            t[0] = '`%s`' % t[3].replace("'", '')
        elif f == MACRO_LET:            
            t[0] = "%s=%s" % tuple(t[3])
        elif f == MACRO_EXPORT:
            t[0] = "export %s=%s" % tuple(t[3])
        elif f == MACRO_IF_ELSE:
            condition, body, else_body = t[3]
            t[0] = """if [ %s ]; then 
                %s 
            else 
                %s
            fi""" % ( condition, body, else_body, )
        elif f in MACRO_LOGICAL:
            left, right = t[3]
            t[0] = '%s %s %s' % ( left, f, right, )
        else:
            if isinstance(t[3], list):
                t[0] = "%s %s" % (f, ' '.join(map(str, t[3])), )
            else:
                t[0] = "%s %s" % (f, t[3])

def p_function(t):
    """
    function : PLUS
             | MINUS
             | TIMES
             | DIVIDE
             | EQ
             | GT
             | GE
             | LT
             | LE
             | NE
             | FUNCTION            
             | BUILTINS
    """
    if t[1] in OPERATOR_MAP:
        t[0] = OPERATOR_MAP[t[1]]
    elif t[1] == 'range':
        t[0] = range
    elif t[1] in FUNCTIONS:
        t[0] = t[1]
    else:
        t[0] = t[1]

def p_error(t):
    print("Syntax error at '%s'" % t.value)


