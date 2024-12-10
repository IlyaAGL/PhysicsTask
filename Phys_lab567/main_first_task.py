import numpy as np
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

# Константы
g = 9.81  # ускорение свободного падения, м/с^2


# Функция для вычисления производных
def equations(t, y, k):
    x, vx, y_pos, vy = y
    v = np.sqrt(vx ** 2 + vy ** 2)
    # Уравнения движения
    dxdt = vx
    dvxdt = -k * v * vx
    dydt = vy
    dvydt = -g - k * v * vy
    return np.array([dxdt, dvxdt, dydt, dvydt])


# Функция для проверки, является ли строка положительным числом
def is_positive_number(value):
    try:
        num = float(value)
        return num > 0
    except ValueError:
        return False


# Функция для запуска расчетов и построения графиков
def calculate_and_plot():
    # Проверка всех полей ввода
    if not (is_positive_number(v0_entry.get()) and
            is_positive_number(angle_entry.get()) and
            is_positive_number(h0_entry.get()) and
            is_positive_number(k_entry.get())):
        messagebox.showerror("Ошибка ввода", "Пожалуйста, введите положительные числовые значения.")
        return

    v0 = float(v0_entry.get())
    angle = float(angle_entry.get())
    h0 = float(h0_entry.get())
    k = float(k_entry.get())

    # Перевод угла в радианы
    angle_rad = np.radians(angle)

    # Начальные условия
    vx0 = v0 * np.cos(angle_rad)  # начальная горизонтальная скорость
    vy0 = v0 * np.sin(angle_rad)  # начальная вертикальная скорость
    y0 = np.array([0, vx0, h0, vy0])  # [x, vx, y, vy]

    # Время моделирования
    t_span = 10  # общее время моделирования (с)
    dt = 0.01  # шаг времени (с)
    num_steps = int(t_span / dt)  # количество шагов

    # Массивы для хранения результатов
    x_vals = np.zeros(num_steps)
    y_vals = np.zeros(num_steps)
    v_vals = np.zeros(num_steps)
    t_vals = np.linspace(0, t_span, num_steps)

    # Начальные условия
    x_vals[0], y_vals[0] = y0[0], y0[2]
    vx, vy = y0[1], y0[3]
    v_vals[0] = np.sqrt(vx ** 2 + vy ** 2)  # Установка начальной скорости

    # Метод Эйлера
    for i in range(1, num_steps):
        t = i * dt
        dydt = equations(t, y0, k)

        # Обновление значений
        y0 += dydt * dt
        x_vals[i] = y0[0]
        y_vals[i] = y0[2]
        vx, vy = y0[1], y0[3]
        v_vals[i] = np.sqrt(vx ** 2 + vy ** 2)  # Обновление скорости

    # Включение интерактивного режима
    plt.ion()

    # Визуализация: Траектория движения
    plt.figure()
    plt.plot(x_vals, y_vals)
    plt.title('Траектория движения тела')
    plt.xlabel('x (м)')
    plt.ylabel('y (м)')
    plt.grid(True)


    # Визуализация: Зависимость скорости от времени
    plt.figure()
    plt.plot(t_vals, v_vals)
    plt.title('Зависимость скорости от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Скорость (м/с)')
    plt.grid(True)

    # Установка делений по вертикальной оси с шагом 5
    plt.yticks(np.arange(0, max(v_vals) + 5, 5))  # Установим деления с шагом 5

    # Визуализация: Зависимость координат x и y от времени
    plt.figure()
    plt.plot(t_vals, x_vals, label='x (м)')
    plt.plot(t_vals, y_vals, label='y (м)')
    plt.title('Зависимость координат от времени')
    plt.xlabel('Время (с)')
    plt.ylabel('Координаты (м)')
    plt.legend()
    plt.grid(True)

    # Показываем все графики
    plt.show()


# Создание основного окна
root = tk.Tk()
root.title("Расчет траектории движения тела")

# Создание меток и полей ввода
tk.Label(root, text="Начальная скорость (м/с):").grid(row=0, column=0)
v0_entry = tk.Entry(root)
v0_entry.grid(row=0, column=1)

tk.Label(root, text="Угол броска (градусы):").grid(row=1, column=0)
angle_entry = tk.Entry(root)
angle_entry.grid(row=1, column=1)

tk.Label(root, text="Начальная высота (м):").grid(row=2, column=0)
h0_entry = tk.Entry(root)
h0_entry.grid(row=2, column=1)

tk.Label(root, text="Коэффициент сопротивления среды:").grid(row=3, column=0)
k_entry = tk.Entry(root)
k_entry.grid(row=3, column=1)

# Кнопка для запуска расчета
calculate_button = tk.Button(root, text="Рассчитать и построить графики", command=calculate_and_plot)
calculate_button.grid(row=4, columnspan=2)

# Запуск основного цикла
root.mainloop()