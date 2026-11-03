# 🧮 Simple Calculator

A modern, lightweight, and versatile calculator in Python. It supports standard arithmetic operations, scientific functions, safe mathematical expression parsing (AST-based), and provides both an interactive terminal REPL and a non-interactive CLI.

---

## 📂 Project Structure

```
.
├── 📄 main.py                   # Main executable CLI entrypoint
├── 📄 README.md                 # Project documentation & usage guide
├── 📄 .gitignore                # Git ignore patterns for Python & build files
├── 📁 calculator/               # Core application package
│   ├── 📄 __init__.py           # Package exports (Calculator)
│   ├── 📄 calculator.py         # Core Calculator engine & AST expression evaluator
│   └── 📄 cli.py                # Command-line interface & interactive REPL loop
└── 📁 tests/                    # Automated test suite
    ├── 📄 __init__.py           # Test package initialization
    └── 📄 test_calculator.py    # Unit tests for operations, parsing, and CLI
```

---

## ✨ Features

- **Standard Arithmetic**: Addition (`+`), Subtraction (`-`), Multiplication (`*`), Division (`/`), Integer Floor Division (`//`), and Modulo (`%`).
- **Power & Roots**: Exponentiation (`**` or `^`) and Square Root (`sqrt`).
- **Safe Expression Evaluator**: Uses Python's Abstract Syntax Tree (`ast`) parser to safely compute expressions without risky `eval()` vulnerabilities.
- **Built-in Constants & Math Functions**: Supports constants (`pi`, `e`) and functions (`sqrt()`, `abs()`).
- **Interactive REPL**:
  - Continuous calculation loop.
  - History recall using `ans` (referencing previous calculation output).
  - Built-in `help` command.
- **CLI Subcommands**:
  - `eval`: Quickly compute expressions directly from terminal arguments.
  - `op`: Perform single operations with explicit operands.
  - `interactive`: Start the interactive prompt.
- **Robust Error Handling**: Graceful handling and informative messages for division by zero, invalid input syntax, and negative square roots.
- **Zero External Dependencies**: Built strictly using the Python Standard Library.

---

## 🚀 Installation & Requirements

### Requirements
- **Python**: 3.8+ (tested on Python 3.12)
- No third-party packages required!

### Setup
Clone the repository:
```bash
git clone https://github.com/<your-repo>/simple-calculator.git
cd simple-calculator
```

---

## 💻 Usage

### 1. Interactive Shell (REPL)
Launch the interactive shell:
```bash
python3 main.py
# or
python3 main.py interactive
```

**Example Session:**
```text
=============================================
        Welcome to Simple Calculator!
=============================================
Type expressions (e.g. '3 + 4 * 2', 'sqrt(25)')
Type 'help' for examples or 'exit' / 'quit' to quit.
---------------------------------------------
calc> 25 * 4
= 100
calc> ans / 5
= 20
calc> sqrt(144) + 2^3
= 20
calc> 2 * pi
= 6.28318531
calc> quit
Goodbye!
```

---

### 2. Command Line Evaluation (`eval`)
Evaluate mathematical expressions in one shot:
```bash
python3 main.py eval "10 + 5 * (4 - 2)"
# Output: 20

python3 main.py eval "sqrt(81) + 2^5"
# Output: 41
```

---

### 3. Direct Operation Command (`op`)
Perform standalone arithmetic operations directly:
```bash
# Addition
python3 main.py op add 14 28
# Output: 42

# Division
python3 main.py op div 100 4
# Output: 25

# Power
python3 main.py op pow 2 10
# Output: 1024

# Square Root
python3 main.py op sqrt 64
# Output: 8
```

Available operations: `add`, `sub`, `mul`, `div`, `floordiv`, `mod`, `pow`, `sqrt`.

---

### 4. Programmatic API
You can also import and use `Calculator` directly in your Python projects:

```python
from calculator import Calculator

calc = Calculator()

# Basic arithmetic
result = calc.add(10, 5)          # 15
product = calc.multiply(4, 6)     # 24

# Advanced operations
power_res = calc.power(2, 8)      # 256
root_res = calc.square_root(49)   # 7.0

# Expression evaluation
expr_res = calc.evaluate("sqrt(16) * (3 + 2)^2") # 100.0
print(f"Result: {expr_res}")
```

---

## 🧪 Running Tests

To run the automated test suite:

```bash
python3 -m unittest discover tests -v
```

All 20 test cases verify core operations, edge cases (such as zero division, negative roots), safe expression parsing, and command-line execution.

---

## 📄 License

This project is licensed under the MIT License.
