import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use("Qt5Agg")

CONSTANT_ELECTROSTATIC = 8.98755e9

class ElectriclVisualizer:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Визуализация электрического потенциала")
        self.main_window.geometry("900x700")

        self.tab_container = ttk.Notebook(self.main_window)
        self.tab_container.pack(fill=tk.BOTH, expand=True)

        self.point_charge_tab = ttk.Frame(self.tab_container)
        self.polarized_particle_tab = ttk.Frame(self.tab_container)
        self.visualization_tab = ttk.Frame(self.tab_container)

        self.tab_container.add(self.point_charge_tab, text="Точечные заряды")
        self.tab_container.add(self.polarized_particle_tab, text="Диполи")
        self.tab_container.add(self.visualization_tab, text="Визуализация")

        self.setup_user_interface()

    def setup_user_interface(self):
        point_charge_frame = ttk.Frame(self.point_charge_tab)
        point_charge_frame.pack(fill=tk.X, padx=15, pady=15)

        add_point_charge_button = ttk.Button(point_charge_frame, text="Добавить точечный заряд", command=self.add_point_charge_input)
        add_point_charge_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.point_charge_entries = []

        polarized_particle_frame = ttk.Frame(self.polarized_particle_tab)
        polarized_particle_frame.pack(fill=tk.X, padx=15, pady=15)

        add_polarized_particle_button = ttk.Button(polarized_particle_frame, text="Добавить диполь", command=self.add_polarized_particle_input)
        add_polarized_particle_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.polarized_particle_entries = []

        visualization_frame = ttk.Frame(self.visualization_tab)
        visualization_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)

        visualize_button = ttk.Button(visualization_frame, text="Вывести электростатическое поле", command=self.generate_visualization)
        visualize_button.pack(side=tk.TOP, fill=tk.X)

        self.visualization_output = tk.Text(visualization_frame, height=25)
        self.visualization_output.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

    def add_point_charge_input(self):
        point_charge_frame = ttk.Frame(self.point_charge_tab)
        point_charge_frame.pack(fill=tk.X, padx=15, pady=7)

        x_label = ttk.Label(point_charge_frame, text="x (м):")
        x_label.pack(side=tk.LEFT)
        x_entry = ttk.Entry(point_charge_frame)
        x_entry.pack(side=tk.LEFT)

        y_label = ttk.Label(point_charge_frame, text="y (м):")
        y_label.pack(side=tk.LEFT)
        y_entry = ttk.Entry(point_charge_frame)
        y_entry.pack(side=tk.LEFT)

        charge_label = ttk.Label(point_charge_frame, text="Заряд (Кл):")
        charge_label.pack(side=tk.LEFT)
        charge_entry = ttk.Entry(point_charge_frame)
        charge_entry.pack(side=tk.LEFT)

        self.point_charge_entries.append((point_charge_frame, x_entry, y_entry, charge_entry))

    def add_polarized_particle_input(self):
        polarized_particle_frame = ttk.Frame(self.polarized_particle_tab)
        polarized_particle_frame.pack(fill=tk.X, padx=15, pady=7)

        x_label = ttk.Label(polarized_particle_frame, text="x (м):")
        x_label.pack(side=tk.LEFT)
        x_entry = ttk.Entry(polarized_particle_frame)
        x_entry.pack(side=tk.LEFT)

        y_label = ttk.Label(polarized_particle_frame, text="y (м):")
        y_label.pack(side=tk.LEFT)
        y_entry = ttk.Entry(polarized_particle_frame)
        y_entry.pack(side=tk.LEFT)

        moment_label = ttk.Label(polarized_particle_frame, text="Момент диполя (Кл*м):")
        moment_label.pack(side=tk.LEFT)
        moment_entry = ttk.Entry(polarized_particle_frame)
        moment_entry.pack(side=tk.LEFT)

        angle_label = ttk.Label(polarized_particle_frame, text="Угол ориентации (в градусах):")
        angle_label.pack(side=tk.LEFT)
        angle_entry = ttk.Entry(polarized_particle_frame)
        angle_entry.pack(side=tk.LEFT)

        self.polarized_particle_entries.append((polarized_particle_frame, x_entry, y_entry, moment_entry, angle_entry))

    def generate_visualization(self):
        point_charges = []
        for _, x_entry, y_entry, charge_entry in self.point_charge_entries:
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                charge = float(charge_entry.get())
                point_charges.append((x, y, charge))
            except ValueError as e:
                messagebox.showerror('Ошибка ввода', str(e))

        polarized_particles = []
        for _, x_entry, y_entry, moment_entry, angle_entry in self.polarized_particle_entries:
            try:
                x = float(x_entry.get())
                y = float(y_entry.get())
                moment = float(moment_entry.get())
                angle = np.radians(float(angle_entry.get()))
                polarized_particles.append((x, y, moment, angle))
            except ValueError as e:
                messagebox.showerror('Ошибка ввода', str(e))

        if point_charges or polarized_particles:
            self.display_electric_field(point_charges, polarized_particles)
        else:
            messagebox.showerror('Ошибка', "Не хватает входных данных.")

    def compute_electric_field(self, point_charges, polarized_particles):
        x_range = np.linspace(-6, 6, 120)
        y_range = np.linspace(-6, 6, 120)
        X, Y = np.meshgrid(x_range, y_range)
        electric_field_x = np.zeros_like(X)
        electric_field_y = np.zeros_like(Y)
        potential = np.zeros_like(X)

        for x_c, y_c, charge in point_charges:
            distance = np.sqrt((X - x_c) ** 2 + (Y - y_c) ** 2)
            unit_vector_x = (X - x_c) / distance
            unit_vector_y = (Y - y_c) / distance
            distance[distance == 0] = np.inf
            electric_field_x += CONSTANT_ELECTROSTATIC * charge * unit_vector_x / distance ** 2
            electric_field_y += CONSTANT_ELECTROSTATIC * charge * unit_vector_y / distance ** 2
            potential += CONSTANT_ELECTROSTATIC * charge / distance

        for x_d, y_d, moment, theta in polarized_particles:
            distance = np.sqrt((X - x_d) ** 2 + (Y - y_d) ** 2)
            unit_vector_x = (X - x_d) / distance
            unit_vector_y = (Y - y_d) / distance
            distance[distance == 0] = np.inf

            moment_x = moment * np.cos(theta)
            moment_y = moment * np.sin(theta)

            dot_product = moment_x * unit_vector_x + moment_y * unit_vector_y

            electric_field_x += CONSTANT_ELECTROSTATIC * (3 * dot_product * unit_vector_x - moment_x) / distance ** 3
            electric_field_y += CONSTANT_ELECTROSTATIC * (3 * dot_product * unit_vector_y - moment_y) / distance ** 3

        return X, Y, electric_field_x, electric_field_y, potential

    def calculate_torque_on_dipole(self, dipole, electric_field_x, electric_field_y, X, Y):
        x, y, moment, theta = dipole
        index_x = (np.abs(X[0] - x)).argmin()
        index_y = (np.abs(Y[:, 0] - y)).argmin()

        electric_field_at_dipole = np.array([electric_field_x[index_y, index_x], electric_field_y[index_y, index_x]])
        moment_vector = np.array([moment * np.cos(theta), moment * np.sin(theta)])

        force = electric_field_at_dipole * moment
        torque = np.cross(moment_vector, electric_field_at_dipole)
        return force, torque

    def display_electric_field(self, point_charges, polarized_particles):
        X, Y, electric_field_x, electric_field_y, potential = self.compute_electric_field(point_charges, polarized_particles)

        figure, axis = plt.subplots(figsize=(10, 8))
        axis.quiver(X, Y, electric_field_x, electric_field_y, color='red', pivot='middle', scale=1e10, width=0.005, label='Электростатическое поле')
        axis.streamplot(X, Y, electric_field_x, electric_field_y, color=np.sqrt(electric_field_x ** 2 + electric_field_y ** 2), cmap="plasma", density=1.5, linewidth=1)

        kontur = axis.contour(X, Y, potential, levels=25, colors="red", linewidths=0.5)
        axis.clabel(kontur, inline=1, fontsize=8, fmt="%.1e")

        filled_contour = axis.contourf(X, Y, potential, levels=100, cmap="RdYlBu", alpha=0.8)
        plt.colorbar(filled_contour, label="Электрический потенциал (В)")

        results = []

        for dipole in polarized_particles:
            x, y, moment, theta = dipole
            force, torque = self.calculate_torque_on_dipole(dipole, electric_field_x, electric_field_y, X, Y)
            axis.arrow(x, y, 0.2 * np.cos(theta), 0.2 * np.sin(theta), head_width=0.1, color='white', label='Диполь')
            results.append(f"Частица в ({x:.1f}, {y:.1f}): Сила = {force}, Момент = {torque:.2e}")

        axis.set_title("Электрическое поле с диполями")
        axis.set_xlabel("X, м")
        axis.set_ylabel("Y, м")
        axis.legend(loc='lower left')

        plt.show()

        self.visualization_output.delete(1.0, tk.END)
        self.visualization_output.insert(tk.END, "\n".join(results))

    def start_application(self):
        self.main_window.mainloop()

if __name__ == "__main__":
    visualizer = ElectriclVisualizer()
    visualizer.start_application()