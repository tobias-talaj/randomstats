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

def default_value():
    return []

nodes = []
objects = defaultdict(default_value)

def not_argument(node):
    if hasattr(node, 'parent'):
        if 'args' in node.parent._fields:
            if node in node.parent.args:
                return False
        else:
            not_argument(node.parent)
    return True


class CallAttributeVisitor(ast.NodeVisitor):

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
        object_name = node.targets[0].id
        print(object_name, '<-- object_name')
        children = list(ast.iter_child_nodes(node))
        for n in nodes:
            if children[1] in n[0] or (children[1].func if 'func' in children[1]._fields else None) in n[0]:
                print(n[1], '<-- initial n[1]')
                if object_name in n[1]:
                        n[1].remove(object_name)
                for a, b in objects.items():
                    if n[1][-1] == a:
                        print(b, '<-- b')
                        n[1] = n[1][:-1] + b
                        print(n[1], '<-- n[1]')
                if object_name not in objects:
                    objects[object_name] = n[1]
                    print(objects[object_name], '<-- objects 1')
                else:
                    print(n[1])
                    objects[object_name] = n[1] + objects[object_name]
                    print(objects[object_name], '<-- objects 2')
                print('\n')
                nodes.remove(n)
        



    # def visit_Assign(self, node):
    #     print(ast.unparse(node), '<-- assign')
    #     children = list(ast.iter_child_nodes(node))
    #     print(ast.dump(children[1], indent=4))
    #     for n in nodes:
    #         if children[1] in n[0] or (children[1].func if 'func' in children[1]._fields else None) in n[0]:
    #             if children[0].id in n[1]:
    #                 n[1].remove(children[0].id)
    #             objects[children[0].id] = n[1] + objects[children[0].id] + [children[0].id]
    #             print(children[0].id, n[1], '<-- key and values')
    #             nodes.remove(n)
    #     print('\n')



def main():
    functions = []
    tree = ast.parse(bar)
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node

    CallAttributeVisitor().visit(tree)
    AssignVisitor().visit(tree)

    for k, v in objects.items():
        functions.append('.'.join(v[::-1]))

    for n in nodes:
        functions.append('.'.join(n[1][::-1]))

    print(Counter(functions))


if __name__ == '__main__':
    main()
