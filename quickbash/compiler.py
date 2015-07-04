from itertools import chain
from helpers import (
    shell_quote,
    import_module,
    create_array,
    wrap,
    OPERATOR_MAP,
    INVERSE_OPERATOR_MAP
)
from lexer import (
    MACRO_BACKTICKS,
    MACRO_IF_ELSE,
    MACRO_LET,
    MACRO_EXPORT,
    MACRO_PIPE,
    MACRO_COMMENT,
    MACRO_RAW,
    MACRO_FOR,
    MACRO_VAR,
    MACRO_ARRAY
)

# Parsing rules
precedence = ()


def p_sexprs(t):
    """
    sexprs : sexprs sexpr
    sexprs : sexpr
    """
    if len(t) == 2:
        t[0] = [t[1]]
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
         | TRUE
         | FALSE
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
        if f.__name__ in ['add', 'div', 'mul', 'sub']:
            t[0] = '$(({} {} {}))'.format(
                t[3][0],
                INVERSE_OPERATOR_MAP[f],
                t[3][1]
            )
        else:
            t[0] = f(*t[3])
        if fname == "range":
            t[0] = create_array(t[0])
    elif isinstance(f, basestring):
        if f == MACRO_FOR:
            loop_variable, iterable, body = t[3]
            t[0] = """for %s in $( %s ); do
                %s
            done""" % (loop_variable, iterable, body,)
        elif f == MACRO_ARRAY:
            t[0] = create_array([t[3]])
        elif f == MACRO_BACKTICKS:
            t[0] = '`%s`' % t[3].replace("'", '')
        elif f == MACRO_VAR:
            t.is_variable = True
            t[0] = wrap('${}'.format(t[3]), '"')
        elif f == MACRO_LET:
            t[3][1] = shell_quote(t[3][1])
            t[0] = "%s=%s" % tuple(t[3])
        elif f == MACRO_EXPORT:
            t[3][1] = shell_quote(t[3][1])
            t[0] = "export %s=%s" % tuple(t[3])
        elif f == MACRO_IF_ELSE:
            condition, body, else_body = t[3]
            t[0] = """if [ {} ]; then
                {}
            else
                {}
            fi""".format(
                condition,
                body,
                else_body
            )
        elif f.strip('?') in ('ne', 'eq', 'gt', 'ge', 'lt', 'le',):
            left_operand, right_operand = t[3]
            t[0] = ' '.join([
                shell_quote(left_operand),
                '-{}'.format(f.strip('?')),
                shell_quote(right_operand)
            ])
        elif f in (MACRO_COMMENT, MACRO_RAW):
            if t[3].startswith("'"):
                strip_char = "'"
            else:
                strip_char = '"'
            t[0] = t[3].strip(strip_char)
            if f == MACRO_COMMENT:
                t[0] = '# %s' % t[0]
        elif f == MACRO_PIPE:
            t[0] = ' | '.join(t[3])
        else:
            if isinstance(t[3], list):
                def _quote_tokens(token):
                    if hasattr(t, 'is_variable'):
                        if getattr(t, 'is_variable'):
                            return '"{}"'.format(
                                unicode(token)
                            )
                    else:
                        return shell_quote(
                            unicode(token)
                        )
                t[0] = "{} {}".format(
                    f,
                    ' '.join(
                        map(
                            _quote_tokens,
                            chain(t[3])
                        )
                    )
                )
            else:
                t[0] = "%s %s" % (f, t[3])
    if isinstance(t[0], bool):
        t[0] = unicode(t[0]).lower()


def p_apply_python_function(t):
    """
    sexpr : LPAREN python_function sexprs RPAREN
    sexpr : LPAREN python_function sexpr RPAREN
    sexpr : LPAREN python_function RPAREN
    """
    python_function = t[2]
    if len(t) > 4:
        args = t[3]
        if not isinstance(args, list):
            args = (args,)
    else:
        args = ()
    python_function = python_function.split('.')
    # Import as part of package or module
    if len(python_function) > 1:
        module = import_module(python_function[0])
        if module is None:
            raise Exception(
                "Could not import modules for expression: '%s'" % t[2]
            )
        function = module
        for module_element in python_function[1:]:
            function = getattr(function, module_element)
    else:
        function_name = python_function[0]
        try:
            function = globals()['__builtins__'][function_name]
        except AttributeError:
            raise AttributeError(
                "Function does not exist in builtins: {}".format(
                    function_name
                )
            )
    result = function(*args)
    if function.__name__ == "range":
        t[0] = create_array(result)
    else:
        t[0] = shell_quote("'%s'" % unicode(function(*args)))


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
             | LOGICAL
    """
    if t[1] in OPERATOR_MAP:
        t[0] = OPERATOR_MAP[t[1]]
    elif t[1] == 'range':
        t[0] = range
    else:
        t[0] = t[1]


def p_python_function(t):
    """
    python_function : PYTHON_FUNCTION
    """
    t[0] = t[1]


def p_error(t):
    print(
        "Line {}: Syntax error at '{}'".format(
            t.lineno,
            t.value
        )
    )
