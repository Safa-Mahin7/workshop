"""Unit tests for the Calculator and CLI."""

import io
import math
import sys
import unittest
from unittest.mock import patch

from calculator.calculator import Calculator
from calculator.cli import main


class TestCalculatorOperations(unittest.TestCase):
    """Test individual Calculator methods."""

    def setUp(self):
        self.calc = Calculator()

    def test_add(self):
        self.assertEqual(self.calc.add(2, 3), 5)
        self.assertEqual(self.calc.add(-1.5, 2.5), 1.0)
        self.assertEqual(self.calc.add(0, 0), 0)

    def test_subtract(self):
        self.assertEqual(self.calc.subtract(10, 4), 6)
        self.assertEqual(self.calc.subtract(4, 10), -6)
        self.assertEqual(self.calc.subtract(-5, -5), 0)

    def test_multiply(self):
        self.assertEqual(self.calc.multiply(3, 4), 12)
        self.assertEqual(self.calc.multiply(-2, 3), -6)
        self.assertEqual(self.calc.multiply(0, 100), 0)
        self.assertAlmostEqual(self.calc.multiply(2.5, 4), 10.0)

    def test_divide(self):
        self.assertEqual(self.calc.divide(10, 2), 5.0)
        self.assertAlmostEqual(self.calc.divide(7, 2), 3.5)
        with self.assertRaises(ZeroDivisionError):
            self.calc.divide(10, 0)

    def test_floor_divide(self):
        self.assertEqual(self.calc.floor_divide(7, 2), 3)
        self.assertEqual(self.calc.floor_divide(-7, 2), -4)
        with self.assertRaises(ZeroDivisionError):
            self.calc.floor_divide(5, 0)

    def test_modulo(self):
        self.assertEqual(self.calc.modulo(10, 3), 1)
        self.assertEqual(self.calc.modulo(10, 5), 0)
        with self.assertRaises(ZeroDivisionError):
            self.calc.modulo(10, 0)

    def test_power(self):
        self.assertEqual(self.calc.power(2, 3), 8)
        self.assertEqual(self.calc.power(5, 0), 1)
        self.assertEqual(self.calc.power(4, 0.5), 2.0)
        self.assertEqual(self.calc.power(2, -1), 0.5)

    def test_square_root(self):
        self.assertEqual(self.calc.square_root(16), 4.0)
        self.assertEqual(self.calc.square_root(0), 0.0)
        self.assertAlmostEqual(self.calc.square_root(2), 1.41421356, places=6)
        with self.assertRaises(ValueError):
            self.calc.square_root(-4)


class TestCalculatorEvaluation(unittest.TestCase):
    """Test Calculator evaluate expression parsing."""

    def setUp(self):
        self.calc = Calculator()

    def test_basic_arithmetic(self):
        self.assertEqual(self.calc.evaluate("1 + 2"), 3)
        self.assertEqual(self.calc.evaluate("10 - 4"), 6)
        self.assertEqual(self.calc.evaluate("3 * 5"), 15)
        self.assertEqual(self.calc.evaluate("8 / 2"), 4.0)
        self.assertEqual(self.calc.evaluate("7 // 2"), 3)
        self.assertEqual(self.calc.evaluate("7 % 4"), 3)

    def test_operator_precedence_and_parentheses(self):
        self.assertEqual(self.calc.evaluate("2 + 3 * 4"), 14)
        self.assertEqual(self.calc.evaluate("(2 + 3) * 4"), 20)
        self.assertEqual(self.calc.evaluate("2 ^ 3 + 1"), 9)
        self.assertEqual(self.calc.evaluate("2 ** 3"), 8)
        self.assertEqual(self.calc.evaluate("-(3 + 2)"), -5)
        self.assertEqual(self.calc.evaluate("+5 * -2"), -10)

    def test_math_functions(self):
        self.assertEqual(self.calc.evaluate("sqrt(25)"), 5.0)
        self.assertEqual(self.calc.evaluate("abs(-42)"), 42)
        self.assertEqual(self.calc.evaluate("sqrt(100) + abs(-5)"), 15.0)

    def test_constants(self):
        self.assertAlmostEqual(self.calc.evaluate("pi"), math.pi)
        self.assertAlmostEqual(self.calc.evaluate("e"), math.e)
        self.assertAlmostEqual(self.calc.evaluate("2 * pi"), 2 * math.pi)

    def test_evaluation_errors(self):
        with self.assertRaises(ValueError):
            self.calc.evaluate("")
        with self.assertRaises(ValueError):
            self.calc.evaluate("   ")
        with self.assertRaises(ValueError):
            self.calc.evaluate("2 + ")
        with self.assertRaises(ValueError):
            self.calc.evaluate("import os")
        with self.assertRaises(ValueError):
            self.calc.evaluate("__import__('os').system('ls')")
        with self.assertRaises(ValueError):
            self.calc.evaluate("undefined_variable + 2")
        with self.assertRaises(ValueError):
            self.calc.evaluate("sqrt(-1)")
        with self.assertRaises(ValueError):
            self.calc.evaluate("sqrt(1, 2)")
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("10 / 0")
        with self.assertRaises(ZeroDivisionError):
            self.calc.evaluate("10 % 0")


class TestCalculatorCLI(unittest.TestCase):
    """Test CLI commands."""

    def test_cli_eval(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["eval", "2 + 3 * 4"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "14")

    def test_cli_eval_float(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["eval", "5 / 2"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "2.5")

    def test_cli_eval_error(self):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            exit_code = main(["eval", "5 / 0"])
            self.assertEqual(exit_code, 1)
            self.assertIn("Error:", mock_stderr.getvalue())

    def test_cli_op_add(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["op", "add", "15", "27"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "42")

    def test_cli_op_sqrt(self):
        with patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["op", "sqrt", "64"])
            self.assertEqual(exit_code, 0)
            self.assertEqual(mock_stdout.getvalue().strip(), "8")

    def test_cli_op_div_by_zero(self):
        with patch("sys.stderr", new_callable=io.StringIO) as mock_stderr:
            exit_code = main(["op", "div", "10", "0"])
            self.assertEqual(exit_code, 1)
            self.assertIn("Error:", mock_stderr.getvalue())

    def test_cli_interactive_flow(self):
        # Simulate typing '5 + 5', 'ans * 2', 'help', and 'exit'
        inputs = ["5 + 5", "ans * 2", "help", "exit"]
        with patch("builtins.input", side_effect=inputs), \
             patch("sys.stdout", new_callable=io.StringIO) as mock_stdout:
            exit_code = main(["interactive"])
            self.assertEqual(exit_code, 0)
            output = mock_stdout.getvalue()
            self.assertIn("= 10", output)
            self.assertIn("= 20", output)
            self.assertIn("Supported operations and syntax:", output)
            self.assertIn("Goodbye!", output)


if __name__ == "__main__":
    unittest.main()
