import os
import re
from tokens import *
from parser import *

PATH = os.path.dirname(os.path.abspath(__file__))

# Build the lexer
import ply.lex as lex
lex.lex(None, None, 0, 1, "lextab", 0, 1, PATH)

# Parser
import ply.yacc as yacc
yacc.yacc('LALR', False, None, 'parsetab', None, 1, 1, 1, None, PATH)

__all__=['qsh', 'qsh_file']

def startswith_any(iterable, s):
    return filter(lambda x: s.startswith(x + ' ') or s == x, iterable)

def qsh(source):
    compiled = []
    lines = [ _.strip() for _ in source.split("\n") ]
    BUFFER = [[]]
    for _ in lines:
        BUFFER[-1].append(_.strip(';'))
        if _.endswith(';'):
            BUFFER.append([])
    BUFFER = [ ' '.join(_) for _ in BUFFER ]
    for line in BUFFER:
        if line.strip() == '':
            continue
        compiled.append(yacc.parse(line).pop())
    LEVEL = 0
    INDENT_SPACES = 4
    DECREASE_INDENT = [ 'fi', 'done', ]
    INCREASE_INDENT = [ 'for', 'if', ]
    EQUAL_INDENT = [ 'else', ]
    compiled_formatted = []
    for _ in map(str, compiled):
        statement = _.strip().split("\n")
        for line in statement:
            line = line.strip()
            if startswith_any(DECREASE_INDENT, line):
                LEVEL -= INDENT_SPACES
            if startswith_any(EQUAL_INDENT, line):
                compiled_formatted.append((LEVEL - INDENT_SPACES) * ' ' + line)
            else:
                compiled_formatted.append(LEVEL * ' ' + line)
            if startswith_any(INCREASE_INDENT, line):
                LEVEL += INDENT_SPACES
    return "\n".join(compiled_formatted)

def qsh_file(path):  
    output_file = os.path.splitext(os.path.abspath(path))[0] + '.qshc'
    with open(os.path.splitext(path)[0], 'w') as f:
        f.write(qsh(read_from_source_file(path)))
    return output_file
