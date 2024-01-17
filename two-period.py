import numpy as np
import matplotlib.pyplot as plt

C = 47 * 10 ** -6  # емкость
E_m = 10  # амплитуда ЭДС гениератора
R = 10 ** 5  # Сопротивление нагрузки
r = 3.386 # сопротивление


def E(tau, w):  # входной сигнал_2
    return abs(E_m*np.sin(w * tau * r * C))


def equation(tau, v, w):  # диффур
    return E(tau, w) / E_m - v * (1 + r / R)


def mama(w, tau, h):  # функция численного решения диффура
    x = [0]  # выходное напряжение
    for i in range(len(tau) - 1):
        k0 = h * equation(tau[i], x[i], w)
        k1 = h * equation(tau[i] + 0.5 * h, x[i] + 0.5 * k0, w)
        k2 = h * equation(tau[i] + 0.5 * h, x[i] + 0.5 * k1, w)
        k3 = h * equation(tau[i] + h, x[i] + k2, w)
        x.append(x[i] + (1 / 6) * (k0 + 2 * k1 + 2 * k2 + k3))
    return x


# Зависимость напряжения от времени:
def time(f, tau, h):
    w = f * 2 * np.pi  # циклическая частота генератора
    x = mama(w, tau, h)

    plt.plot([i for i in tau], [E(i, w) / E_m for i in tau])  # начальный сигнал генератора
    plt.plot([i for i in tau], x)  # выходное напряжение
    plt.title(f'Частота среза: {round(1 / (2 * np.pi * C * r))} Гц \n Частота генератора: {round(w / (2 * np.pi))} Гц')
    plt.xlabel('tau')
    plt.ylabel('v')
    plt.grid(which="both")
    plt.minorticks_on()
    plt.xlim(10, tau[-1])
    plt.show()


# АЧХ:
def fr(start, stop, step, tau, h):
    u_max = []  # массив асплитудных значений напряжения на выходе
    f = []  # массив циклической частоты
    for i in range(start, stop, step):
        u_max.append(max(mama(2 * np.pi * i, tau, h)))
        f.append(i)

    plt.plot([round(1 / (2 * np.pi * C * r)) for _ in u_max], u_max)  # прямая частоты среза
    plt.plot(f, u_max)  # АЧХ
    plt.xlabel('f, Гц')
    plt.ylabel(r'$v_m$')
    plt.title(f'Частота среза: {round(1 / (2 * np.pi * C * r))} Гц')
    plt.grid(which="both")
    plt.minorticks_on()
    plt.show()


tau = np.linspace(0, 80, 1001)
h = (tau[1] - tau[0]) / 2  # разбиение

# time(1000, tau, h)  # задаем входную частоту, массив времени, разбиение и строим v(t)

fr(20, 10000, 50, tau, h)  # v(w), задачется начальное, конечное значение частоты и шаг
