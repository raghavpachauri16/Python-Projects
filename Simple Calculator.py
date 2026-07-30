"""
Simple Calculator (GUI)
------------------------
A basic calculator built with Python's Tkinter library.
Enter two numbers, click an operation button, and see the result.

Operations:
    +   Addition
    -   Subtraction
    *   Multiplication
    /   Division
    %   Percentage (Number1 % of Number2)
    ^   Power (Number1 raised to Number2)
    sqrt   Square root of Number1 (Number2 is ignored)
"""

import tkinter as tk
from tkinter import messagebox
import math


def get_numbers():
    """Read and validate the two number inputs."""
    try:
        num1 = float(entry_num1.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter a valid Number 1.")
        return None, None

    # Number 2 isn't needed for sqrt, so allow it to be blank in that case.
    num2_text = entry_num2.get().strip()
    if num2_text == "":
        num2 = None
    else:
        try:
            num2 = float(num2_text)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid Number 2.")
            return None, None

    return num1, num2


def format_result(value):
    """Show integer results without a trailing .0"""
    if value == int(value):
        return str(int(value))
    return str(round(value, 6))


def calculate(op):
    """Perform the calculation for the given operation and show the result."""
    num1, num2 = get_numbers()
    if num1 is None:
        return

    if op == "sqrt":
        if num1 < 0:
            messagebox.showerror("Math Error", "Cannot take the square root of a negative number.")
            return
        result = math.sqrt(num1)
        result_label.config(text=f"Result: sqrt({format_result(num1)}) = {format_result(result)}")
        return

    if num2 is None:
        messagebox.showerror("Invalid Input", "Please enter Number 2.")
        return

    if op == "+":
        result = num1 + num2
    elif op == "-":
        result = num1 - num2
    elif op == "*":
        result = num1 * num2
    elif op == "/":
        if num2 == 0:
            messagebox.showerror("Math Error", "Cannot divide by zero.")
            return
        result = num1 / num2
    elif op == "%":
        # Interprets as "Number1 percent of Number2"
        result = (num1 * num2) / 100
    elif op == "^":
        result = num1 ** num2
    else:
        messagebox.showerror("Invalid Operation", "Unknown operation.")
        return

    result_label.config(text=f"Result: {format_result(result)}")


def clear_fields():
    """Reset all inputs and the result display."""
    entry_num1.delete(0, tk.END)
    entry_num2.delete(0, tk.END)
    result_label.config(text="Result: ")


# ---------------- GUI Setup ----------------
root = tk.Tk()
root.title("Simple Calculator")
root.geometry("340x360")
root.resizable(False, False)

# Title
tk.Label(root, text="Simple Calculator", font=("Arial", 16, "bold")).pack(pady=10)

# Input frame
input_frame = tk.Frame(root)
input_frame.pack(pady=5)

tk.Label(input_frame, text="Number 1:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
entry_num1 = tk.Entry(input_frame, width=15)
entry_num1.grid(row=0, column=1, padx=5, pady=5)

tk.Label(input_frame, text="Number 2:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
entry_num2 = tk.Entry(input_frame, width=15)
entry_num2.grid(row=1, column=1, padx=5, pady=5)
tk.Label(input_frame, text="(leave blank for sqrt)", font=("Arial", 8), fg="gray").grid(
    row=2, column=1, sticky="w", padx=5
)

# Operation buttons
ops_frame = tk.Frame(root)
ops_frame.pack(pady=10)

operations = [
    ("+", "+"),
    ("-", "-"),
    ("*", "*"),
    ("/", "/"),
    ("%", "%"),
    ("^ (power)", "^"),
    ("sqrt", "sqrt"),
]

for i, (label, op_code) in enumerate(operations):
    row, col = divmod(i, 4)
    tk.Button(
        ops_frame, text=label, width=8, bg="#4CAF50", fg="white",
        command=lambda o=op_code: calculate(o)
    ).grid(row=row, column=col, padx=3, pady=3)

# Clear button
tk.Button(root, text="Clear", command=clear_fields, width=10).pack(pady=5)

# Result display
result_label = tk.Label(root, text="Result: ", font=("Arial", 12), wraplength=300)
result_label.pack(pady=15)

root.mainloop()