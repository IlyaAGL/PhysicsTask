import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

K_E = 8.99e9


class ElectrostaticFieldVisualizer:
    def __init__(self, main_window):
        self.main_window = main_window
        self.main_window.title("Электростатическое поле точечных зарядов")
        self.main_window.geometry("300x500")

        self.header_frame = tk.Frame(main_window)
        self.input_frame = tk.Frame(main_window)

        self.header_frame.pack(fill=tk.X, padx=10, pady=10)
        self.input_frame.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.btn_add_charge = tk.Button(self.header_frame, text="Добавить заряд", command=self.create_charge_input)
        self.btn_visualize = tk.Button(self.header_frame, text="Визуализировать поле", command=self.compute_field)

        self.btn_add_charge.pack(side=tk.LEFT, padx=5)
        self.btn_visualize.pack(side=tk.LEFT, padx=5)

        self.charge_inputs_frame = tk.Frame(self.input_frame)
        self.charge_inputs_frame.pack(expand=True, fill=tk.BOTH)

        self.charge_entries = []
        self.create_charge_input()
        self.separator = ttk.Separator(self.charge_inputs_frame, orient='horizontal')
        self.separator.pack(fill=tk.X, pady=10)

    def create_charge_input(self):
        charge_entry_frame = tk.Frame(self.charge_inputs_frame)
        charge_entry_frame.pack(pady=5, fill=tk.X)

        label_x = tk.Label(charge_entry_frame, text="x, м:")
        label_x.grid(row=0, column=0, padx=5, pady=5)
        entry_x = tk.Entry(charge_entry_frame)
        entry_x.grid(row=0, column=1, padx=5, pady=5)

        label_y = tk.Label(charge_entry_frame, text="y, м:")
        label_y.grid(row=1, column=0, padx=5, pady=5)
        entry_y = tk.Entry(charge_entry_frame)
        entry_y.grid(row=1, column=1, padx=5, pady=5)

        label_q = tk.Label(charge_entry_frame, text="q, Кл:")
        label_q.grid(row=2, column=0, padx=5, pady=5)
        entry_q = tk.Entry(charge_entry_frame)
        entry_q.grid(row=2, column=1, padx=5, pady=5)

        self.charge_entries.append((entry_x, entry_y, entry_q))

        if len(self.charge_entries) > 1:
            self.separator = ttk.Separator(self.charge_inputs_frame, orient='horizontal')
            self.separator.pack(fill=tk.X, pady=10)

    def compute_field(self):
        charge_data = []
        for entry_x, entry_y, entry_q in self.charge_entries:
            try:
                x = float(entry_x.get())
                y = float(entry_y.get())
                q = float(entry_q.get())
                charge_data.append((x, y, q))
            except ValueError:
                messagebox.showerror("Ошибка ввода", "Неправильный формат ввода.")
                return

        if charge_data:
            X, Y, E_x, E_y, potential = self.calculate_field_values(charge_data)
            self.display_field(X, Y, E_x, E_y, potential)

    @staticmethod
    def calculate_field_values(charges):
        x_bounds = (-10, 10)
        y_bounds = (-10, 10)
        resolution = 100

        x_values = np.linspace(*x_bounds, resolution)
        y_values = np.linspace(*y_bounds, resolution)
        X, Y = np.meshgrid(x_values, y_values)
        E_x = np.zeros_like(X)
        E_y = np.zeros_like(Y)
        potential = np.zeros_like(X)

        for x_charge, y_charge, charge in charges:
            distance = np.sqrt((X - x_charge) ** 2 + (Y - y_charge) ** 2)
            unit_vector_x = (X - x_charge) / distance
            unit_vector_y = (Y - y_charge) / distance
            distance[distance == 0] = np.inf
            E_x += K_E * charge * unit_vector_x / distance ** 2
            E_y += K_E * charge * unit_vector_y / distance ** 2
            potential += K_E * charge / distance

        return X, Y, E_x, E_y, potential

    def display_field(self, X, Y, E_x, E_y, potential):
        figure, axis = plt.subplots(figsize=(8, 6))

        axis.quiver(X, Y, E_x, E_y, color='blue', pivot='middle', scale=1e12, width=0.002, label='Векторное поле')
        axis.streamplot(X, Y, E_x, E_y, color=np.sqrt(E_x ** 2 + E_y ** 2), cmap="viridis", density=1.5, linewidth=1)

        contour_lines = axis.contour(X, Y, potential, levels=20, colors="black", linewidths=1)
        axis.clabel(contour_lines, inline=1, fontsize=8, fmt="%.1e")

        filled_contours = axis.contourf(X, Y, potential, levels=50, cmap="RdYlBu", alpha=0.8)
        plt.colorbar(filled_contours, label="Потенциал (В)")

        axis.set_title("Электростатическое поле")
        axis.set_xlabel("x, м")
        axis.set_ylabel("y, м")

        axis.set_xlim(*(-10, 10))
        axis.set_ylim(*(-10, 10))
        axis.xaxis.set_ticks(np.arange(-10, 11, 2))
        axis.yaxis.set_ticks(np.arange(-10, 11, 2))
        axis.grid(True, linestyle='--', alpha=0.7)

        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    app = ElectrostaticFieldVisualizer(root)
    root.mainloop()
