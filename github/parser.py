from collections import Counter, defaultdict
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
aaa.lll()
qqq = ppp()
qqq()
pd.DataFrame(goo).doodle(jjjj()).bar()
pd.DataFrame(goo).doodle(jjjj())
re.sub()
'''

bar = '''
foo()
aaa = bbb()
ccc = aaa().ddd()
ccc = ccc.mmm()
fff = ccc().kkkkkkkkkk
eee.rrr.jjj(o = yyy.nnn())
'''

# def parse_function_chain(functions_list):
#     functions = ''
#     for fl in functions_list:
#         functions.append('.'.join(fl[1][::-1]))
#     return functions

def default_value():
    return []

nodes = []
objects = defaultdict(default_value)

# class CallVisitor(ast.NodeVisitor):

#     def visit_Call(self, node):
#         print(node.parent, '<-- parent')
#         print(node, '<-- node')
#         name = []
#         if isinstance(node.parent, ast.Attribute) and not isinstance(node.parent.parent, ast.Call):
#             name.append(node.parent.attr)
#             print(node.parent.attr, node.parent._fields, '<-- parent attr')
#         if isinstance(node.func, ast.Attribute):
#             temp_name = ''
#             if isinstance(node.func.value, ast.Name):
#                 temp_name = f'{node.func.value.id}.'
#                 print(node.func.value.id, '<-- id')
#             print(node.func.attr, '<-- attr')
#             name.append(f'{temp_name}{node.func.attr}')
#         elif isinstance(node.func, ast.Name):
#             name.append(node.func.id)
#             print(node.func.id, '<-- id')
#         print(ast.unparse(node), '<-- unparse')
#         for n in nodes:
#             if node in n[0]:
#                 n[1] += name
#                 break
#         else:
#             nodes.append([[n for n in list(ast.walk(node)) if not isinstance(n.parent, ast.Call)], name])  # Appending list with children nodes, but without args
#         print(ast.dump(node, indent=4))
#         print('\n')
#         self.generic_visit(node)

def not_argument(node):
    if hasattr(node, 'parent'):
        if 'args' in node.parent._fields:
            if node in node.parent.args:
                return False
        else:
            not_argument(node.parent)
    return True

class CallVisitor(ast.NodeVisitor):

    def visit_Call(self, node):
        print(node.parent, '<-- parent')
        print(node, '<-- node')
        name = ''

        print(ast.unparse(node), '<-- unparse')
        if isinstance(node.func, ast.Name):
            name = node.func.id
            print(node.func.id, '<-- id')

            for n in nodes:
                if node in n[0]:
                    print('CALL APPENDING')
                    try:
                        print(node.parent, node.parent._fields, node.parent.args)
                    except:
                        print('no keywords')
                    print(name)
                    n[1].append(name)
                    break
            else:
                # nodes.append([list(ast.walk(node)), [name]])
                nodes.append([[n for n in list(ast.walk(node)) if not_argument(n)], [name]])
                print('CALL SAVING')
                try:
                    print(node.parent, node.parent._fields, node.parent.args)
                except:
                    print('no keywords')
                print(name)
        print(ast.dump(node.parent, indent=4))
        print('\n')
        self.generic_visit(node)

    def visit_Attribute(self, node):
        print(node.parent, '<-- parent')
        print(node, '<-- node')
        name = ''

        print(ast.unparse(node), '<-- unparse')
        name = node.attr
        print(node.attr, '<-- attr')

        for n in nodes:
            if node in n[0]:
                print('ATTRIBUTE APPENDING')
                try:
                    print(node.parent, node.parent._fields, node.parent.args)
                except:
                    print('no keywords')
                print(name)
                n[1].append(name)
                break
        else:
            nodes.append([[n for n in list(ast.walk(node)) if not_argument(n)], [name]])
            print('ATTRIBUTE SAVING')
            try:
                print(node.parent, node.parent._fields, node.parent.args)
            except:
                print('no keywords')
            print(name)

        if isinstance(node.value, ast.Name):
            name = node.value.id
            print(node.value.id, '<-- id')

            for n in nodes:
                if node in n[0]:
                    print('ATTRIBUTE APPENDING')
                    try:
                        print(node.parent, node.parent._fields, node.parent.args)
                    except:
                        print('no keywords')
                    print(name)
                    n[1].append(name)
                    break
            else:
                nodes.append([[n for n in list(ast.walk(node)) if not_argument(n)], [name]])
                print('ATTRIBUTE SAVING')
                try:
                    print(node.parent, node.parent._fields, node.parent.args)
                except:
                    print('no keywords')
                print(name)
        print(ast.dump(node.parent, indent=4))
        print('\n')
        self.generic_visit(node)


class AssignVisitor(ast.NodeVisitor):

    def visit_Assign(self, node):
        print(node, ast.unparse(node), '<-- assign')
        children = list(ast.iter_child_nodes(node))
        print(children)
        if isinstance(children[1], ast.Call):
            for n in nodes:
                if children[1] in n[0]:
                    print(children[0].id, n[1])
                    objects[children[0].id] = n[1] + objects[children[0].id]
                    print(objects)
                    nodes.remove(n)
                    # objects.append([ast.unparse(children[0]), ast.unparse(children[1])])
        elif isinstance(children[1], ast.Attribute):
            for n in nodes:
                if children[1] in n[0]:
                    print(children[0].attr, n[1])
                    objects[children[0].attr] = n[1] + objects[children[0].attr]
                    print(objects)
                    nodes.remove(n)
        print('\n')



def main():
    functions = []
    tree = ast.parse(foo)
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    print(nodes)

    CallVisitor().visit(tree)
    for n in nodes:
        functions.append('.'.join(n[1][::-1]))
    print(Counter(functions))
    print(nodes)

    print('\n', '-----------------------------------------', '\n')

    # AssignVisitor().visit(tree)
    # print(nodes)
    # print(objects)


if __name__ == '__main__':
    main()
