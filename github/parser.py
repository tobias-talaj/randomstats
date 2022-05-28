import ast
from collections import Counter


code = '''import re
import foo
import a as b
from d.gg import b as ppp
from aaaa import tttt

def dupa():
    return 'foo'

ppp.func()

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


def parse_functions(d, c):
    def parse_chain(d, c, p=[]):
        if isinstance(d, ast.Name):
            return [d.id]+p
        if isinstance(d, ast.Call):
            for i in d.args:
                parse_functions(i, c)
            return parse_chain(d.func, c, p)
        if isinstance(d, ast.Attribute):
            return parse_chain(d.value, c, [d.attr]+p)
    if isinstance(d, (ast.Call, ast.Attribute)):
        c.append('.'.join(parse_chain(d, c)))
    else:
        for i in getattr(d, '_fields', []):
            if isinstance(t := getattr(d, i), list):
                for i in t:
                    parse_functions(i, c)
            else:
                parse_functions(t, c)


def parse_imports(d, c):
    if isinstance(d, ast.Import):
        name = d.names[0].name
        asname = d.names[0].asname
        imports.append([None, name, asname if asname else name])
    elif isinstance(d, ast.ImportFrom):
        name = d.names[0].name
        asname = d.names[0].asname
        imports.append([d.module, name, asname if asname else name])
    else:
        for i in getattr(d, '_fields', []):
            if isinstance(t := getattr(d, i), list):
                for i in t:
                    parse_imports(i, c)
            else:
                parse_imports(t, c)


functions = []
imports = []
imports_functions = []

parse_imports(ast.parse(code), imports)
print(imports)

parse_functions(ast.parse(code), functions)
print(Counter(functions))

for index_f, f in enumerate(functions):
    for i in imports:
        if i[2] == f[:len(i[2])]:
            functions[index_f] = f.replace(f[:len(i[2])], '.'.join(i[:2]) if i[0] else i[1])

print(Counter(functions))