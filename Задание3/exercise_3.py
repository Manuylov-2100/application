import tkinter as tk
import math
import re

class Calculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор")
        self.mode = "standard"
        self.memory = [0]
        self.memory_advanced = [0, 0, 0, 0]
        self.memory_index = 0
        self.expression = ""
        self.lg10_open = False
        self.sinh_open = False
        self.history = []
        self.create_standard_widgets()

    def resize_grid(self, rows, cols, start_row=0):
        for i in range(start_row, start_row + rows):
            self.grid_rowconfigure(i, weight=1)
        for j in range(cols):
            self.grid_columnconfigure(j, weight=1)

    def create_standard_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.display = tk.Entry(self, font=("Arial", 32), justify="right", bd=2, relief="ridge")
        self.display.grid(row=0, column=0, columnspan=5, sticky="nsew", padx=3, pady=3)

        self.clear_btn = tk.Button(self, text="C", font=("Arial", 16),
                                   command=lambda: self.on_click_standard("C"))
        self.clear_btn.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=2, pady=2)

        self.mode_btn = tk.Button(self, text="☰", font=("Arial", 16), command=self.toggle_mode)
        self.mode_btn.grid(row=1, column=2, columnspan=3, sticky="nsew", padx=2, pady=2)

        memory_btns = ['MC', 'MR', 'MS', 'M+', 'M-']
        for i, txt in enumerate(memory_btns):
            tk.Button(self, text=txt, font=("Arial", 16),
                      command=lambda t=txt: self.on_click_standard(t)) \
                .grid(row=2, column=i, sticky="nsew", padx=2, pady=2)

        btn_texts = [
            ('7', '8', '9', '/',  '←'),
            ('4', '5', '6', '*',  '√'),
            ('1', '2', '3', '-',  '+/-'),
            ('.',  '0', '=', '+', 'x^y'),
        ]
        for r, row in enumerate(btn_texts, 3):
            for c, txt in enumerate(row):
                if txt:
                    tk.Button(self, text=txt, font=("Arial", 16),
                              command=lambda t=txt: self.on_click_standard(t)) \
                        .grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        self.resize_grid(8, 5, start_row=0)
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def toggle_mode(self):
        if self.mode == "standard":
            self.mode = "advanced"
            self.create_advanced_widgets()
        else:
            self.mode = "standard"
            self.create_standard_widgets()

    def create_advanced_widgets(self):
        for widget in self.winfo_children():
            widget.destroy()

        self.history_display = tk.Text(self, height=5, font=("Courier", 12), state='disabled')
        self.history_display.grid(row=0, column=0, columnspan=7, sticky="nsew", padx=3, pady=3)

        self.display = tk.Entry(self, font=("Arial", 24), justify="right")
        self.display.grid(row=1, column=0, columnspan=7, sticky="nsew", padx=3, pady=3)

        self.clear_btn = tk.Button(self, text="C", font=("Arial", 16),
                                   command=lambda: self.on_click_advanced("C"))
        self.clear_btn.grid(row=2, column=0, columnspan=3, sticky="nsew", padx=2, pady=2)

        self.mode_btn = tk.Button(self, text="☰", font=("Arial", 16), command=self.toggle_mode)
        self.mode_btn.grid(row=2, column=3, columnspan=4, sticky="nsew", padx=2, pady=2)

        self.mindex = tk.IntVar(value=self.memory_index)
        for i in range(4):
            tk.Radiobutton(self, text=f"M{i+1}", variable=self.mindex, value=i,
                           command=self.on_memory_select) \
                .grid(row=3, column=i, padx=2, pady=2)

        adv_btns = [
            ('MC',  'MR', 'MS', 'M+',  'M-',   '←'),
            ('7',   '8',  '9',  '/',   '()',   'mod'),
            ('4',   '5',  '6',  '*',   '√',    'sinh'),
            ('1',   '2',  '3',  '-',   '+/-',  'lg10'),
            ('.',   '0',  '=',  '+',   'x^y',  'y√x'),
        ]
        for r, row in enumerate(adv_btns, 4):
            for c, txt in enumerate(row):
                if txt:
                    tk.Button(self, text=txt, font=("Arial", 14),
                              command=lambda t=txt: self.on_click_advanced(t)) \
                        .grid(row=r, column=c, sticky="nsew", padx=2, pady=2)

        self.resize_grid(9, 7, start_row=0)
        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.update_history()

    def on_memory_select(self):
        self.memory_index = self.mindex.get()

    def update_history(self):
        if not hasattr(self, 'history_display') or not self.history_display.winfo_exists():
            return
        self.history_display.config(state='normal')
        self.history_display.delete(1.0, tk.END)
        for line in self.history[-5:]:
            self.history_display.insert(tk.END, line + '\n')
        self.history_display.config(state='disabled')

    def add_history(self, text):
        self.history.append(text)
        self.update_history()

    def preprocess_expression(self, expr):
        expr = re.sub(r'√(-?\d+(\.\d+)?)', r'math.sqrt(\1)', expr)
        expr = re.sub(r'lg10\(', r'math.log10(', expr)
        expr = re.sub(r'sinh\(', r'math.sinh(', expr)
        expr = expr.replace('^', '**')
        expr = re.sub(r'(\d+(\.\d+)?)\s*mod\s*(\d+(\.\d+)?)', r'(\1 % \3)', expr)
        expr = re.sub(r'(-?\d+(\.\d+)?)\s*y√x\s*(-?\d+(\.\d+)?)', r'(\3 ** (1/\1))', expr)
        return expr

    def format_result(self, result):
        if isinstance(result, float):
            if abs(result - round(result)) < 1e-10:
                return str(int(round(result)))
            else:
                return str(float('{:.10g}'.format(result)))
        return str(result)

    def close_function_parentheses(self):
        if self.lg10_open:
            self.expression += ")"
            self.lg10_open = False
        if self.sinh_open:
            self.expression += ")"
            self.sinh_open = False

    def should_autoclose(self, char):
        return not (char.isdigit() or char in ('.', '+/-', ')'))

    def handle_memory_standard(self, char):
        try:
            current = float(self.expression) if self.expression not in ("", "Ошибка") else 0.0
        except ValueError:
            current = 0.0

        if char == "MC":
            self.memory[0] = 0
        elif char == "MR":
            self.close_function_parentheses()
            val = self.format_result(self.memory[0]) if isinstance(self.memory[0], float) \
                else str(self.memory[0])
            self.expression += val
        elif char == "MS":
            self.memory[0] = current
        elif char == "M+":
            self.memory[0] += current
        elif char == "M-":
            self.memory[0] -= current

    def handle_memory_advanced(self, char):
        idx = self.mindex.get()
        self.memory_index = idx

        try:
            current = float(self.expression) if self.expression not in ("", "Ошибка") else 0.0
        except ValueError:
            current = 0.0

        if char == "MC":
            self.memory_advanced[idx] = 0
        elif char == "MR":
            self.close_function_parentheses()
            val = self.format_result(self.memory_advanced[idx]) \
                if isinstance(self.memory_advanced[idx], float) \
                else str(self.memory_advanced[idx])
            self.expression += val
        elif char == "MS":
            self.memory_advanced[idx] = current
        elif char == "M+":
            self.memory_advanced[idx] += current
        elif char == "M-":
            self.memory_advanced[idx] -= current

    def on_click_standard(self, char):
        memory_chars = {'MC', 'MR', 'MS', 'M+', 'M-'}

        if char == "C":
            self.expression = ""
            self.lg10_open = False
            self.sinh_open = False

        elif char in memory_chars:
            self.handle_memory_standard(char)

        elif char == "=":
            self.close_function_parentheses()
            try:
                processed_expr = self.preprocess_expression(self.expression)
                result = eval(processed_expr, {"__builtins__": {}}, {"math": math})
                self.expression = self.format_result(result)
            except ZeroDivisionError:
                self.expression = "Деление на 0"
            except Exception:
                self.expression = "Ошибка"

        elif char == "+/-":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression

        elif char == "x^y":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += "^"

        elif char == "√":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += "√"

        elif char == "←":
            if self.expression:
                if self.lg10_open and self.expression.endswith("lg10("):
                    self.lg10_open = False
                if self.sinh_open and self.expression.endswith("sinh("):
                    self.sinh_open = False
                self.expression = self.expression[:-1]

        else:
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += char

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)

    def on_click_advanced(self, char):
        memory_chars = {'MC', 'MR', 'MS', 'M+', 'M-'}

        if char == "C":
            self.expression = ""
            self.lg10_open = False
            self.sinh_open = False

        elif char in memory_chars:
            self.handle_memory_advanced(char)

        elif char == "=":
            self.close_function_parentheses()

            try:
                processed_expr = self.preprocess_expression(self.expression)
                result = eval(processed_expr, {"__builtins__": {}}, {"math": math})
                result_str = self.format_result(result)
                self.add_history(f"{self.expression} = {result_str}")
                self.expression = result_str
            except ZeroDivisionError:
                self.add_history(f"{self.expression} = Деление на 0")
                self.expression = "Деление на 0"
            except Exception:
                self.add_history(f"{self.expression} = Ошибка")
                self.expression = "Ошибка"

        elif char == "+/-":
            if self.expression.startswith("-"):
                self.expression = self.expression[1:]
            else:
                self.expression = '-' + self.expression

        elif char == "√":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += "√"

        elif char == "lg10":
            if not self.lg10_open and not self.sinh_open:
                self.expression += "lg10("
                self.lg10_open = True

        elif char == "sinh":
            if not self.sinh_open and not self.lg10_open:
                self.expression += "sinh("
                self.sinh_open = True

        elif char == "mod":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += " mod "

        elif char == "x^y":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += "^"

        elif char == "y√x":
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += "y√x"

        elif char == "()":
            if self.lg10_open or self.sinh_open:
                self.expression += ")"
                self.lg10_open = False
                self.sinh_open = False
            else:
                open_cnt  = self.expression.count("(")
                close_cnt = self.expression.count(")")
                self.expression += "(" if open_cnt == close_cnt else ")"

        elif char == "←":
            if self.expression:
                if self.lg10_open and self.expression.endswith("lg10("):
                    self.lg10_open = False
                if self.sinh_open and self.expression.endswith("sinh("):
                    self.sinh_open = False
                self.expression = self.expression[:-1]

        else:
            if self.should_autoclose(char):
                self.close_function_parentheses()
            self.expression += char

        self.display.delete(0, tk.END)
        self.display.insert(0, self.expression)
        self.update_history()

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()
