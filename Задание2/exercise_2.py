import tkinter as tk
from tkinter import messagebox


class BankingSystem:
    """Класс для управления банковскими счетами"""

    def __init__(self):
        # Инициализация банка с начальным клиентом
        self.accounts = {"Manuylov": 70210562}

    def deposit(self, name, amount):
        """Пополнение счета клиента"""
        if name not in self.accounts:
            self.accounts[name] = 0
        self.accounts[name] += amount
        return f"{name} {self.accounts[name]}"

    def withdraw(self, name, amount):
        """Снятие денег со счета клиента"""
        if name not in self.accounts:
            self.accounts[name] = 0
        self.accounts[name] -= amount
        return f"{name} {self.accounts[name]}"

    def balance(self, name=None):
        """Запрос баланса клиента или всех клиентов"""
        if name:
            if name in self.accounts:
                return f"{name} {self.accounts[name]}"
            else:
                return "NO CLIENT"
        else:
            # Вывод баланса всех клиентов
            result = []
            for client_name in sorted(self.accounts.keys()):
                result.append(f"{client_name} {self.accounts[client_name]}")
            return "\n".join(result)

    def transfer(self, name1, name2, amount):
        """Перевод денег между счетами клиентов"""
        if name1 not in self.accounts:
            self.accounts[name1] = 0
        if name2 not in self.accounts:
            self.accounts[name2] = 0

        self.accounts[name1] -= amount
        self.accounts[name2] += amount

        return f"{name1} {self.accounts[name1]}\n{name2} {self.accounts[name2]}"

    def income(self, percent):
        """Начисление процентов всем клиентам с положительным балансом"""
        result = []
        for name in sorted(self.accounts.keys()):
            if self.accounts[name] > 0:
                self.accounts[name] += int(self.accounts[name] * percent / 100)
            result.append(f"{name} {self.accounts[name]}")
        return "\n".join(result)

    def process_command(self, command_line):
        """Обработка одной команды"""
        parts = command_line.strip().split()

        if not parts:
            return ""

        command = parts[0].upper()

        try:
            if command == "DEPOSIT":
                if len(parts) != 3:
                    raise ValueError("Неверное количество параметров")
                name = parts[1]
                amount = int(parts[2])
                return self.deposit(name, amount)

            elif command == "WITHDRAW":
                if len(parts) != 3:
                    raise ValueError("Неверное количество параметров")
                name = parts[1]
                amount = int(parts[2])
                return self.withdraw(name, amount)

            elif command == "BALANCE":
                if len(parts) == 1:
                    return self.balance()
                elif len(parts) == 2:
                    name = parts[1]
                    return self.balance(name)
                else:
                    raise ValueError("Неверное количество параметров")

            elif command == "TRANSFER":
                if len(parts) != 4:
                    raise ValueError("Неверное количество параметров")
                name1 = parts[1]
                name2 = parts[2]
                amount = int(parts[3])
                return self.transfer(name1, name2, amount)

            elif command == "INCOME":
                if len(parts) != 2:
                    raise ValueError("Неверное количество параметров")
                percent = float(parts[1])
                return self.income(percent)

            else:
                raise ValueError(f"Неизвестная команда: {command}")

        except (ValueError, IndexError) as e:
            raise ValueError(f"ОШИБКА: {command_line}")


class BankingGUI:
    """Графический интерфейс для банковской системы"""

    def __init__(self, root):
        self.root = root
        self.root.title("Банковская система управления счетами")
        self.root.geometry("1000x900")  # Увеличенный размер
        self.root.minsize(900, 800)  # Минимальный размер

        # Создаем банковскую систему
        self.bank = BankingSystem()

        # Создаем интерфейс
        self.create_widgets()

        # Привязываем клавиши
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<Shift-Return>', lambda e: self.load_file())

    def create_widgets(self):
        """Создание элементов интерфейса"""

        # Заголовок
        tk.Label(
            self.root, 
            text="Система управления банковскими счетами", 
            font=("Arial", 18, "bold"),
            bg="#3498db",
            fg="white",
            pady=20
        ).pack(fill=tk.X)

        # Метка "Ввод команд"
        tk.Label(
            self.root,
            text="Ввод команд:",
            font=("Arial", 13, "bold"),
            anchor="w",
            pady=10
        ).pack(fill=tk.X, padx=20)

        # Поле ввода команд
        self.input_text = tk.Text(
            self.root,
            height=12,
            width=80,
            font=("Courier", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=3,
            bg="#E3F2FD",
            fg="#000000",
            insertbackground="#000000"
        )
        self.input_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Кнопка РАСЧЁТ
        tk.Button(
            self.root,
            text="РАСЧЁТ (Enter)",
            command=self.calculate,
            font=("Arial", 13, "bold"),
            bg="#4CAF50",
            fg="black",
            pady=12,
            width=25
        ).pack(pady=20)

        # Метка "Результаты"
        tk.Label(
            self.root,
            text="Результаты:",
            font=("Arial", 13, "bold"),
            anchor="w",
            pady=10
        ).pack(fill=tk.X, padx=20)

        # Поле вывода результатов
        self.output_text = tk.Text(
            self.root,
            height=12,
            width=80,
            font=("Courier", 11),
            wrap=tk.WORD,
            relief=tk.SOLID,
            borderwidth=3,
            bg="#FFF9C4",
            fg="#000000",
            state=tk.DISABLED
        )
        self.output_text.pack(padx=20, pady=5, fill=tk.BOTH, expand=True)

        # Нижняя панель
        bottom_frame = tk.Frame(self.root)
        bottom_frame.pack(fill=tk.X, padx=20, pady=20)

        tk.Label(
            bottom_frame, 
            text="Имя файла:", 
            font=("Arial", 11, "bold")
        ).pack(side=tk.LEFT, padx=5)

        self.file_entry = tk.Entry(
            bottom_frame, 
            font=("Arial", 11), 
            width=35,
            relief=tk.SOLID,
            borderwidth=2
        )
        self.file_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(
            bottom_frame,
            text="Загрузить (Shift+Enter)",
            command=self.load_file,
            font=("Arial", 10, "bold"),
            bg="#2196F3",
            fg="black",
            pady=5
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            bottom_frame,
            text="Очистить",
            command=self.clear_fields,
            font=("Arial", 10, "bold"),
            bg="#FF9800",
            fg="black",
            pady=5
        ).pack(side=tk.LEFT, padx=5)

    def calculate(self):
        """Выполнение команд"""
        commands_text = self.input_text.get("1.0", tk.END).strip()

        if not commands_text:
            messagebox.showwarning("Предупреждение", "Введите команды для выполнения")
            return

        commands = commands_text.split('\n')

        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)

        for command_line in commands:
            command_line = command_line.strip()
            if not command_line:
                continue

            try:
                result = self.bank.process_command(command_line)
                output = f"{command_line}\n    {result}\n>>>\n"
                self.output_text.insert(tk.END, output)

            except ValueError as e:
                error_msg = str(e)
                self.output_text.insert(tk.END, f"{error_msg}\n>>>\n")
                break

        self.output_text.config(state=tk.DISABLED)
        self.output_text.see(tk.END)

    def load_file(self):
        """Загрузка команд из файла"""
        filename = self.file_entry.get().strip()

        if not filename:
            messagebox.showwarning("Предупреждение", "Введите имя файла")
            return

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()

            self.input_text.delete("1.0", tk.END)
            self.input_text.insert("1.0", content)

            messagebox.showinfo("Успех", f"Файл {filename} загружен успешно")

        except FileNotFoundError:
            messagebox.showerror("Ошибка", f"Файл {filename} не найден")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {str(e)}")

    def clear_fields(self):
        """Очистка полей ввода и вывода"""
        self.input_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.NORMAL)
        self.output_text.delete("1.0", tk.END)
        self.output_text.config(state=tk.DISABLED)


def main():
    """Главная функция запуска приложения"""
    root = tk.Tk()
    app = BankingGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()

