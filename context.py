import os
import ast
import sys

def get_functions(filepath):
    with open(filepath, 'r') as f:
        tree=ast.parse(f.read())
        functions=[]
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
    return functions

def scan_codebase(path):
    for root, dirs, files in os.walk(path):
        for filename in files:
            if filename.endswith(".py"):
                filepath=os.path.join(root, filename)
                funcs=get_functions(filepath)
                print(f"{filepath} -> {', '.join(funcs)}")

if __name__ == "__main__":
    scan_codebase(sys.argv[1])
