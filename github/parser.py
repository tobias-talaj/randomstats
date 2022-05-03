from collections import Counter
import ast

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

'''

foo = '''import re
import pandas as pd
aaa = bbb()
pd.DataFrame(goo).doodle(jjjj()).bar()
pd.DataFrame(goo).doodle(jjjj()).bar()
re.sub()
'''

class Visitor(ast.NodeVisitor):
    nodes = []

    def visit_Call(self, node):
        print(node.parent, '<-- parent')
        print(node, '<-- node')
        name = ''
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                name = f'{node.func.value.id}.'
                print(node.func.value.id, '<-- id')
            print(node.func.attr, '<-- attr')
            name += node.func.attr
        elif isinstance(node.func, ast.Name):
            name = node.func.id
            print(node.func.id, '<-- id')
        print(ast.unparse(node), '<-- unparse')
        for n in Visitor.nodes:
            if node in n[0]:
                n[1].append(name)
                break
        else:
            Visitor.nodes.append([[n for n in list(ast.walk(node)) if not isinstance(n.parent, ast.Call)], [name]])  # Appending list with children nodes, but without args
        # print(ast.dump(node, indent=4))
        print('\n')
        self.generic_visit(node)


def main():
    functions = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    Visitor().visit(tree)
    for n in Visitor.nodes:
        functions.append('.'.join(n[1][::-1]))
    print(Counter(functions))


if __name__ == '__main__':
    main()
