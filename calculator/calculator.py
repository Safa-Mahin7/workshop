"""Core calculator implementation supporting basic arithmetic, advanced operations, and safe expression evaluation."""

import ast
import math
import operator
from typing import Union

Number = Union[int, float]


class Calculator:
    """A versatile calculator supporting basic/scientific operations and expression evaluation."""

    _OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.FloorDiv: operator.floordiv,
        ast.Mod: operator.mod,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def add(self, a: Number, b: Number) -> Number:
        """Return the sum of a and b."""
        return a + b

    def subtract(self, a: Number, b: Number) -> Number:
        """Return the difference of a and b."""
        return a - b

    def multiply(self, a: Number, b: Number) -> Number:
        """Return the product of a and b."""
        return a * b

    def divide(self, a: Number, b: Number) -> float:
        """Return the quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a / b

    def floor_divide(self, a: Number, b: Number) -> int:
        """Return the integer quotient of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")
        return a // b

    def modulo(self, a: Number, b: Number) -> Number:
        """Return the modulo remainder of a divided by b.

        Raises:
            ZeroDivisionError: If b is zero.
        """
        if b == 0:
            raise ZeroDivisionError("Cannot compute modulo by zero.")
        return a % b

    def power(self, base: Number, exponent: Number) -> Number:
        """Return base raised to the power of exponent."""
        return base ** exponent

    def square_root(self, a: Number) -> float:
        """Return the square root of a.

        Raises:
            ValueError: If a is negative.
        """
        if a < 0:
            raise ValueError("Cannot calculate square root of a negative number.")
        return math.sqrt(a)

    def evaluate(self, expression: str) -> Number:
        """Safely parse and evaluate a mathematical expression string using AST.

        Supported operators: +, -, *, /, //, %, ** (or ^), unary +/-, parentheses.
        Supported functions: sqrt(x), abs(x).
        Supported constants: pi, e.

        Raises:
            ValueError: On invalid syntax or unsupported operations/tokens.
            ZeroDivisionError: On division or modulo by zero.
        """
        if not expression or not expression.strip():
            raise ValueError("Expression cannot be empty.")

        # Normalize ^ to ** for power
        cleaned_expr = expression.strip().replace("^", "**")

        try:
            tree = ast.parse(cleaned_expr, mode="eval")
        except SyntaxError as e:
            raise ValueError(f"Invalid expression syntax: {e}") from e

        return self._eval_node(tree.body)

    def _eval_node(self, node: ast.AST) -> Number:
        """Recursively evaluate an AST node safely."""
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError(f"Unsupported constant type: {type(node.value).__name__}")

        if isinstance(node, ast.UnaryOp):
            op_type = type(node.op)
            if op_type in self._OPERATORS:
                operand = self._eval_node(node.operand)
                return self._OPERATORS[op_type](operand)
            raise ValueError(f"Unsupported unary operator: {op_type.__name__}")

        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type in self._OPERATORS:
                left = self._eval_node(node.left)
                right = self._eval_node(node.right)
                if op_type in (ast.Div, ast.FloorDiv, ast.Mod) and right == 0:
                    raise ZeroDivisionError("Division or modulo by zero in expression.")
                return self._OPERATORS[op_type](left, right)
            raise ValueError(f"Unsupported binary operator: {op_type.__name__}")

        if isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                func_name = node.func.id.lower()
                if func_name == "sqrt":
                    if len(node.args) != 1:
                        raise ValueError("sqrt expects exactly 1 argument.")
                    val = self._eval_node(node.args[0])
                    if val < 0:
                        raise ValueError("Cannot calculate square root of a negative number.")
                    return math.sqrt(val)
                if func_name == "abs":
                    if len(node.args) != 1:
                        raise ValueError("abs expects exactly 1 argument.")
                    val = self._eval_node(node.args[0])
                    return abs(val)
            raise ValueError(f"Unsupported function call in expression.")

        if isinstance(node, ast.Name):
            name_lower = node.id.lower()
            if name_lower == "pi":
                return math.pi
            if name_lower == "e":
                return math.e
            raise ValueError(f"Unsupported variable or identifier: {node.id}")

        raise ValueError(f"Unsupported syntax expression element: {type(node).__name__}")
