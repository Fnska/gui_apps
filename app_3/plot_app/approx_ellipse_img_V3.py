import numpy as np
import scipy.optimize
from math import pi, sqrt

from PIL import Image
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
"""
Аппроксимация эллипсом V3 с тем приближением что нет поворотов и занулены коэфффициенты D и E в канноническом уравнении.
np.set_printoptions(threshold=np.nan) - для полной выписки массива точек
"""


def el_im_app(im, MAX, file_path, low_value_i_sub=11503, delta_ring=5000, deletes_point=75, B_0=0, J=1, points_plot=0, update=0):
    """
    Определяем функию, которая будет возвращать объект изображения эллипса
    Параметры:  im - объект Image.open("./path/to/file_name.png").convert("I")
                MAX - int/float, верхний уровень интенсивности кольца
                level_crop - int/float, ширина кольца от верхнего уровня
                deletes_point - int, кол-во удаленных точек сверху
                B_0 - float, влияет на экцентриситет 0 - окружность, 1 - эллипс
                J - int, уменьшение по оси Y эллипса в n раз
                points_plot - bool, влючает/отключает точечный график
    """
    a = np.array(im)
    a = a[::J]
    a[a > MAX] = 0
    a[a < MAX - delta_ring] = 0
    b = np.nonzero(a)
    xs = b[1]
    ys = b[0]
    index = [i for i in range(deletes_point)]
    xs = np.delete(xs, index)
    ys = np.delete(ys, index)

    x0 = sum(xs) / len(xs)
    y0 = sum(ys) / len(ys)
    R = 1

    def fit_func1(x):
        return sum(((xs - x[0])**2 + (ys - x[1])**2 - x[2])**2)

    result1 = scipy.optimize.fmin(func=fit_func1, x0=[x0, y0, R], disp=0)

    x0 = result1[0]
    y0 = result1[1]

    A = 1
    B = B_0
    C = 1
    D = 0
    E = 0
    F = result1[2]

    def fit_func2(x):
        return sum((A * (xs - x[0])**2 + B * (xs - x[0]) * (ys - x[1]) + C * (ys - x[1])**2 - F)**2)

    result = scipy.optimize.fmin(func=fit_func2, x0=[x0, y0, A, B, C, F], disp=0)

    x0 = result[0]
    y0 = result[1]

    A = result[2]
    B = result[3]
    C = result[4]
    D = 0
    E = 0
    F = result[5]

    M_0 = np.matrix([[F, D / 2, E / 2], [D / 2, A, B / 2], [E / 2, B / 2, C]])
    M = np.matrix([[A, B / 2], [B / 2, C]])

    LA = np.linalg.eig(M)
    lam1 = LA[0][0]
    lam2 = LA[0][1]

    u = result[0]
    v = result[1]
    x_a = sqrt(np.linalg.det(M_0) / np.linalg.det(M) * lam1)
    y_b = sqrt(np.linalg.det(M_0) / np.linalg.det(M) * lam2) / J
    exs = sqrt(abs(1 - y_b**2 / (x_a**2)))
    p = y_b**2 / x_a
    c = x_a * exs
    r_p = x_a * (1 - exs)
    r_a = x_a * (1 + exs)

    out_results = [["Верхняя интенсивность", "I", MAX],
                   ["Нижняя интенсивность", "I_SUB", MAX - delta_ring],
                   ["Большая полуось", "x_a", "%.4f" % x_a],
                   ["Малая полуось", "y_b", "%.4f" % y_b],
                   ["Фокальное расстояние", "c", "%.4f" % c],
                   ["Координаты центра", "x, y", (float("%.4f" % u), float("%.4f" % v))],
                   ["Эксцентриситет", "exs", "%.4f" % exs],
                   ["Фокальный параметр", "p", "%.4f" % p],
                   ["Перифокусное расстояние", "r_p", "%.4f" % r_p],
                   ["Апофокусное расстояние", "r_a", "%.4f" % r_a]]

    t = np.linspace(0, 2 * pi, 1000)

    temp_file = file_path + 'temp_image.png'

    a = np.array(im)
    a[a < low_value_i_sub] = 0
    imga = Image.fromarray(a)
    if update == 0:
        fig, ax = plt.subplots(nrows=1, ncols=1)
        ax.plot(u + x_a * np.cos(t), v + y_b * np.sin(t), linewidth=5, zorder=3)
        if points_plot:
            plt.plot(xs, ys, "o", zorder=2)
        plt.imshow(imga)
        plt.xlim((300, 600))
        plt.ylim((300, 100))
        fig.savefig(temp_file)
        plt.close(fig)
    elif update == 1:
        plt.plot(u + x_a * np.cos(t), v + y_b * np.sin(t), linewidth=5, zorder=3)
        if points_plot:
            plt.plot(xs, ys, "o", zorder=2)
        plt.imshow(imga)
        plt.xlim((300, 600))
        plt.ylim((300, 100))
        plt.savefig(temp_file)
    elif update == 2:
        plt.close('all')
        plt.imshow(imga)
        plt.xlim((300, 600))
        plt.ylim((300, 100))
        plt.savefig(temp_file)

    return temp_file, out_results


def img_3d_interp(im, file_path, W=640, H=480):
    """
    Строим 3D график по изображению возвращает объект 3d картинки
    Параметры:  im - объект Image.open("./path/to/file_name.png").convert("I")
                W - ширина изображения в пикселях
                H - высота изображения в пикселях
    """
    a = np.array(im)

    # Формируем данные
    X = np.arange(0, W, 1)
    Y = np.arange(0, H, 1)
    X, Y = np.meshgrid(X, Y)
    Z = a

    temp_file = file_path + 'temp_image.png'

    # Отрисовываем фигуру
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    # Строим график
    surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, linewidth=0, antialiased=False)

    # Добавляем градиент цвета.
    fig.colorbar(surf, shrink=0.5, aspect=15)
    fig.savefig(temp_file)
    plt.close(fig)

    return temp_file


def gaussian(x, amplitude, mean, stddev):
    return amplitude * np.exp(-(x - mean)**2 / (2 * stddev**2))
