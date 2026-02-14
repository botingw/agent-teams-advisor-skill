import sys
import ast

ALLOWED_NODES = (
    ast.Expression, ast.BinOp, ast.UnaryOp, ast.Constant,
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow,
    ast.UAdd, ast.USub,
)

def safe_eval(expression):
    tree = ast.parse(expression, mode='eval')
    for node in ast.walk(tree):
        if not isinstance(node, ALLOWED_NODES):
            raise ValueError(f"Disallowed expression: {type(node).__name__}")
    return eval(compile(tree, '<expr>', 'eval'))

def main():
    print("Simple Calculator Service v1.0")
    try:
        expression = sys.argv[1]
        result = safe_eval(expression)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
