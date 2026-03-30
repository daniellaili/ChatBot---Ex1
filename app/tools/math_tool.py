from __future__ import annotations

import ast
import operator as op


_ALLOWED_BIN_OPS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.FloorDiv: op.floordiv,
    ast.Mod: op.mod,
    ast.Pow: op.pow,
}

_ALLOWED_UNARY_OPS = {
    ast.UAdd: op.pos,
    ast.USub: op.neg,
}


def _eval_node(node: ast.AST) -> float:
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return float(node.value)

    if isinstance(node, ast.Num):  # compatibility
        return float(node.n)

    if isinstance(node, ast.BinOp):
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        operation = _ALLOWED_BIN_OPS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported operator")
        return float(operation(left, right))

    if isinstance(node, ast.UnaryOp):
        operation = _ALLOWED_UNARY_OPS.get(type(node.op))
        if operation is None:
            raise ValueError("Unsupported unary operator")
        return float(operation(_eval_node(node.operand)))

    raise ValueError("Unsupported expression")


def safe_calculate(expression: str) -> float:
    try:
        parsed = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError("Invalid expression") from exc

    return _eval_node(parsed.body)


def calculate_math(expression: str) -> str:
    try:
        result = safe_calculate(expression)
    except ZeroDivisionError:
        return "Math error: division by zero."
    except ValueError:
        return "Math error: invalid or unsupported expression."

    if result.is_integer():
        return f"The result is {int(result)}."

    return f"The result is {result}."