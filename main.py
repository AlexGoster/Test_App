
import tkinter as tk
from tkinter import messagebox

class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Калькулятор")
        self.root.geometry("500x200")
        self.root.resizable(False, False)

        # Поля ввода для чисел
        self.entry1 = tk.Entry(root, width=10, font=("Arial", 14), justify="center")
        self.entry1.grid(row=0, column=0, padx=10, pady=20)

        self.entry2 = tk.Entry(root, width=10, font=("Arial", 14), justify="center")
        self.entry2.grid(row=0, column=2, padx=10, pady=20)

        # Кнопки операций (между полями)
        operations = [
            ("+", self.add),
            ("-", self.sub),
            (":", self.div),
            ("*", self.mul)
        ]

        for i, (text, command) in enumerate(operations):
            btn = tk.Button(root, text=text, width=4, height=2,
                            font=("Arial", 12), command=command)
            btn.grid(row=0, column=1, rowspan=2, padx=2, pady=2,
                     sticky="ns" if i % 2 == 0 else "ew")  # размещаем в ряд по два

        # Поле для вывода результата (справа)
        self.result_label = tk.Label(root, text="Результат", font=("Arial", 14),
                                     relief="sunken", width=15, anchor="e",
                                     bg="white")
        self.result_label.grid(row=0, column=3, rowspan=2, padx=20, pady=10, sticky="nsew")

        # Настройка весов столбцов для растягивания
        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=0)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

    def get_numbers(self):
        """Считывает числа из полей ввода, возвращает (num1, num2) или вызывает ошибку."""
        try:
            num1 = float(self.entry1.get().replace(',', '.'))
            num2 = float(self.entry2.get().replace(',', '.'))
            return num1, num2
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа!")
            return None, None

    def show_result(self, result):
        """Отображает результат в поле, округляя до 6 знаков."""
        if result is not None:
            # Если результат целое число, показываем без десятичной части
            if result == int(result):
                self.result_label.config(text=str(int(result)))
            else:
                self.result_label.config(text=f"{result:.6f}".rstrip('0').rstrip('.'))
        else:
            self.result_label.config(text="Ошибка")

    def add(self):
        a, b = self.get_numbers()
        if a is not None:
            self.show_result(a + b)

    def sub(self):
        a, b = self.get_numbers()
        if a is not None:
            self.show_result(a - b)

    def mul(self):
        a, b = self.get_numbers()
        if a is not None:
            self.show_result(a * b)

    def div(self):
        a, b = self.get_numbers()
        if a is not None:
            if b == 0:
                messagebox.showerror("Ошибка", "Деление на ноль невозможно!")
                self.result_label.config(text="Ошибка")
            else:
                self.show_result(a / b)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()