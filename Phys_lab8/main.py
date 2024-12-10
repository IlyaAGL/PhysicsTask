import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import tkinter as tk
from tkinter import messagebox

matplotlib.use("Qt5Agg")

def calculate_and_plot():
    try:
        mass = float(mass_entry.get())
        spring_constant = float(spring_constant_entry.get())
        damping_coefficient = float(damping_coefficient_entry.get())

        if mass <= 0 or spring_constant <= 0 or damping_coefficient <= 0:
            raise ValueError('Введенные значения должны быть положительными.')

        initial_amplitude = 1.0
        initial_velocity = 0.0
        max_time = 10
        time_step = 0.01
        time_array = np.arange(0, max_time, time_step)
        natural_frequency = np.sqrt(spring_constant / mass)
        damping_ratio = damping_coefficient / (2 * mass)

        def calculate_position(t):
            if damping_ratio < natural_frequency:
                damped_frequency = np.sqrt(natural_frequency**2 - damping_ratio**2)
                return initial_amplitude * np.exp(-damping_ratio * t) * np.cos(damped_frequency * t)
            return initial_amplitude * np.exp(-damping_ratio * t)

        position_values = calculate_position(time_array)
        velocity_values = np.gradient(position_values, time_step)
        kinetic_energy = 0.5 * mass * velocity_values**2
        potential_energy = 0.5 * spring_constant * position_values**2
        total_energy = kinetic_energy + potential_energy

        plt.figure(figsize=(10, 8))
        plt.subplot(3, 1, 1)
        plt.plot(time_array, kinetic_energy, label='Кинетическая энергия (KE)')
        plt.xlabel('Время (с)')
        plt.ylabel('Энергия (Дж)')
        plt.legend()
        plt.grid(True)

        plt.subplot(3, 1, 2)
        plt.plot(time_array, potential_energy, label='Потенциальная энергия (PE)', color='orange')
        plt.xlabel('Время (с)')
        plt.ylabel('Энергия (Дж)')
        plt.legend()
        plt.grid(True)

        plt.subplot(3, 1, 3)
        plt.plot(time_array, total_energy, label='Полная механическая энергия (TE)', color='green')
        plt.xlabel('Время (с)')
        plt.ylabel('Энергия (Дж)')
        plt.legend()
        plt.grid(True)

        plt.tight_layout()
        plt.show()

    except ValueError as e:
        messagebox.showerror('Ошибка ввода', str(e))

root = tk.Tk()
root.title('Расчет механической энергии системы')

tk.Label(root, text='Масса груза (кг):').grid(row=0, column=0)
mass_entry = tk.Entry(root)
mass_entry.grid(row=0, column=1)

tk.Label(root, text='Коэффициент жесткости пружины (Н/м):').grid(row=1, column=0)
spring_constant_entry = tk.Entry(root)
spring_constant_entry.grid(row=1, column=1)

tk.Label(root, text='Коэффициент сопротивления среды:').grid(row=2, column=0)
damping_coefficient_entry = tk.Entry(root)
damping_coefficient_entry.grid(row=2, column=1)

calculate_button = tk.Button(root, text='Рассчитать и построить графики', command=calculate_and_plot)
calculate_button.grid(row=3, columnspan=2)

root.mainloop()