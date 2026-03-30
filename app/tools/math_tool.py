"""Deterministic, safe arithmetic evaluation (no LLM, no arbitrary code)."""

from __future__ import annotations

import ast
import math
import operator
from typing import Any, Dict, Type, Union

_ALLOWED_BINOPS: Dict[Type[ast.operator], Any] = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.FloorDiv: operator.floordiv,
    ast.Mod: operator.mod,
    ast.Pow: operator.pow,
}

_ALLOWED_UNARY: Dict[Type[ast.unaryop], Any] = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}

_ALLOWED_FUNCS: Dict[str, Any] = {
    "abs": abs,
    "round": round,
    "min": min,
    "max": max,
    "sqrt": math.sqrt,
    "sin": math.sin,
    "cos": math.cos,
    "tan": math.tan,
    "log": math.log,
    "log10": math.log10,
    "ceil": math.ceil,
    "floor": math.floor,
}

_ALLOWED_NAMES: Dict[str, float] = {
    "pi": math.pi,
    "e": math.e,
}


class UnsafeExpressionError(ValueError):
    pass


def _eval_node(node: ast.AST) -> Union[float, int]:
    if isinstance(node, ast.Expression):
        return _eval_node(node.body)
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)) and not isinstance(node.value, bool):
            return node.value
        raise UnsafeExpressionError("Only numeric constants are allowed.")
    if isinstance(node, ast.UnaryOp) and type(node.op) in _ALLOWED_UNARY:
        return _ALLOWED_UNARY[type(node.op)](_eval_node(node.operand))
    if isinstance(node, ast.BinOp) and type(node.op) in _ALLOWED_BINOPS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        return _ALLOWED_BINOPS[type(node.op)](left, right)
    if isinstance(node, ast.Name):
        if node.id in _ALLOWED_NAMES:
            return _ALLOWED_NAMES[node.id]
        raise UnsafeExpressionError("Name '{0}' is not allowed.".format(node.id))
    if isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
            raise UnsafeExpressionError("Only simple function calls are allowed.")
        name = node.func.id
        if name not in _ALLOWED_FUNCS:
            raise UnsafeExpressionError("Function '{0}' is not allowed.".format(name))
        fn = _ALLOWED_FUNCS[name]
        args = [_eval_node(arg) for arg in node.args]
        if node.keywords:
            raise UnsafeExpressionError("Keyword arguments are not allowed.")
        try:
            return fn(*args)
        except Exception as exc:
            raise UnsafeExpressionError(str(exc))
    raise UnsafeExpressionError("Unsupported syntax in expression.")


def calculate_math(expression: str) -> str:
    text = expression.strip()
    if not text:
        return "No expression provided."
    try:
        tree = ast.parse(text, mode="eval")
        result = _eval_node(tree)
        if isinstance(result, float) and result.is_integer():
            result = int(result)
        return str(result)
    except SyntaxError as exc:
        return "Could not parse expression: {0}".format(exc.msg)
    except UnsafeExpressionError as exc:
        return "Expression not allowed or invalid: {0}".format(exc)
    except ZeroDivisionError:
        return "Division by zero."
    except Exception as exc:
        return "Could not evaluate: {0}".format(exc)
