import ast
from collections import Counter


code = '''import re
import foo
import a as b
from d.gg import b as ppp
from aaaa import tttt

def dupa():
    return 'foo'

lll = rrr()

new_lll = lll.zzz()

ppp.func()

qq, ww, ee = q(), w(), [a, v, b]

new_object = SomeClass()

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
        c.append(['.'.join(parse_chain(d, c)), d])
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


def parse_assign(d, c):
    if isinstance(d, ast.Assign):
        left = d.targets[0]
        right = d.value
        if isinstance(left, ast.Name):
            assignments.append([left.id, right])
        elif isinstance(left, ast.Tuple):
            for le, re in zip(left.elts, right.elts):
                assignments.append([le.id, re])
    else:
        for i in getattr(d, '_fields', []):
            if isinstance(t := getattr(d, i), list):
                for i in t:
                    parse_assign(i, c)
            else:
                parse_assign(t, c)


functions = []
imports = []
assignments = []
name_mapping = []

ast_parsed = ast.parse(code)
parse_imports(ast_parsed, imports)
parse_functions(ast_parsed, functions)
parse_assign(ast_parsed, assignments)

for a in assignments:
    if isinstance(a[1], (ast.Call, ast.Attribute)):
        for f in functions:
            if f[1] == a[1]:
                name_mapping.append([a[0], f[0]])
    else:
        name_mapping.append([a[0], a[1].__class__.__name__])

while set([n[0] for n in name_mapping]) & set([n[1] for n in name_mapping]):
    for mapping in name_mapping:


for index_f, f in enumerate(functions):
    for n in name_mapping:
        if n[0] == f[0][:len(n[0])]:
            functions[index_f][0] = f[0].replace(f[0][:len(n[0])], n[1])
            print(f[0][:len(n[0])], n[1])


print('name_mapping', name_mapping, len(name_mapping), '\n')

for index_f, f in enumerate(functions):
    for i in imports:
        if i[2] == f[0][:len(i[2])]:
            functions[index_f][0] = f[0].replace(f[0][:len(i[2])], '.'.join(i[:2]) if i[0] else i[1])

print(Counter([f[0] for f in functions]))
