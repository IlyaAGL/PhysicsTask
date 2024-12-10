import math
import matplotlib.pyplot as plt
import matplotlib
import numpy as np

matplotlib.use('Qt5Agg')

g = 9.81


def trajectory_parameters(h, v0, angle):
    if angle == 90:
        v0x = 0
    else:
        v0x = v0 * math.cos(angle * math.pi / 180)
    v0y = v0 * math.sin(angle * math.pi / 180)

    trajectory = (v0y + math.sqrt(v0y ** 2 + 2 * g * h)) / g

    t = np.linspace(0, trajectory, num=500)

    x = v0x * t
    y = h + v0y * t - 0.5 * g * t ** 2

    v_x = v0x * np.ones_like(t)
    v_y = v0y - g * t
    v = np.sqrt(v_x ** 2 + v_y ** 2)

    plt.figure()
    trajectory_graph(x, y)
    plt.figure()
    speed_time_graph(t, v)
    plt.figure()
    coords_graph(t, x, y)
    plt.show()


def trajectory_graph(x, y):
    plt.plot(x, y)
    plt.title('Траектория движения тела')
    plt.xlabel('x (м)')
    plt.ylabel('y (м)')
    plt.grid(True)


def speed_time_graph(t, v):
    plt.plot(t, v)
    plt.title('Зависимость скорости от времени')
    plt.xlabel('t (с)')
    plt.ylabel('v (м/с)')
    plt.grid(True)


def coords_graph(t, x, y):
    plt.plot(t, x, label='x (горизонтальная координата)')
    plt.plot(t, y, label='y (вертикальная координата)')
    plt.title('Зависимость координат от времени')
    plt.xlabel('t (с)')
    plt.ylabel('Координаты (м)')
    plt.legend()
    plt.grid(True)
