import os
import ast
import sys

def resolve_calls(import_graph, call_graph):
    resolved_calls={}
    for func,calls in call_graph.items():
        resolved_calls[func]=[]
        for call in calls:
            if call in import_graph:
                resolved_calls[func].append(import_graph[call]+"."+call)
            else:
                resolved_calls[func].append(call)
    return resolved_calls

def get_imports(filepath):
    with open(filepath,'r') as f:
        tree=ast.parse(f.read())
        import_graph={}
        for node in ast.walk(tree):
            if isinstance(node,ast.ImportFrom):
                module=node.module
                for name in node.names:
                    import_graph[name.name]=module
    return import_graph

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
                imports=get_imports(filepath)
                resolved_calls=resolve_calls(imports, funcs)
                print(f"File: {filepath}")
                print("Imports:")
                for name,module in imports.items():
                    print(f"  {name} <-- {module}")
                print("Call graph:")
                for func, calls in resolved_calls.items():
                    print(f"  {func} --> {calls}")

if __name__ == "__main__":
    scan_codebase(sys.argv[1])
