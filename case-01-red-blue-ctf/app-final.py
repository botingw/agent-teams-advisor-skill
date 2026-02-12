#!/usr/bin/env -S python3 -I
# Defense: shebang requests isolated mode. Runtime check below enforces it.

import sys

# CRITICAL: This check MUST come before any other imports.
# In isolated mode, Python ignores PYTHONPATH, PYTHONSTARTUP,
# sitecustomize.py, and usercustomize.py — blocking environment injection.
if not sys.flags.isolated:
    import os
    os.execvp(sys.executable, [sys.executable, "-I"] + sys.argv)

import ast
import operator

# Safe math evaluator: only allows arithmetic on numbers.
# No function calls, no attribute access, no imports, no builtins.

SAFE_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

def safe_eval(node):
    """Recursively evaluate an AST node, allowing only numbers and basic arithmetic."""
    if isinstance(node, ast.Expression):
        return safe_eval(node.body)
    elif isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    elif isinstance(node, ast.BinOp) and type(node.op) in SAFE_OPS:
        left = safe_eval(node.left)
        right = safe_eval(node.right)
        return SAFE_OPS[type(node.op)](left, right)
    elif isinstance(node, ast.UnaryOp) and type(node.op) in SAFE_OPS:
        return SAFE_OPS[type(node.op)](safe_eval(node.operand))
    else:
        raise ValueError(f"Unsupported expression: {ast.dump(node)}")

def main():
    print("Simple Calculator Service v1.0")
    try:
        expression = sys.argv[1]
        tree = ast.parse(expression, mode='eval')
        result = safe_eval(tree)
        print(f"Result: {result}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
