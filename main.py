import tkinter as tk
from tkinter import messagebox

class Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        self.expression = ""
        self.input_var = tk.StringVar()

        self.display = tk.Entry(root, textvariable=self.input_var, font=("Arial", 20),
                                justify="right", bd=10, relief="ridge", state="readonly")
        self.display.grid(row=0, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

        buttons = [
            ('C', 1, 0), ('⌫', 1, 1), ('%', 1, 2), ('÷', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('×', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('−', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('+', 4, 3),
            ('±', 5, 0), ('0', 5, 1), ('.', 5, 2), ('=', 5, 3),
        ]

        for (text, row, col) in buttons:
            if text in ('C', '⌫'):
                bg, fg = '#f44336', 'white'
            elif text in ('+', '−', '×', '÷', '='):
                bg, fg = '#ff9800', 'white'
            elif text in ('%', '±'):
                bg, fg = '#607d8b', 'white'
            else:
                bg, fg = '#e0e0e0', 'black'

            btn = tk.Button(root, text=text, font=("Arial", 16), bg=bg, fg=fg,
                            command=lambda t=text: self.on_button_click(t))
            btn.grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        for i in range(1, 6):
            root.grid_rowconfigure(i, weight=1)

        root.bind('<Key>', self.on_key_press)

    def on_button_click(self, value):
        if value == 'C':
            self.clear()
        elif value == '⌫':
            self.backspace()
        elif value == '=':
            self.calculate()
        elif value == '±':
            self.negate()
        else:
            self.expression += value
            self.update_display()

    def on_key_press(self, event):
        key = event.char
        if key.isdigit() or key in '+-*/%.()':
            self.expression += key
            self.update_display()
        elif key == '\r' or key == '=':
            self.calculate()
        elif key == '\x08':
            self.backspace()
        elif key == '\x1b' or key.lower() == 'c':
            self.clear()

    def update_display(self):
        self.input_var.set(self.expression)

    def clear(self):
        self.expression = ""
        self.update_display()

    def backspace(self):
        self.expression = self.expression[:-1]
        self.update_display()

    def negate(self):
        if self.expression:
            try:
                val = float(self.expression)
                if val > 0:
                    self.expression = '-' + self.expression
                else:
                    self.expression = self.expression[1:]
                self.update_display()
            except ValueError:
                pass

    def calculate(self):
        try:
            expr = self.expression.replace('×', '*').replace('÷', '/').replace('−', '-')
            allowed = set('0123456789+-*/().% ')
            if not all(c in allowed for c in expr):
                raise ValueError
            result = eval(expr)
            if isinstance(result, float) and result.is_integer():
                result = int(result)
            self.expression = str(result)
            self.update_display()
        except ZeroDivisionError:
            messagebox.showerror("Ошибка", "Деление на ноль!")
            self.clear()
        except Exception:
            messagebox.showerror("Ошибка", "Некорректное выражение")
            self.clear()

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
