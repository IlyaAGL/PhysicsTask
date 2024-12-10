import tkinter as tk
from tkinter import messagebox
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

matplotlib.use('Qt5Agg')

class ChargeFieldSimulator:
    def __init__(self, root, plot_callback):
        self.root = root
        self.root.title('Электростатическое поле')
        self.root.geometry('300x150')
        self.root.resizable(False, False)
        self.plot_callback = plot_callback
        self.main_frame = tk.Frame(self.root, bg='#f0f0f0')
        self.main_frame.pack(fill='both', expand=True)
        self.header_label = tk.Label(self.main_frame, text='Введите количество зарядов', font=('Arial', 14, 'bold'), fg='#000000', bg='#f0f0f0')
        self.header_label.grid(row=0, column=0, columnspan=2, pady=10)
        self.num_qs_label = tk.Label(self.main_frame, text='Количество зарядов:', font=('Arial', 12), bg='#f0f0f0')
        self.num_qs_input = tk.Entry(self.main_frame, width=10)
        self.num_qs_label.grid(row=1, column=0, padx=5, pady=5)
        self.num_qs_input.grid(row=1, column=1, padx=5, pady=5)
        self.add_qs_button = tk.Button(self.main_frame, text='Начать вводить данные зарядов', command=self.create_charge_inputs, bg='#000000', fg='white', font=('Arial', 10))
        self.add_qs_button.grid(row=2, column=0, columnspan=2, pady=10)
        self.charge_entries = []

    def create_charge_inputs(self):
        try:
            num_qs = int(self.num_qs_input.get())
            if num_qs <= 0:
                raise ValueError('Введите целое положительное число зарядов.')
            self.qs_window = tk.Toplevel(self.root)
            self.qs_window.title('Ввод данных о зарядах')
            self.qs_window.geometry('430x400')
            self.qs_window.resizable(False, False)
            qs_frame = tk.Frame(self.qs_window, bg='#f0f0f0')
            qs_frame.pack(fill='both', expand=True)
            self.simulate_button = tk.Button(qs_frame, text='Показать поле', command=lambda: self.simulation(), bg='#000000', fg='white', font=('Arial', 12))
            self.simulate_button.grid(row=0, column=0, columnspan=7, pady=10)
            range_label = tk.Label(qs_frame, text='-10 <= x <= 10 и -10 <= y <= 10', font=('Arial', 10), bg='#f0f0f0', fg='red')
            range_label.grid(row=1, column=0, columnspan=7, pady=5)
            for i in range(num_qs):
                label = tk.Label(qs_frame, text=f'Заряд {i + 1}:', font=('Arial', 12), bg='#f0f0f0')
                x_input = tk.Entry(qs_frame, width=8)
                y_input = tk.Entry(qs_frame, width=8)
                q_input = tk.Entry(qs_frame, width=8)
                label.grid(row=i + 2, column=0, padx=5, pady=5)
                tk.Label(qs_frame, text='x (м):', font=('Arial', 12), bg='#f0f0f0').grid(row=i + 2, column=1, padx=5, pady=5)
                x_input.grid(row=i + 2, column=2, padx=5, pady=5)
                tk.Label(qs_frame, text='y (м):', font=('Arial', 12), bg='#f0f0f0').grid(row=i + 2, column=3, padx=5, pady=5)
                y_input.grid(row=i + 2, column=4, padx=5, pady=5)
                tk.Label(qs_frame, text='q (Кл):', font=('Arial', 12), bg='#f0f0f0').grid(row=i + 2, column=5, padx=5, pady=5)
                q_input.grid(row=i + 2, column=6, padx=5, pady=5)
                self.charge_entries.append({'x': x_input, 'y': y_input, 'q': q_input})
        except ValueError as e:
            messagebox.showerror('Ошибка', str(e))

    def simulation(self):
        qs = []
        try:
            for i, entry in enumerate(self.charge_entries):
                x = float(entry['x'].get())
                y = float(entry['y'].get())
                q = float(entry['q'].get())
                if not (-10 <= x <= 10 and -10 <= y <= 10):
                    raise ValueError(f'Координаты заряда {i + 1} должны быть в пределах от -10 до 10.')
                qs.append({'q': q, 'pos': (x, y), 'color': 'blue'})

            self.plot_callback(qs)
        except ValueError as e:
            messagebox.showerror('Ошибка', str(e))

def plot_field(charges):
    x = np.linspace((-10), 10, 300)
    y = np.linspace((-10), 10, 300)
    X, Y = np.meshgrid(x, y)
    E_x = np.zeros(X.shape)
    E_y = np.zeros(Y.shape)
    for charge in charges:
        q = charge['q']
        x0, y0 = charge['pos']
        rx = X - x0
        ry = Y - y0
        r = np.sqrt(rx ** 2 + ry ** 2)
        r[r == 0] = 1e-09
        E_x += q * rx / r ** 3
        E_y += q * ry / r ** 3
    E = np.sqrt(E_x ** 2 + E_y ** 2)
    E_x /= E
    E_y /= E
    plt.figure(figsize=(10, 8))
    plt.streamplot(X, Y, E_x, E_y, color=np.log(E + 1), linewidth=1.5, cmap='hsv', density=2.0)
    plt.colorbar(label='Величина электрического поля')
    for charge in charges:
        x0, y0 = charge['pos']
        plt.scatter(x0, y0, color=charge['color'], s=200, edgecolor='black')
    plt.title('Электростатическое поле введенных зарядов')
    plt.xlabel('x, (м)')
    plt.ylabel('y, (м)')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    root = tk.Tk()
    window = ChargeFieldSimulator(root, plot_callback=plot_field)
    root.mainloop()
