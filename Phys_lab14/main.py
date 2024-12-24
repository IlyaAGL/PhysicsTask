import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')


class RefractionPlotter:
    def __init__(self, epsilon1, epsilon2, angle_inc, e0):
        self.epsilon1 = epsilon1
        self.epsilon2 = epsilon2
        self.angle_inc = angle_inc
        self.e0 = e0
        self.x = None
        self.y_inc_E = None
        self.y_refr_E = None
        self.y_inc_D = None
        self.y_refr_D = None

    def _calculate_refraction(self):
        angle_inc_rad = np.radians(self.angle_inc)
        angle_refr_rad = np.arctan(np.tan(angle_inc_rad) * (self.epsilon1 / self.epsilon2))
        d_ratio = self.epsilon2 / self.epsilon1
        return angle_inc_rad, angle_refr_rad, d_ratio

    def _generate_data(self):
        angle_inc_rad, _, d_ratio = self._calculate_refraction()

        self.x = np.linspace(-2, 2, 100)

        self.y_inc_E = np.tan(angle_inc_rad) * self.x
        self.y_refr_E = np.tan(angle_inc_rad) * self.x

        self.y_inc_D = self.y_inc_E * d_ratio
        self.y_refr_D = self.y_refr_E * d_ratio

    def _create_plot(self):
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.axhline(0, color="k", linestyle="--", linewidth=1)

        ax.plot(self.x[self.x <= 0], self.y_inc_E[self.x <= 0], color="b", label="E в среде 1")
        ax.plot(self.x[self.x >= 0], self.y_refr_E[self.x >= 0], color="r", label="E в среде 2")

        ax.plot(self.x[self.x <= 0], self.y_inc_D[self.x <= 0], color="c", linestyle="--", label="D в среде 1")
        ax.plot(self.x[self.x >= 0], self.y_refr_D[self.x >= 0], color="m", linestyle="--", label="D в среде 2")

        ax.set_title("Преломление E и D на границе двух диэлектриков")
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.legend()
        ax.grid(True)

        return fig

    def plot(self):
        self._generate_data()
        fig = self._create_plot()
        plt.show()


def generate_plot(epsilon1, epsilon2, angle_inc, e0):
    plotter = RefractionPlotter(epsilon1, epsilon2, angle_inc, e0)
    plotter.plot()


class DielectricFieldSimulator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Преломление электрического поля на границе диэлектриков")
        self.geometry("600x500")
        self.config(background='#e0e0e0')
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.build_user_interface()

    def build_user_interface(self):
        header_frame = ttk.Frame(self, padding="15")
        header_frame.pack(fill=tk.X)

        main_content_frame = ttk.Frame(self, padding="20")
        main_content_frame.pack(fill=tk.BOTH, expand=True)

        footer_frame = ttk.Frame(self, padding="15")
        footer_frame.pack(fill=tk.X)

        title_label = ttk.Label(header_frame, text="Граничные условия на границе диэлектриков",
                                font=("Helvetica", 18, "bold"))
        title_label.pack()

        input_section = ttk.Frame(main_content_frame)
        input_section.pack(fill=tk.BOTH, expand=True)

        # Common inputs
        common_inputs_frame = ttk.Frame(input_section)
        common_inputs_frame.pack(pady=20)

        e0_label = ttk.Label(common_inputs_frame, text="Модуль напряженности E (В/м):")
        e0_label.grid(row=0, column=0, padx=10, pady=5)
        self.e0_entry = ttk.Entry(common_inputs_frame, width=12)
        self.e0_entry.grid(row=0, column=1, padx=10, pady=5)

        angle_label = ttk.Label(common_inputs_frame, text="Угол падения (в градусах):")
        angle_label.grid(row=1, column=0, padx=10, pady=5)
        self.angle_entry = ttk.Entry(common_inputs_frame, width=12)
        self.angle_entry.grid(row=1, column=1, padx=10, pady=5)

        medium_properties_frame = ttk.Frame(input_section)
        medium_properties_frame.pack(pady=20)

        initial_medium_label = ttk.Label(medium_properties_frame, text="Среда 1:",
                                         font=("Arial", 14, "bold"))
        initial_medium_label.grid(row=0, column=0, columnspan=2, padx=10, pady=5)

        epsilon1_label = ttk.Label(medium_properties_frame, text="ε_1 (Ф/м):")
        epsilon1_label.grid(row=1, column=0, padx=10, pady=5)
        self.epsilon1_entry = ttk.Entry(medium_properties_frame, width=12)
        self.epsilon1_entry.grid(row=1, column=1, padx=10, pady=5)

        final_medium_label = ttk.Label(medium_properties_frame, text="Среда 2:", font=("Arial", 14, "bold"))
        final_medium_label.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        epsilon2_label = ttk.Label(medium_properties_frame, text="ε_2 (Ф/м):")
        epsilon2_label.grid(row=3, column=0, padx=10, pady=5)
        self.epsilon2_entry = ttk.Entry(medium_properties_frame, width=12)
        self.epsilon2_entry.grid(row=3, column=1, padx=10, pady=5)

        simulate_button = ttk.Button(footer_frame, text="Построить график",
                                     command=self.validate_and_simulate)
        simulate_button.pack(pady=15)

    def validate_and_simulate(self):
        try:
            e0 = float(self.e0_entry.get())
            angle = float(self.angle_entry.get())
            epsilon1 = float(self.epsilon1_entry.get())
            epsilon2 = float(self.epsilon2_entry.get())

            if epsilon1 <= 0 or epsilon2 <= 0 or not (0 <= angle <= 90) or e0 <= 0:
                raise ValueError("Проверьте корректность входных данных!")

            generate_plot(epsilon1, epsilon2, angle, e0)

        except ValueError as e:
            messagebox.showerror("Ошибка ввода", str(e))


if __name__ == "__main__":
    app = DielectricFieldSimulator()
    app.mainloop()