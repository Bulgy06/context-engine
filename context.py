import os
import ast
import sys

def get_call_name(func):
    if isinstance(func,ast.Attribute):
        return get_call_name(func.value)+"."+func.attr
    elif isinstance(func,ast.Name):
        return func.id
    else:
        return "unknown"
def get_functions(filepath):
    with open(filepath, 'r') as f:
        tree=ast.parse(f.read())
        call_graph={}
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_name=node.name
                functions=[]
                for node2 in ast.walk(node):
                    if isinstance(node2,ast.Call):
                        functions.append(get_call_name(node2.func))
                call_graph[function_name]=list(set(functions))       
    return call_graph

def scan_codebase(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".py"):
                filepath=os.path.join(root, filename)
                funcs=get_functions(filepath)
                for i in funcs:
                    print(i,funcs[i])
                        

if __name__ == "__main__":
    scan_codebase(sys.argv[1])
