#!/usr/bin/env python
from __future__ import unicode_literals, print_function
import os
import re
import pyparsing
from lexer import (
    t_PARAMETER,
    t_LOGICAL,
    t_FUNCTION,
    t_PYTHON_FUNCTION,
    t_VARIABLE,
    t_STRING,
    t_FLOAT,
    t_INTEGER,
    t_newline,
    t_error,
    t_ignore,
    t_PLUS,
    t_MINUS,
    t_TIMES,
    t_DIVIDE,
    t_EQ,
    t_NE,
    t_GT,
    t_LT,
    t_GE,
    t_LE,
    t_LPAREN,
    t_RPAREN,
    t_NIL,
    t_TRUE,
    t_FALSE,
    tokens
)
from compiler import (
    p_sexprs,
    p_sexpr,
    p_atom,
    p_apply_function,
    p_apply_python_function,
    p_function,
    p_python_function,
    p_error
)
from helpers import read_source_file, startswith_any


__version__ = (0, 0, 1)
__all__ = [
    'qsh'
]


PATH = os.path.dirname(os.path.abspath(__file__))
OUTPUTDIR = os.path.join(PATH, 'tmp')

# Create directory for parsetab, lextab output files
if not os.path.exists(OUTPUTDIR):
    os.mkdir(OUTPUTDIR)

# Indentation
INDENT_SPACES = 4
INDENT_DECREASE = [
    re.compile(r'fi\s*$'),
    re.compile(r'done\s*$')
]
INDENT_INCREASE = [
    re.compile(r'for\s*'),
    re.compile(r'if\s*')
]
INDENT_RESET = [
    re.compile(r'else\s*$')
]


# Build the lexer
import ply.lex as lex
lex.lex(
    module=None,
    object=None,
    debug=False,
    optimize=True,
    lextab="lextab",
    reflags=0,
    nowarn=False,
    outputdir=OUTPUTDIR
)

# Parser
import ply.yacc as yacc
yacc.yacc(
    method='LALR',
    debug=False,
    outputdir=OUTPUTDIR
)


def code_reassembly(structure):
    """
    Recursively re-assemble the results of pyparsing
    analyzed tokens
    """
    reassembled = []
    for element in structure:
        if isinstance(element, pyparsing.ParseResults):
            reassembled.append(code_reassembly(element))
        else:
            reassembled.append(element)
    return '({})'.format(
        ' '.join(map(unicode, reassembled))
    )


def preprocessor(source):
    """
    Divide raw source code to statements
    by locating longest possible parenthesized statements
    """
    expression = pyparsing.Forward()
    comment = pyparsing.cppStyleComment()
    all_chars = pyparsing.Word(
        pyparsing.printables.replace('(', '').replace(')', '')
    )
    expression << pyparsing.nestedExpr(
        content=pyparsing.OneOrMore(expression | all_chars)
    )
    syntax = pyparsing.OneOrMore(expression)
    syntax.ignore(comment)
    return [
        code_reassembly(token)
        for token in syntax.parseString(source)
    ]


def qsh(source):
    indent_level = 0
    # Initially pass through pyparsing
    preprocessed_statements = preprocessor(source)
    # Compile with yacc
    compiled_statements = [
        unicode(parsed_statement.pop())
        for parsed_statement in map(
            yacc.parse,
            preprocessed_statements
        )
        if parsed_statement is not None
    ]
    # Apply indentation
    compiled_formatted = []
    INDENT_TEMPLATE = "{indent}{expression}"
    for statement in compiled_statements:
        expressions = statement.strip().split("\n")
        for expression in map(unicode.strip, expressions):
            if startswith_any(expression, INDENT_DECREASE):
                indent_level -= INDENT_SPACES
            if startswith_any(expression, INDENT_RESET):
                current_indent = indent_level - INDENT_SPACES
            else:
                current_indent = indent_level
            compiled_formatted.append(
                INDENT_TEMPLATE.format(
                    indent=current_indent * ' ',
                    expression=expression
                )
            )
            if startswith_any(expression, INDENT_INCREASE):
                indent_level += INDENT_SPACES
    return "\n".join(compiled_formatted)


def write_qshc_file(compiled_source, path):
    output_file = os.path.splitext(os.path.abspath(path))[0] + '.qshc'
    with open(output_file, 'w') as f:
        f.write(compiled_source)
    return output_file


if __name__ == "__main__":
    import argparse
    import tempfile
    import subprocess
    import pipes

    version_string = '.'.join(map(unicode, __version__))
    argparser = argparse.ArgumentParser(
        'quick-bash compiler v'.format(
            version_string
        )
    )
    g = argparser.add_mutually_exclusive_group(required=True)
    g.add_argument('-c', '--command', help='Evaluate the passed string')
    g.add_argument('-f', '--file', help='Compile the specified source file')
    argparser.add_argument(
        '--syntax-check',
        action='store_true',
        default=False,
        help='Run through bash -n to syntax check the output script'
    )
    parameters = argparser.parse_args()

    if parameters.command is None:
        qsh_code = read_source_file(parameters.file)
    else:
        qsh_code = parameters.command
    compiled_bash_code = qsh(qsh_code)
    if parameters.syntax_check:
        with tempfile.NamedTemporaryFile() as f:
            f.write(qsh_code)
            try:
                subprocess.check_output(['bash', '-n', pipes.quote(f.name)])
            except subprocess.CalledProcessError as e:
                print('Syntax errors found:')
                print(e.output)

    if parameters.command is None:
        output_compiled_file = write_qshc_file(
            compiled_bash_code,
            parameters.file
        )
        print("Bash Compiled file: {}".format(output_compiled_file))
    else:
        print(compiled_bash_code)
