code = '''import re

def dupa():
    return 'foo'

def remove_parentheses_brackets(input_string):
    parens = []
    opening_pb = []
    for index, ch in enumerate(input_string):
        if ch == '(' or ch == '[':
            opening_pb.append(index)
        elif (ch == ')' or ch == ']') and opening_pb:
            op = opening_pb.pop()
            if len(opening_pb) == 0:
                parens.append(input_string[op:index+1])
    for p in parens:
        input_string = input_string.replace(p, '')
    input_string = re.sub(r'[\(\)\[\]]', '', input_string).strip()
    remove_parentheses_brackets(input_string).dupa()
    return input_string

def remove_parentheses_brackets(input_string):
    parens = []
    opening_pb = []
    for index, ch in enumerate(input_string):
        if ch == '(' or ch == '[':
            opening_pb.append(index)
        elif (ch == ')' or ch == ']') and opening_pb:
            op = opening_pb.pop()
            if len(opening_pb) == 0:
                parens.append(input_string[op:index+1])
    for p in parens:
        input_string = input_string.replace(p, '')
    input_string = re.sub(r'[\(\)\[\]]', '', input_string).strip()
    remove_parentheses_brackets(input_string).dupa()
    return input_string
'''

from collections import Counter
import ast

def parse(d, c):
  def parse_chain(d, c, p=[]):
     if isinstance(d, ast.Name):
        return [d.id]+p
     if isinstance(d, ast.Call):
        for i in d.args:
           parse(i, c)
        return parse_chain(d.func, c, p)
     if isinstance(d, ast.Attribute):
        return parse_chain(d.value, c, [d.attr]+p)
  if isinstance(d, (ast.Call, ast.Attribute)):
     c.append('.'.join(parse_chain(d, c)))
  else:
     for i in getattr(d, '_fields', []):
       if isinstance(t:=getattr(d, i), list):
          for i in t:
             parse(i, c)
       else:
          parse(t, c)

results = []

parse(ast.parse(code), results)
print(Counter(results))