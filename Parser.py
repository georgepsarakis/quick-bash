#!/usr/bin/python
import sys
from Tokenizer import Tokenizer
from Tokens import *
from operator import *
from ply.lex import LexToken

'''
Adding numbers:
integers:
var1=1
var2=2
echo $(($var1+$var2))

floating point:
a=0.5
b=0.7
n=$(echo $a+$b|bc -l)

Better solution (using awk):
a=10.94
b=87.33
awk -v a=$a -v b=$b 'BEGIN { print a/b }'
c=11.22
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

def quote_backticks(command):
  return '`' + command + '`'

def quote_variable(token):
  if is_token_type(token, 'VARIABLE'):
    token.value = '"' + token.value + '"'
  return token

def analyze_logical_condition(condition):
  pass

def is_logical_operator(token):
  return token.type in logical_operators

def is_math_operator(token):
  return token.type in mathematical_operators

def get_line_tokens(l_tokens, position):
  current_line = l_tokens[position].lineno
  line_tokens = { 'next' : [], 'previous' : [] }
  for direction in line_tokens.keys():
    if direction == 'next':
      finder = get_previous_token
      step = 1
    else:
      finder = get_next_token
      step = -1
    offset = add(step, position)  
    line_token = finder(l_tokens, offset)
    while ( line_token and ( line_token.lineno == current_line ) ):
      line_tokens[direction].append(line_token)
      offset = add(step, offset)
      line_token = finder(l_tokens, offset)
  line_tokens['item'] = l_tokens[position]    
  return line_tokens

def is_token_equal(token_1, token_2):
  for attr, value in token_1.__dict__.iteritems():
    if token_2.__dict__[attr] != value:
      return False
  return True 

def __list_contains(l, item):
  item_index = None
  try:
    item_index = l.index(item)
  except:
    pass
  return item_index  

def get_token_position(l_tokens, token, offset = 0):
  for index, _token in enumerate(l_tokens):    
    if is_token_equal(_token, token) and index >= offset:
      return index
  return None    

def __set_awk_variable(token):
  return ' -v ' + token.value.replace('$', '') + '=' + token.value

def line_contains_token_type(line_tokens, token_type, offset = 0):
  for index, token in enumerate(line_tokens):
    if token.type == token_type and index >= offset:
      return index
  return None

def search_token_types(l_tokens, token_types, matching = True, offset = 0):
  for index, token in l_tokens:
    if matching:
      test = truth
    else:
      test = not_
    if test(token.type in token_types) and index >= offset:
      return index
  return None    

def get_math_operation_bounds(line_tokens, is_assignment = True):
  if is_assignment:
    start_index = line_contains_token_type(line_token, 'EQUALS')
    end_index = len(line_tokens) - 1
  else:
    first_math_op_index = search_token_types(line_tokens, mathematical_operators)
    first_index = search_token_types(line_tokens, parentheses + reserved.values())
    last_index = search_token_types(line_tokens, mathematical_expression_tokens, False, first_index)
  return ( first_index, last_index )  

def bash_math_operation(l_tokens, position):
  '''
    awk -v a=$a -v b=$b 'BEGIN { print a/b }'
    * use backticks for evaluation except for variable assignments
  '''
  awk_command = "awk"
  line_tokens = get_line_tokens(l_tokens, position)
  variables = []
  line_tokens = line_tokens['previous'] + list(line_tokens['position']) + line_tokens['next']
  for token in line_tokens:
    if is_variable(token):
      variables.append(token)            
  ( math_start_index, math_last_index ) = get_math_operation_bounds(l_tokens)
  c += ''.join(map(__set_awk_variable, variables)) + " 'BEGIN { print %s }'"
  return awk_command


token_list_lines = {}
token_list_flattened = []

def flatten_token_list(token_list):
  global token_list_flattened

  if hasattr(token_list, '__iter__'):
    if isinstance(token_list, dict):
       for k, v in token_list.iteritems():
	 flatten_token_list(v)
    elif isinstance(token_list, list):
       for token in token_list:
         flatten_token_list(token)
  else:
    token_list_flattened.append( token_list )

#def separate_lines():
#  pass

def is_token_type(token, token_type):
  return token.type == token_type

def is_variable(token):
  return token.type == 'VARIABLE'

def is_variable_assignment(l_tokens):
  return line_contains_token_type(l_tokens, 'EQUALS')

def get_previous_token(l_tokens, position):
  if position > 0:
    return l_tokens[ position - 1 ]
  return None

def get_next_token(l_tokens, position):
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

'''
flatten_token_list(tokenizer.token_list)
separate_lines()
for line, token_list in token_list_lines.iteritems():
  print 20*'-',line,20*'-'
  print token_list
'''

for t in tokenizer.token_list:
  r_print_iterable(t)

sys.exit()

flatten_token_list(tokenizer.token_list)    
renumber_flattened_token_lines()
print token_list_flattened
#print token_list_lines



#LexToken properties -> 'lexer', 'lexpos', 'lineno', 'type', 'value'

