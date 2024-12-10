import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox


def gravitational_potential(x, y, m, g):
    return m * g * y


def spring_potential(x, y, k):
    return 0.5 * k * (x ** 2 + y ** 2)


def weight_potential(x, y, weight):
    return weight * y


def unknown_potential(x, y, A, B, alpha, beta):
    return A * x ** alpha + B * y ** beta


class InitialWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Распределение потенциальной энергии')
        self.geometry('400x250')
        self.configure(bg='#ffffff')

        title_label = tk.Label(self, text='Какую силу выберете?', font=('Arial', 14, 'bold'), fg='#000000',
                               bg='#ffffff')
        title_label.pack(pady=15)

        self.force_var = tk.StringVar(value='spring')

        radio_style = {'fg': '#000000', 'bg': '#ffffff', 'font': ('Arial', 12)}
        self.spring_radio = tk.Radiobutton(self, text='Упругая сила', variable=self.force_var, value='spring',
                                           **radio_style)
        self.gravity_radio = tk.Radiobutton(self, text='Гравитационная сила', variable=self.force_var, value='gravity',
                                            **radio_style)
        self.weight_radio = tk.Radiobutton(self, text='Сила тяжести', variable=self.force_var, value='weight',
                                           **radio_style)
        self.unknown_radio = tk.Radiobutton(self, text='Добавить неизвестные силы', variable=self.force_var,
                                            value='unknown', **radio_style)

        self.spring_radio.pack(anchor='w', padx=20)
        self.gravity_radio.pack(anchor='w', padx=20)
        self.weight_radio.pack(anchor='w', padx=20)
        self.unknown_radio.pack(anchor='w', padx=20)

        self.next_button = tk.Button(self, text='Далее', command=self.check_and_proceed, bg='#ffffff', fg='#000000',
                                     font=('Arial', 12, 'bold'), padx=10, pady=5, borderwidth=1, relief='solid')
        self.next_button.pack(pady=20)

    def check_and_proceed(self):
        choice = self.force_var.get()
        if choice == '':
            messagebox.showerror('Ошибка', 'Пожалуйста, выберите одну из сил.')
        else:
            self.data_window = DataWindow(choice)
            self.data_window.mainloop()
            self.destroy()


class DataWindow(tk.Tk):
    def __init__(self, choice):
        super().__init__()
        self.title('Ввод данных для выбранной силы')
        if choice in ['spring', 'gravity', 'weight']:
            self.geometry('500x250')
        else:
            self.geometry('500x450')
        self.configure(bg='#ffffff')
        self.choice = choice
        self.entries = {}
        if self.choice == 'spring':
            self.create_input_field('Коэффициент упругости k (Н/м):', 'spring')
        elif self.choice == 'gravity':
            self.create_input_field('Масса для гравитационного поля (кг):', 'gravity_mass')
            self.create_input_field('Ускорение свободного падения (м/c^2):', 'gravity_g')
        elif self.choice == 'weight':
            self.create_input_field('Сила тяжести (Н):', 'weight')
        elif self.choice == 'unknown':
            explanation_label = tk.Label(self, text='Формула неизвестной силы: F = Ax^α + By^β', font=('Arial', 12),
                                         fg='#000000', bg='#ffffff')
            explanation_label.pack(pady=10)
            self.create_input_field('Количество неизвестных сил:', 'unknown_count')
            self.add_unknown_forces_button = tk.Button(self, text='Добавить неизвестные силы',
                                                       command=self.add_unknown_forces, bg='#ffffff', fg='#000000',
                                                       font=('Arial', 12, 'bold'), padx=10, pady=5, borderwidth=1,
                                                       relief='solid')
            self.add_unknown_forces_button.pack(pady=10)

        self.run_button = tk.Button(self, text='Показать распределение', command=self.run_simulation, bg='#ffffff',
                                    fg='#000000', font=('Arial', 12, 'bold'), padx=10, pady=5, borderwidth=1,
                                    relief='solid')
        self.run_button.pack(pady=20)

    def create_input_field(self, label_text, key):
        frame = tk.Frame(self, bg='#ffffff')
        frame.pack(pady=5, fill='x')
        label = tk.Label(frame, text=label_text, font=('Arial', 12), fg='#000000', bg='#ffffff')
        label.pack(side='left', padx=5)
        entry = tk.Entry(frame, width=25, font=('Arial', 10))
        entry.pack(side='right', padx=5)
        self.entries[key] = entry

    def add_unknown_forces(self):
        try:
            count = int(self.entries['unknown_count'].get())
            for i in range(count):
                self.create_input_field(f'Коэффициент A для неизвестной силы {i + 1}:', f'unknown_A_{i}0')
                self.create_input_field(f'Коэффициент B для неизвестной силы {i + 1}:', f'unknown_B_{i}0')
                self.create_input_field(f'Степень для x (alpha) для силы {i + 1}:', f'unknown_alpha_{i}0')
                self.create_input_field(f'Степень для y (beta) для силы {i + 1}:', f'unknown_beta_{i}0')
            self.add_unknown_forces_button.config(state='disabled')
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректное количество неизвестных сил.')

    def run_simulation(self):
        try:
            choice = self.choice
            if choice == 'spring':
                k = float(self.entries['spring'].get())
                self.calculate_potential([('spring', k)], [])
            elif choice == 'gravity':
                m = float(self.entries['gravity_mass'].get())
                g = float(self.entries['gravity_g'].get())
                self.calculate_potential([('gravity', m, g)], [])
            elif choice == 'weight':
                weight = float(self.entries['weight'].get())
                self.calculate_potential([('weight', weight)], [])
            elif choice == 'unknown':
                unknown_forces = []
                count = int(self.entries['unknown_count'].get())
                for i in range(count):
                    A = float(self.entries[f'unknown_A_{i}0'].get())
                    B = float(self.entries[f'unknown_B_{i}0'].get())
                    alpha = int(self.entries[f'unknown_alpha_{i}0'].get())
                    beta = int(self.entries[f'unknown_beta_{i}0'].get())
                    unknown_forces.append((A, B, alpha, beta))
                self.calculate_potential([], unknown_forces)
        except ValueError:
            messagebox.showerror('Ошибка', 'Введите корректные числовые значения.')

    def calculate_potential(self, choices, unknown_forces):
        x = np.linspace(-10, 10, 100)
        y = np.linspace(-10, 10, 100)
        X, Y = np.meshgrid(x, y)
        total_potential = np.zeros_like(X)
        for choice in choices:
            if choice[0] == 'spring':
                k = choice[1]
                total_potential += spring_potential(X, Y, k)
            elif choice[0] == 'gravity':
                m, g = choice[1], choice[2]
                total_potential += gravitational_potential(X, Y, m, g)
            elif choice[0] == 'weight':
                weight = choice[1]
                total_potential += weight_potential(X, Y, weight)
        for force in unknown_forces:
            A, B, alpha, beta = force
            total_potential += unknown_potential(X, Y, A, B, alpha, beta)
        plt.figure()
        cp = plt.contourf(X, Y, total_potential, cmap='plasma')
        plt.colorbar(cp)
        plt.title('Поле потенциальной энергии')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.show()


app = InitialWindow()
app.mainloop()