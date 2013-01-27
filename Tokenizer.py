#!/usr/bin/python
import ply.lex as lex
from Tokens import *

class Tokenizer:
    tokens = list(tokens) + list(reserved.values()) + list(builtin_functions.values()) + utilities
    token_list = []
    original_code = ''
    global_line_number = 1

    # Regular expression rules for simple tokens
    t_PIPE         = r'\=\=\='
    t_TO           = r'\-\>'
    t_APPEND       = r'\-\-\>'
    t_PLUS         = r'\+'
    t_MINUS        = r'-'
    t_TIMES        = r'\*'
    t_DIVIDE       = r'/'
    t_LPAREN       = r'\('
    t_RPAREN       = r'\)'
    t_LBRACE       = r'\{'
    t_RBRACE       = r'\}'
    t_LGEQUALS     = r'\=\='
    t_EQUALS       = r'\='
    t_SEMICOLON    = r'\;'
    t_GT           = r'\>'
    t_GE           = r'\>\='
    t_LT           = r'\<'
    t_LE           = r'\<\='
    t_NOT          = r'\!'
    t_SINGLE_QUOTE = r'\''
    t_DOUBLE_QUOTE = r'\"'
    t_COMMA        = r'\,'

    # Build the lexer
    def __init__(self, **kwargs):
       self.original_code = kwargs.pop('code')       
       self.lexer = lex.lex(module = self, **kwargs)
       self.__tokenize()
    
    def __tokenize(self):
       self.lexer.input(self.original_code)
       for token in self.lexer:
         if token.type == 'CODEBLOCK':
           self.token_list.append(self.__get_nested_code(token.value))
         else:
           self.token_list.append(token)
              
    def t_VARIABLE(self, t):
      r'\$[a-zA-Z_][a-zA-Z_0-9]*'
      return t

    def t_KEYWORDS(self, t):
      r'(?i)[a-zA-Z_][a-zA-Z_0-9]*'
      keyword = t.value.lower()
      if builtin_functions.get(keyword): # Check for builtin functions
	  t.type = 'BUILTIN_FUNCTION'
      elif keyword in utilities:
	  t.type = 'UTILITY'    
      elif reserved.get(keyword):    
	  t.type = reserved[keyword]	  
      else:
	  t.type = 'VARIABLE'    
      return t

    def t_STRING(self, t):
      r'\'[^\']*?\'|"[^"]*?"'
      t.value = t.value[1:-1]
      return t

    def t_DECIMAL(self, t):
      r'\d+?\.\d*'
      return t

# A regular expression rule with some action code
    def t_INTEGER(self, t):
      r'\d+'
      t.value = int(t.value)    
      return t

# Define a rule so we can track line numbers
    def t_newline(self, t):
      r'\n+'
#      t.lexer.lineno += len(t.value)
      Tokenizer.global_line_number += len(t.value)
      t.lexer.lineno = Tokenizer.global_line_number

# A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

# Error handling rule
    def t_error(self, t):
      print "Illegal character '%s'" % t.value[0]
      t.lexer.skip(1)

    def t_COMMENT(self, t):
      r'\#.*'
      pass
      # No return value. Token discarded

# Declare the state
    states = (
      ('codeblock', 'exclusive'),
    )

# Match the first {. Enter ccode state.
    def t_codeblock(self, t):
      r'\{'
      t.lexer.code_start = t.lexer.lexpos        # Record the starting position
      t.lexer.level = 1                          # Initial brace level
      t.lexer.begin('codeblock')                 # Enter 'codeblock' state

# Rules for the ccode state
    def t_codeblock_lbrace(self, t):     
      r'\{'
      t.lexer.level +=1                

    def t_codeblock_rbrace(self, t):
      r'\}'
      t.lexer.level -=1

      # If closing brace, return the code fragment
      if t.lexer.level == 0:
	t.value = t.lexer.lexdata[t.lexer.code_start : (t.lexer.lexpos - 1)]
	t.type = "CODEBLOCK"
	t.lexer.lineno += t.value.count('\n') 
	t.lexer.begin('INITIAL')           
	return t

    def t_codeblock_string(self, t):
      r'\"([^\\\n]|(\\.))*?\"'

    def t_codeblock_char(self, t):
      r'\'([^\\\n]|(\\.))*?\''

# Any sequence of non-whitespace characters (not braces, strings)
    def t_codeblock_nonspace(self, t):
      r'[^\s\{\}\'\"]+'

# Ignored characters (whitespace)
    t_codeblock_ignore = " \t\n"

# For bad characters, we just skip over it
    def t_codeblock_error(self, t):
      t.lexer.skip(1)

    def __get_nested_code(self, c, level = 1):
      nested_code = {}
      lexer = lex.lex(module = self)
      lexer.input(c)
      for token in lexer:
	  if not level in nested_code:
	     nested_code[level] = []
	  nested_code[level].append(token)
	  if token.type == 'CODEBLOCK':
	    nested_code[level].append(self.__get_nested_code(token.value, level + 1))
      return nested_code

''' 
LexToken properties -> 'lexer', 'lexpos', 'lineno', 'type', 'value'
class LexToken(object):
  return "LexToken(%s,%r,%d,%d)" % (self.type,self.value,self.lineno,self.lexpos)
'''
