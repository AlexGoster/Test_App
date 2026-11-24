import importlib.util
from pathlib import Path

import tkinter as tk
import pytest

spec = importlib.util.spec_from_file_location("calculator_gui", Path(__file__).parents[1] / "main.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


@pytest.fixture(scope="module")
def root():
    root = tk.Tk()
    root.withdraw()
    yield root
    root.destroy()


@pytest.fixture
def calculator(monkeypatch, root):
    monkeypatch.setattr(module.messagebox, "showerror", lambda *args: None)
    app = module.Calculator(root)
    yield app
    for widget in root.winfo_children():
        widget.destroy()


def test_buttons_and_errors(calculator):
    for key in ["2", "+", "3", "="]:
        calculator.on_button_click(key)
    assert calculator.expression == "5"
    calculator.expression = "1÷0"
    calculator.calculate()
    assert calculator.expression == ""


def test_negate_zero(calculator):
    calculator.expression = "0"
    calculator.negate()
    assert calculator.expression == "0"


def test_scientific_result_can_be_reused(calculator):
    calculator.expression = "1/100000000"
    calculator.calculate()
    calculator.on_button_click("+")
    calculator.on_button_click("1")
    calculator.calculate()
    assert float(calculator.expression) == 1.00000001
