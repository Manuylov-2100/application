import tkinter as tk
from tkinter import ttk
import copy
import random

class HanoiTowerGUI:
    """Графический интерфейс для визуализации Ханойских башен"""

    def __init__(self, root, student_id="70210562"):
        self.root = root
        self.student_id = student_id

        # Параметры визуализации
        self.canvas_width = 1280
        self.canvas_height = 400
        self.spindle_spacing = 145
        self.start_x = 60
        self.start_y = 350
        self.disk_height = 8

        # Создаем начальное состояние
        self.initial_state = self.create_initial_state()

        # Гармоничная цветовая палитра - пастельные цвета
        self.disk_colors = self.generate_colors()

        self.background_color = "#f0f4f8"
        self.title_bg_color = "#d7e6f2"
        self.control_bg_color = "#f9f9f9"
        self.info_bg_color = "#e6f1f8"
        self.button_bg_color = "#9cb8d9"
        self.button_active_bg = "#7a95c6"

        # Цвета для текста
        self.text_color = "#1b3a57"
        self.header_text_color = "#134074"
        self.label_text_color = "#2e4a62"

        # Промежуточные проценты - из ID
        self.percentages = [
            int(student_id[0:2]),
            int(student_id[2:4]),
            int(student_id[4:6]),
            int(student_id[6:8])
        ]

        # Общее количество дисков
        self.total_disks = sum(int(d) for d in student_id)

        # Общее количество итераций
        self.total_iterations = 5000

        self.current_iteration = 0
        self.create_ui()
        self.show_iteration(0)

    def create_initial_state(self):
        state = {}
        for i, digit in enumerate(self.student_id):
            spindle = 8 - i
            count = int(digit)
            disks = []
            for pos in range(1, count + 1):
                diameter = spindle * 10 + pos
                disks.append(diameter)
            state[spindle] = disks
        return state

    def generate_colors(self):
        """Гармоничная пастельная палитра для дисков"""
        colors = {}
        color_palette = [
            "#a8dadc", "#f4a261", "#e76f51", "#457b9d",
            "#ffb4a2", "#90be6d", "#f9dcc4", "#f4d35e",
            "#5e6472", "#cdb4db", "#ffc8dd", "#b5ead7",
            "#ffe066", "#ff6f91", "#845ec2", "#d65db1"
        ]

        disk_idx = 0
        for spindle in range(8, 0, -1):
            for disk in self.initial_state.get(spindle, []):
                colors[disk] = color_palette[disk_idx % len(color_palette)]
                disk_idx += 1

        return colors

    def create_ui(self):
        self.root.title(f"Ханойские башни - ID: {self.student_id}")
        self.root.geometry("1300x850")
        self.root.resizable(False, False)
        self.root.configure(bg=self.background_color)

        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = tk.Label(
            main_frame,
            text=f"Модифицированная задача о Ханойских башнях (ID: {self.student_id})",
            font=("Arial", 12, "bold"),
            bg=self.title_bg_color,
            fg=self.header_text_color,
            pady=4
        )
        title_label.pack(fill=tk.X)

        canvas_frame = tk.Frame(main_frame, relief=tk.SUNKEN, bd=2, bg="white")
        canvas_frame.pack(pady=5, padx=5, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.canvas_width,
            height=self.canvas_height,
            bg="white"
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)

        info_frame = tk.Frame(main_frame, bg=self.info_bg_color, pady=3)
        info_frame.pack(fill=tk.X, padx=5)

        info_text = f"Всего дисков: {self.total_disks}  |  Макс итераций: {self.total_iterations}"
        self.info_label = tk.Label(
            info_frame,
            text=info_text,
            font=("Arial", 9),
            bg=self.info_bg_color,
            fg=self.text_color
        )
        self.info_label.pack()

        self.iteration_label = tk.Label(
            main_frame,
            text="Итерация: 0",
            font=("Arial", 11, "bold"),
            fg="blue",
            bg=self.background_color,
            pady=2
        )
        self.iteration_label.pack(fill=tk.X)

        control_frame = tk.Frame(main_frame, bg=self.control_bg_color, padx=5, pady=5)
        control_frame.pack(fill=tk.X)

        btn_row = tk.Frame(control_frame, bg=self.control_bg_color)
        btn_row.pack(pady=3)

        start_btn = tk.Button(
            btn_row,
            text="▶ Начало (0%)",
            command=lambda: self.show_iteration(0),
            width=16, height=1,
            bg=self.button_bg_color, font=("Arial", 9, "bold"),
            relief=tk.RAISED, bd=1,
            activebackground=self.button_active_bg
        )
        start_btn.pack(side=tk.LEFT, padx=3)

        end_btn = tk.Button(
            btn_row,
            text="⏹ Окончание (100%)",
            command=lambda: self.show_iteration(self.total_iterations),
            width=16, height=1,
            bg=self.button_bg_color, font=("Arial", 9, "bold"),
            relief=tk.RAISED, bd=1,
            activebackground=self.button_active_bg
        )
        end_btn.pack(side=tk.LEFT, padx=3)

        percent_label = tk.Label(
            control_frame,
            text="Промежуточные состояния:",
            font=("Arial", 9, "bold"),
            bg=self.control_bg_color,
            fg=self.text_color
        )
        percent_label.pack(anchor=tk.W, pady=(5, 2))

        percent_row = tk.Frame(control_frame, bg=self.control_bg_color)
        percent_row.pack()

        self.percent_entries = []

        for i in range(4):
            small_frame = tk.Frame(percent_row, bg=self.control_bg_color)
            small_frame.pack(side=tk.LEFT, padx=5)

            entry = tk.Entry(small_frame, width=4, font=("Arial", 10), justify=tk.CENTER)
            entry.insert(0, str(self.percentages[i]))
            entry.pack(side=tk.LEFT, padx=1)
            entry.bind('<Return>', lambda e, idx=i: self.show_percentage(idx))
            self.percent_entries.append(entry)

            tk.Label(small_frame, text="%", font=("Arial", 9), bg=self.control_bg_color, fg=self.text_color).pack(side=tk.LEFT)

            btn = tk.Button(
                small_frame,
                text="Показать",
                command=lambda idx=i: self.show_percentage(idx),
                width=9, height=1,
                font=("Arial", 8),
                bg="#E0E0FF", relief=tk.RAISED, bd=1,
                activebackground="#B0C4DE"
            )
            btn.pack(side=tk.LEFT, padx=2)

        self.status_label = tk.Label(
            control_frame,
            text="✓ Готово",
            font=("Arial", 9),
            fg="green",
            bg=self.control_bg_color,
            pady=2
        )
        self.status_label.pack(pady=3)

    def show_percentage(self, idx):
        try:
            percent_str = self.percent_entries[idx].get()
            percent = float(percent_str)

            if percent < 0 or percent > 100:
                self.status_label.config(
                    text="✗ Ошибка: 0-100%",
                    fg="red"
                )
                return

            iteration = (self.total_iterations * percent) / 100.0
            self.show_iteration(iteration)
            self.status_label.config(
                text=f"✓ {percent}%",
                fg="green"
            )
        except ValueError:
            self.status_label.config(
                text="✗ Число",
                fg="red"
            )

    def show_iteration(self, iteration):
        self.current_iteration = iteration
        state = self.get_state_at_iteration(iteration)
        self.draw_towers(state)

        if iteration == int(iteration):
            self.iteration_label.config(text=f"Итерация: {int(iteration)}")
        else:
            self.iteration_label.config(text=f"Итерация: {iteration:.0f}")

        self.root.update()

    def get_state_at_iteration(self, iteration):
        state = copy.deepcopy(self.initial_state)

        if iteration <= 0:
            return state

        progress = min(1.0, iteration / self.total_iterations)

        disks_to_move = int(self.total_disks * progress)

        if disks_to_move > 0:
            all_disks = []
            for spindle in range(8, 0, -1):
                all_disks.extend(state.get(spindle, []))
            all_disks.sort()

            for spindle in range(8, 0, -1):
                state[spindle] = []

            state[1] = all_disks[:disks_to_move]

            remaining_disks = all_disks[disks_to_move:]
            spindle_order = [8, 7, 6, 5, 4, 3, 2]
            spindle_idx = 0

            for disk in reversed(remaining_disks):
                current_spindle = spindle_order[spindle_idx % len(spindle_order)]
                state[current_spindle].insert(0, disk)
                spindle_idx += 1

        return state

    def draw_towers(self, state):
        self.canvas.delete("all")

        for spindle_idx in range(8):
            spindle = 8 - spindle_idx
            x = self.start_x + spindle_idx * self.spindle_spacing

            self.canvas.create_line(
                x, self.start_y - 10, x, self.start_y - 320,
                width=3, fill="gray60"
            )

            self.canvas.create_rectangle(
                x - 50, self.start_y - 10, x + 50, self.start_y,
                fill="#A9A9A9", outline="black", width=2
            )

            self.canvas.create_text(
                x, self.start_y + 15,
                text=str(spindle),
                font=("Arial", 10, "bold"),
                fill=self.text_color
            )

            disks = state.get(spindle, [])

            for disk_idx, diameter in enumerate(reversed(disks)):
                y = self.start_y - 10 - (disk_idx + 1) * self.disk_height

                if y < self.start_y - 320:
                    continue

                half_width = diameter / 2
                color = self.disk_colors.get(diameter, "#4169E1")

                self.canvas.create_rectangle(
                    x - half_width, y - self.disk_height,
                    x + half_width, y,
                    fill=color, outline="black", width=1
                )

                self.canvas.create_text(
                    x, y - self.disk_height / 2,
                    text=str(diameter),
                    font=("Arial", 6, "bold"),
                    fill="white"
                )

    def run(self):
        self.root.mainloop()


def main():
    root = tk.Tk()
    app = HanoiTowerGUI(root, "70210562")
    app.run()

if __name__ == "__main__":
    main()

