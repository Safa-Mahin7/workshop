"""Command-line interface for the calculator."""

import argparse
import sys
from typing import List, Optional

from .calculator import Calculator


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command-line argument parser."""
    parser = argparse.ArgumentParser(
        prog="calculator",
        description="A simple, fast, and feature-rich command-line calculator.",
        epilog="Run without arguments or with 'interactive' to start the interactive REPL.",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # Command: eval <expression>
    eval_parser = subparsers.add_parser("eval", help="Evaluate a mathematical expression string")
    eval_parser.add_argument("expression", type=str, help="Mathematical expression (e.g. '2 + 3 * 4', 'sqrt(16) + 2^3')")

    # Command: op <operation> <a> <b>
    op_parser = subparsers.add_parser("op", help="Perform a direct operation on numbers")
    op_parser.add_argument(
        "operation",
        choices=["add", "sub", "mul", "div", "floordiv", "mod", "pow", "sqrt"],
        help="Operation to perform",
    )
    op_parser.add_argument("a", type=float, help="First operand")
    op_parser.add_argument("b", type=float, nargs="?", default=None, help="Second operand (not needed for sqrt)")

    # Command: interactive
    subparsers.add_parser("interactive", help="Start an interactive calculator session")

    return parser


def run_interactive(calculator: Calculator) -> None:
    """Run an interactive calculator shell (REPL)."""
    print("=" * 45)
    print("        Welcome to Simple Calculator!        ")
    print("=" * 45)
    print("Type expressions (e.g. '3 + 4 * 2', 'sqrt(25)')")
    print("Type 'help' for examples or 'exit' / 'quit' to quit.")
    print("-" * 45)

    last_result: Optional[float] = None

    while True:
        try:
            line = input("calc> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break

        if not line:
            continue

        lower_line = line.lower()
        if lower_line in ("exit", "quit", "q"):
            print("Goodbye!")
            break

        if lower_line == "help":
            print("\nSupported operations and syntax:")
            print("  Arithmetic: +, -, *, /, //, %, ^ (or **)")
            print("  Functions:  sqrt(x), abs(x)")
            print("  Constants:  pi, e")
            print("  Special:    ans (refer to previous calculation result)")
            print("  Commands:   help, exit, quit\n")
            continue

        # Allow user to use 'ans' for the last computed result
        expr = line
        if last_result is not None:
            # Replace 'ans' case-insensitively with last_result
            expr = expr.replace("ans", str(last_result)).replace("ANS", str(last_result))

        try:
            res = calculator.evaluate(expr)
            # Format nicely: print int if it has no fractional part
            if isinstance(res, float) and res.is_integer():
                formatted_res = int(res)
            else:
                formatted_res = round(res, 8) if isinstance(res, float) else res
            print(f"= {formatted_res}")
            last_result = res
        except Exception as e:
            print(f"Error: {e}")


def main(args: Optional[List[str]] = None) -> int:
    """CLI entrypoint."""
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    calculator = Calculator()

    if parsed_args.command == "eval":
        try:
            res = calculator.evaluate(parsed_args.expression)
            if isinstance(res, float) and res.is_integer():
                print(int(res))
            else:
                print(res)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif parsed_args.command == "op":
        op = parsed_args.operation
        a = parsed_args.a
        b = parsed_args.b

        try:
            if op == "sqrt":
                res = calculator.square_root(a)
            elif op == "add":
                res = calculator.add(a, b)
            elif op == "sub":
                res = calculator.subtract(a, b)
            elif op == "mul":
                res = calculator.multiply(a, b)
            elif op == "div":
                res = calculator.divide(a, b)
            elif op == "floordiv":
                res = calculator.floor_divide(a, b)
            elif op == "mod":
                res = calculator.modulo(a, b)
            elif op == "pow":
                res = calculator.power(a, b)
            else:
                print(f"Unknown operation: {op}", file=sys.stderr)
                return 1

            if isinstance(res, float) and res.is_integer():
                print(int(res))
            else:
                print(res)
            return 0
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)
            return 1

    elif parsed_args.command == "interactive" or parsed_args.command is None:
        run_interactive(calculator)
        return 0

    return 0
