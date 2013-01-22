#!/usr/bin/python
import sys
from Tokenizer import Tokenizer

'''
Adding numbers:
integers:
var1=1
var2=2
echo $(($var1+$var2))

floating point:
a=0.5
b=0.7
n=$(echo $a+$b|bc)
'''


code = ''
if len(sys.argv) > 1:
    try:
      f = open(sys.argv[1], 'r')
      code = f.read()
      f.close()
    except IOError as e:
      print 'File error:', e.args[0]  
else:
  print 'Nothing to parse. Please give a QuickBash file as an argument!'

tokenizer = Tokenizer(code = code)


def bash_convert_condition(condition_list):
  for position, token in condition_list:
    if is_token_type(token, 'THEN'):
      condition_list[position].value = "\n" + token.value
  parentheses = { 'RPAREN' : [], 'LPAREN' : [] }
  rparen = None
  lparen = None
  added_tokens = 0
  for index, token in condition_list:
    if not rparen and is_token_type(token, 'RPAREN'):
      rparen = token
    if not lparen and is_token_type(token, 'LPAREN'):
      lparen = token
    if is_token_type(token, 'RPAREN') or is_token_type(token, 'LPAREN'):
      parentheses[token.type].append(index + added_tokens)
      added_tokens += 1
  for token_type, positions in parentheses.iteritems():
    for p in positions:
      if token_type == 'RPAREN':
	condition_list.insert(p, rparen)
      else:
	condition_list.insert(p, lparen)    

def quote_variable(token):
  if is_token_type(token, 'VARIABLE'):
    token.value = '"' + token.value + '"'
  return token

def analyze_logical_condition(condition):
  pass

def is_token_type(token, token_type):
  return token.type == token_type

def variable_assignment(l_tokens, position):
  return is_token_type(next_token(l_tokens, position), 'EQUALS')

def previous_token(l_tokens, position):
  if position > 0:
    return l_tokens[ position - 1 ]
  return None

def next_token(l_tokens, position):
  if position < (len(l_tokens) - 1):
    return l_tokens[ position + 1]
  return None  

def check_logical(position, token):
  tokenizer.token_list[ position + 1 ]
  return token.type in logical

def r_print_iterable(a, level = 1):
  if hasattr(a, '__iter__'):
    if isinstance(a, dict):
       for k, v in a.iteritems():
         print "\t" * level, k
	 r_print_iterable(v, level + 1)
    elif isinstance(a, list):
      for r in a:
        r_print_iterable(r, level + 1)
  else:
    print "\t"*level, a      

for t in tokenizer.token_list:
  r_print_iterable(t)


#LexToken properties -> 'lexer', 'lexpos', 'lineno', 'type', 'value'

