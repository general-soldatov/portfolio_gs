from tkinter import *
from tkinter.messagebox import showinfo, showerror
from tkinter.ttk import Combobox
from numpy import cos, sin, tan, arange, linspace
from math import pi
from scipy.optimize import root
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plot

def derivative(f,a,method='central',h=0.01):
    if method == 'central':
        return (f(a + h) - f(a - h))/(2*h)
    elif method == 'forward':
        return (f(a + h) - f(a))/h
    elif method == 'backward':
        return (f(a) - f(a - h))/h
    else:
        print("Method must be 'central', 'forward' or 'backward'.")

class Dynam_I(object):

    def __init__(self, var=3): #процедура инициализации класса
        self.var = var

        # исходные данные для расчёта
        self.dynMass = [[1, 0, 2.0, 50, 1.0, 2, 0.0, 0, 60, 30, 0, 0.05],
             [2, 0, 3.0, 60, 1.5, 3, 0.0, 0, 30, 60, 0, 0.1],
             [3, 0, 4.0, 70, 2.0, 3, 0.0, 0, 0, 30, 0, 0.15],
             [4, 1, 2.0, 80, 0.5, 0, 10.0, 5, 30, 45, 0, 0.1],
             [5, 1, 3.0, 110, 0.7, 0, 12.0, 7, 60, 30, 0, 0.15],
             [6, 1, 4.0, 120, 0.9, 0, 14.0, 9, 30, 60, 0, 0.2],
             [7, 2, 3.0, 50, 1.0, 4, 0.0, 0, 30, 0, 60, 0.2],
             [8, 2, 2.0, 60, 1.5, 6, 0.0, 0, 60, 0, 30, 0.15],
             [9, 2, 5.0, 70, 1.2, 9, 0.0, 0, 30, 0, 60, 0.1],
             [10, 3, 1.0, 60, 2.5, 0, 0.0, 0, 0, 60, 30, 0.05],
             [11, 3, 1.5, 70, 3.0, 0, 0.0, 0, 45, 30, 60, 0.1],
             [12, 3, 2.5, 80, 3.5, 0, 0.0, 0, 30, 60, 30, 0.15],
             [13, 4, 3.0, 50, 1.2, 0, 4.0, 2, 30, 0, 0, 0.1],
             [14, 4, 2.0, 60, 1.7, 0, 6.0, 7, 60, 0, 0, 0.15],
             [15, 4, 5.0, 70, 1.4, 0, 9.0, 5, 30, 0, 0, 0.2],
             [16, 5, 4.0, 50, 6.5, 2, 0.0, 0, 60, 30, 0, 0.2],
             [17, 5, 5.5, 60, 4.5, 4, 0.0, 0, 30, 45, 0, 0.15],
             [18, 5, 2.8, 70, 3.5, 6, 0.0, 0, 60, 30, 0, 0.1],
             [19, 6, 2.4, 60, 2.5, 0, 0.0, 0, 60, 30, 0, 0.05],
             [20, 6, 4.5, 90, 3.5, 0, 0.0, 0, 30, 60, 0, 0.1],
             [21, 6, 3.2, 80, 3.0, 0, 0.0, 0, 60, 30, 0, 0.15],
             [22, 7, 2.3, 60, 5.0, 0, 0.0, 0, 60, 30, 45, 0.1],
             [23, 7, 3.7, 70, 3.0, 0, 0.0, 0, 45, 60, 30, 0.15],
             [24, 7, 5.4, 90, 4.5, 0, 0.0, 0, 45, 30, 60, 0.2],
             [25, 8, 1.0, 30, 1.5, 0, 3.5, 0, 60, 30, 0, 0.2],
             [26, 8, 1.5, 40, 2.5, 0, 4.5, 0, 30, 60, 0, 0.15],
             [27, 8, 2.5, 50, 3.5, 0, 5.0, 0, 60, 30, 0, 0.1],
             [28, 9, 3.0, 45, 4.0, 0, 0.0, 0, 30, 0, 60, 0.05],
             [29, 9, 2.0, 35, 3.0, 0, 0.0, 0, 60, 0, 45, 0.1],
             [30, 9, 5.0, 55, 3.5, 0, 0.0, 0, 30, 0, 60, 0.15]]

        self.pict = self.dynMass[self.var - 1][1]

    def corner(self): # функция для вывода углов
        rad = lambda x: x * pi / 180  # лямбда-функция для перевода градусов в радианы
        phi = rad(self.dynMass[self.var-1][8])
        self.alpha = rad(self.dynMass[self.var-1][9])
        beta = rad(self.dynMass[self.var-1][10])
        return phi, self.alpha, beta

    def dyn(self): # функция вывода динамических характеристик
        friction = self.dynMass[self.var - 1][11]
        mass = self.dynMass[self.var-1][2]
        force_ext = self.dynMass[self.var-1][3]
        grav = 9.8061  # ускорение свободного падения
        return friction, mass, force_ext, grav

    def geom(self): # функция вывода геометрических характеристик
        self.corner()
        AB = self.dynMass[self.var-1][4]
        BD = self.dynMass[self.var-1][5]
        BC = self.dynMass[self.var-1][6]
        CD = self.dynMass[self.var-1][7]
        if self.pict == 3 or self.pict == 6:
            BD = AB * sin(self.alpha)
        return AB, BD, BC, CD

    def solveSlip(self): # расчёт движения тела по поверхности
        phi, alpha, beta = self.corner()
        friction, mass, force_ext, grav = self.dyn()
        AB, BD, BC, CD = self.geom()
        self.support_reaction = mass * grav * cos(alpha) + force_ext * sin(phi)

        self.force = [
            mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            - mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            force_ext * cos(phi) - friction * self.support_reaction,
            - mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            force_ext * cos(phi) - friction * self.support_reaction,
            force_ext * cos(phi) - friction * self.support_reaction,
            - mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            - mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            mass * grav * sin(alpha) + force_ext * cos(phi) - friction * self.support_reaction,
            force_ext * cos(phi) - friction * self.support_reaction
        ]

        boost_x = self.force[self.pict] / mass
        timeAB = (2 * AB / boost_x) ** 0.5
        speedAB = boost_x * timeAB

        return boost_x, timeAB, speedAB

    def solveKinetic(self): # расчёт движения по теореме об изменении
        self.solveSlip()    # кинетической энергии и количества движения
        phi, alpha, beta = self.corner()
        friction, mass, force_ext, grav = self.dyn()
        AB, BD, BC, CD = self.geom()
        work_ext = force_ext * AB * cos(phi)
        work_grav = mass * grav * AB * sin(alpha)
        work_friction = friction * self.support_reaction * AB
        sum_work = [
            work_ext + work_grav - work_friction,
            work_ext - work_grav - work_friction,
            work_ext - work_friction,
            work_ext - work_grav - work_friction,
            work_ext - work_friction,
            work_ext - work_friction,
            work_ext - work_grav - work_friction,
            work_ext - work_grav - work_friction,
            work_ext + work_grav - work_friction,
            work_ext - work_grav - work_friction,
        ]
        speed_work_AB = (2 * (sum_work[self.pict]) / mass) ** 0.5

        time_work_AB = mass * speed_work_AB / self.force[self.pict]

        return time_work_AB, speed_work_AB

    def solveFly(self): # расчёт свободного полёта тела
        boost_x, timeAB, speedAB = self.solveSlip()
        phi, alpha, beta = self.corner()
        friction, mass, force_ext, grav = self.dyn()
        AB, BD, BC, CD = self.geom()

        x_body = [
            lambda t: speedAB * cos(alpha) * t,
            lambda t: BC + speedAB * sin(alpha) * t - 0.5 * grav * t ** 2,
            lambda t: speedAB * t,
            lambda t: speedAB * cos(alpha) * t,
            lambda t: BC - 0.5 * grav * t ** 2,
            lambda t: speedAB * t,
            lambda t: speedAB * cos(alpha) * t,
            lambda t: speedAB * cos(alpha) * t,
            lambda t: speedAB * cos(alpha) * t,
            lambda t: speedAB * t
        ]

        body_solve = [
            lambda t: grav * t ** 2 - 2 * BD,  # pict = 0
            lambda t: speedAB * cos(alpha) * t - CD,  # pict = 1
            lambda t: BD - speedAB * t * cos(beta) / sin(beta) - 0.5 * grav * t ** 2,  # pict = 2
            lambda t: BD - speedAB * t * cos(alpha) * sin(beta) / cos(beta) + speedAB * t * sin(alpha) - 0.5 * grav * t ** 2,
            lambda t: speedAB * cos(alpha) * t - CD,
            lambda t: BD + speedAB * t * sin(alpha) / cos(alpha) - 0.5 * grav * t ** 2,
            lambda t: BD + speedAB * t * sin(alpha) - 0.5 * grav * t ** 2,
            lambda t: speedAB * t * (cos(beta) * cos(alpha) / sin(beta) + sin(alpha)) - 0.5 * grav * t ** 2,
            lambda t: BC - speedAB * sin(alpha) * t - 0.5 * grav * t ** 2,
            lambda t: speedAB * t * cos(beta) / sin(beta) - 0.5 * grav * t ** 2

        ]

        fly = root(body_solve[self.pict], 1)
        t_BK = fly.x[0]

        match self.pict: # расчёт длины участка DK
            case 0:
                DK = x_body[self.pict](fly.x[0]) / cos(alpha)
                dynCase = f"DK = {round(DK, 2)} м"

            case 1:
                func = lambda t: + speedAB * sin(alpha) * t - 0.5 * grav * t ** 2 + BC
                eq1 = root(func, 1).x[0]
                if eq1 < fly.x[0]:
                    t_BK = eq1
                    DK = -body_solve[self.pict](t_BK)
                else:
                    DK = x_body[self.pict](t_BK)
                dynCase = f"DK = {round(DK, 2)} м"
            case 2:
                DK = x_body[self.pict](fly.x[0]) / sin(beta)
                dynCase = f"DK = {round(DK, 2)} м"

            case 3:
                DK = x_body[self.pict](fly.x[0]) / cos(beta)
                dynCase = f"DK = {round(DK, 2)} м"
            case 4:
                func = lambda t: speedAB * sin(alpha) * t - 0.5 * grav * t ** 2 + BC
                eq1 = root(func, 1).x[0]
                if eq1 < fly.x[0]:
                    t_BK = eq1
                    DK = body_solve[self.pict](t_BK)
                else:
                    DK = x_body[self.pict](t_BK)
                dynCase = f"DK = {round(DK, 2)} м"
            case 5:
                DK = x_body[self.pict](fly.x[0]) / cos(alpha)
                dynCase = f"DK = {round(DK, 2)} м"
            case 6:
                DK = x_body[self.pict](fly.x[0])
                dynCase = f"DK = {round(DK, 2)} м"
            case 7:
                DK = x_body[self.pict](fly.x[0]) / sin(beta)
                dynCase = f"DK = {round(DK, 2)} м"
            case 8:
                CK = x_body[self.pict](fly.x[0])
                dynCase = f"CK = {round(CK, 2)} м"
            case 9:
                DK = x_body[self.pict](fly.x[0]) / sin(beta)
                dynCase = f"DK = {round(DK, 2)} м"

        return t_BK, dynCase

    def grapher(self, t): # функция графика полёта тела
        pict = self.pict
        boost_x, timeAB, speedAB = self.solveSlip()
        phi, alpha, beta = self.corner()
        friction, mass, force_ext, grav = self.dyn()
        match pict:
            case 0: graph = lambda t : - speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 1: graph = lambda t : speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 2: graph = lambda t: - 0.5 * grav * (t / cos(alpha)) ** 2
            case 3: graph = lambda t: speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 4: graph = lambda t: - 0.5 * grav * (t) ** 2
            case 5: graph = lambda t: - 0.5 * grav * (t) ** 2
            case 6: graph = lambda t: speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 7: graph = lambda t: speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 8: graph = lambda t: - speedAB * tan(alpha) * t - 0.5 * grav * (t / cos(alpha)) ** 2
            case 9: graph = lambda t: - 0.5 * grav * (t / cos(alpha)) ** 2

        return graph(t)

    def drawConst(self): # исходные данные для визуализации
        t_BK, dynCase = self.solveFly()
        boost_x, timeAB, speedAB = self.solveSlip()
        phi, alpha, beta = self.corner()
        friction, mass, force_ext, grav = self.dyn()
        AB, BD, BC, CD = self.geom()
        if self.pict == 5:
            x_fly = arange(0, t_BK * speedAB, 0.001)
        else:
            x_fly = arange(0, t_BK * speedAB * cos(alpha), 0.001)
        match self.pict:
            case 0:
                xCort = (
                    [[0, 0], [0, -BD]],  #line BD
                    [[-AB * cos(alpha), 0], [AB * sin(alpha), 0]],  #line AB
                    [x_fly, -tan(alpha) * x_fly - BD], #lineDK
                    [[-AB * cos(alpha), AB * sin(alpha) + 0.1], # word A
                     [t_BK * speedAB * cos(alpha), -tan(alpha) * t_BK * speedAB * cos(alpha) - BD + 0.1]] # word K
                )
            case 1:
                xCort = (
                    [[0, 0], [0, -BC]],  # line BC
                    [[0, CD], [-BC, -BC]],  # line CD
                    [[CD, CD], [0, -BC]],  # lineDK
                    [[AB * cos(pi - alpha), 0], [-AB * sin(pi - alpha), 0]], #lineAB
                    [[AB * cos(pi - alpha), -AB * sin(pi - alpha) + 0.1], # word A
                     [t_BK * speedAB * cos(alpha), speedAB * t_BK * sin(alpha) - 0.5 * grav * t_BK ** 2 + 0.1]]  # word K
                )

            case 2:
                xCort = (
                    [[0, 0], [0, -BD]],  # line BD
                    [[-AB, 0], [0, 0]],  # line AB
                    [x_fly, tan(pi / 2 - beta) * x_fly - BD],  # lineDK
                    [[-AB * cos(alpha), AB * sin(alpha) + 0.1], # word A
                     [t_BK * speedAB, - 0.5 * grav * t_BK ** 2 + 0.1]]  # word K
                )

            case 3:
                xCort = (
                    [[0, 0], [0, -BD]],  # line BD
                    [[AB * cos(pi - alpha), 0], [-AB * sin(pi - alpha), 0]],  # line AB
                    [x_fly, tan(beta) * x_fly - BD],  # lineDK
                    [[AB * cos(pi - alpha), -AB * sin(pi - alpha) + 0.1],  # word A
                     [t_BK * speedAB * cos(alpha), speedAB * t_BK * sin(alpha) - 0.5 * grav * t_BK ** 2 + 0.1]] # word K
                )

            case 4:
                xCort = (
                    [[0, 0], [0, -BC]],  # line BC
                    [[0, CD], [-BC, -BC]],  # line CD
                    [[CD, CD], [0, -BC]],  # lineDK
                    [[-AB, 0], [0, 0]],  # lineAB
                    [[-AB, 0.1],  # word A
                     [t_BK * speedAB, - 0.5 * grav * t_BK ** 2 + 0.1]]  # word K
                )

            case 5:
                xCort = (
                    [[0, 0], [0, -BD]],  # line BD
                    [[-AB, 0], [0, 0]],  # line AB
                    [x_fly, -tan(alpha) * x_fly - BD],  # lineDK
                    [[-AB, 0.1],  # word A
                     [t_BK * speedAB + 0.001, self.grapher(t_BK) + 0.01]] # word K
                )

            case 6:
                xCort = (
                    [[0, 0], [0, -BD]],  # line BD
                    [[AB * cos(pi - alpha), 0], [-AB * sin(pi - alpha), 0]],  # line AB
                    [x_fly, 0 * x_fly - BD],  # lineDK
                    [[AB * cos(pi - alpha), -AB * sin(pi - alpha) + 0.1],  # word A
                     [t_BK * speedAB * cos(alpha), speedAB * t_BK * sin(alpha) - 0.5 * grav * (t_BK) ** 2 + 0.1]]  # word K
                )

            case 7:
                xCort = (
                    [[0, 0], [0, -AB * sin(alpha)]],  # line BD
                    [[AB * cos(pi - alpha), 0], [-AB * sin(pi - alpha), 0]],  # line AB
                    [x_fly, -tan(pi / 2 - beta) * x_fly],  # lineDK
                    [[AB * cos(pi - alpha), -AB * sin(pi - alpha) + 0.1],  # word A
                     [t_BK * speedAB * cos(alpha), speedAB * t_BK * sin(alpha) - 0.5 * grav * t_BK ** 2 + 0.1]] # word K
                )

            case 8:
                xCort = (
                    [[0, 0], [0, -BC]],  # line BD
                    [[-AB * cos(pi - alpha), 0], [AB * sin(pi - alpha), 0]],  # line AB
                    [-x_fly, 0 * x_fly - BC],  # lineDK
                    [[-AB * cos(pi - alpha), AB * sin(pi - alpha) + 0.1],  # word A
                     [-t_BK * speedAB * cos(alpha), - speedAB * t_BK * sin(alpha) - 0.5 * grav * t_BK ** 2 + 0.1]] # word K
                )
            case 9:
                xCort = (
                    [[0, 0], [0, 0]],  # line BD
                    [[-AB, 0], [0, 0]],  # line AB
                    [x_fly, -tan(pi / 2 - beta) * x_fly],  # lineDK
                    [[-AB, 0.1],  # word A
                     [t_BK * speedAB, - 0.5 * grav * t_BK ** 2 + 0.1]] # word K
                )

        return x_fly, xCort

    def plotTk(self, tk): # процедура вывода визализации с помощью средств
        boost_x, timeAB, speedAB = self.solveSlip() # фреймворка Tkinter
        grapher = lambda t: self.grapher(t)
        x_fly, xCort = self.drawConst()
        t_fly = x_fly / speedAB

        if self.pict in (0, 2, 3, 5, 6, 7, 9):
            lineBD, lineAB, lineDK, word = xCort

            tk.plot(lineDK[0], lineDK[1], lw=2, color='blue')
            tk.plot(lineBD[0], lineBD[1], lw=2, color='blue')

            tk.plot(x_fly, grapher(t_fly), '-', lw=2, color='orange')
            tk.plot(lineAB[0], lineAB[1], lw=2, color='orange', marker='o')

        elif self.pict == 1 or self.pict == 4:
            lineBC, lineCD, lineDK, lineAB, word = xCort

            tk.plot(lineBC[0], lineBC[1], lw=2, color='blue')
            tk.plot(lineCD[0], lineCD[1], lw=2, color='blue')
            tk.plot(lineDK[0], lineDK[1], lw=2, color='blue')

            tk.plot(x_fly, grapher(t_fly), '-', lw=2, color='orange')
            tk.plot(lineAB[0], lineAB[1], lw=2, color='orange', marker='o')

        elif self.pict == 8:
            lineBD, lineAB, lineDK, word = xCort

            tk.plot(lineDK[0], lineDK[1], lw=2, color='blue')
            tk.plot(lineBD[0], lineBD[1], lw=2, color='blue')

            tk.plot(-x_fly, grapher(t_fly), '-', lw=2, color='orange')
            tk.plot(lineAB[0], lineAB[1], lw=2, color='orange', marker='o')

        tk.text(word[0][0], word[0][1], 'A', fontsize=10)
        tk.text(word[1][0], word[1][1], 'K', fontsize=10)
        tk.text(0, 0.1, 'B', fontsize=10)

    def plotMath(self): # процедура визуализации с помощью библиотеки
        self.plotTk(plot)
        plot.xlabel('x (м)')
        plot.ylabel('y (м)')
        plot.subplot(1, 1, 1)
        plot.grid(True)
        plot.show()



    def printCase(self):
        friction, mass, force_ext, grav = self.dyn()
        AB, BD, BC, CD = self.geom()
        boost_x, timeAB, speedAB = self.solveSlip()
        time_work_AB, speed_work_AB = self.solveKinetic()
        t_BK, dynCase = self.solveFly()
        result = f'''Решение:
        Тело массой {mass} кг скользит по участку AB={AB} м
        под действием силы Q={force_ext} Н.
        Результаты расчёта по II закону Ньютона: 
        х = {round(boost_x, 2)}*t^2/2, t_AB = {round(timeAB, 2)} c, v_AB = {round(speedAB, 2)} м/с
        Проверка по теореме об изменении кинетической 
        энергии и количества движения:
        t_AB = {round(time_work_AB, 2)} c, v_AB = {round(speed_work_AB, 2)} м/с
        Свободный полёт тела:
        t_BK = {round(t_BK, 2)} c, {dynCase}
        '''
        return result


class Kinem_I(object):

    def __init__(self, var, ts=1):
        self.var = (var//10, var%10)

        self.ordinate = [
            lambda t: 1 + 4 * cos(pi * t / 6),
            lambda t: 2 * cos(pi * t / 3),
            lambda t: 3 - cos(pi * t / 6),
            lambda t: cos(pi * t / 3) - 2,
            lambda t: 7 * cos(pi * t / 6) - 5,
            lambda t: 2 - 3 * cos(pi * t / 6),
            lambda t: cos(pi * t / 3),
            lambda t: - cos(pi * t / 6) + 8,
            lambda t: - cos(pi * t / 3),
            lambda t: 3 + 7 * cos(pi * t / 6),
        ]

        self.absciss = [
            lambda t: 4 + 2 * sin(pi * t / 6),
            lambda t: 4 * sin(pi * t / 6) - 2,
            lambda t: sin(pi * t / 6) + 5,
            lambda t: 3 - 2 * sin(pi * t / 6),
            lambda t: - sin(pi * t / 6) - 1,
            lambda t: 2 + 5 * sin(pi * t / 6),
            lambda t: 2 * sin(pi * t / 6),
            lambda t: - 4 * sin(pi * t / 6),
            lambda t: sin(pi * t / 6) + 9,
            lambda t: 7 + 3 * sin(pi * t / 6),
        ]

        self.ts = ts

    def kinPar(self):
        var, ts = self.var, self.ts
        absciss, ordinate = self.absciss[var[1]], self.ordinate[var[0]]

        coordinate = (round(absciss(ts), 2), round(ordinate(ts), 2))
        speed = (
            round(derivative(absciss, ts), 2),
            round(derivative(ordinate, ts), 2)
        )

        boostXY = (
            round(derivative(lambda t: derivative(absciss, t), ts), 2),
            round(derivative(lambda t: derivative(ordinate, t), ts), 2)
        )

        boostTN = (round((speed[0] * boostXY[0] + speed[1] * boostXY[1]) / (speed[0] ** 2 + speed[1] ** 2) ** 0.5, 2),
                   round((speed[0] * boostXY[1] - speed[1] * boostXY[0]) / (speed[0] ** 2 + speed[1] ** 2) ** 0.5, 2))


        return coordinate, speed, boostXY, boostTN


    def printCase(self):
        coordinate, speed, boostXY, boostTN = self.kinPar()

        speedABS = round((speed[0] ** 2 + speed[1] ** 2) ** 0.5, 2)
        boostABS = round((boostXY[0]**2 + boostXY[0]**2)**0.5)
        ro = round(speedABS ** 2 / boostTN[1], 2)

        result = f'''Решение: 
        В момент времени t = {self.ts} c исходная точка  
        О({coordinate[0]}, {coordinate[1]}), скорость в этой точке 
        v_x = {speed[0]} м/с, v_y = {speed[1]} м/с.
        Ускорение a_x = {boostXY[0]} м/с^2, a_y = {boostXY[1]} м/с^2.
        Модули v = {speedABS} м/с, a = {boostABS} м/с^2.
        Тангенциальное ускорение а_t = {boostTN[0]} м/с^2, 
        нормальное a_n = {boostTN[1]} м/с^2, 
        радиус кривизны в этой точке {ro} м.
        '''
        return result

    def plotTk(self, plt):
        var = self.var
        absciss, ordinate = self.absciss[var[1]], self.ordinate[var[0]]
        coordinate, speed, boostXY, boostTN = self.kinPar()
        x, y = coordinate
        vx, vy = speed
        v = (speed[0] ** 2 + speed[1] ** 2) ** 0.5
        x_tr = arange(0, 20, 0.1)
        plt.plot(absciss(x_tr), ordinate(x_tr), 'blue')
        plt.plot(coordinate[0], coordinate[1], 'o', color='red')
        plt.annotate(r'$\vec V$', xy=(x, y), xytext=(x + vx, y + vy),
                     arrowprops=dict(arrowstyle="<-", linewidth=0.8 * v, color='red'))

    def plotMath(self):
        self.plotTk(plot)
        plot.xlabel('x (м)')
        plot.ylabel('y (м)')
        plot.subplot(1, 1, 1)
        plot.grid(True)
        plot.show()

class Kinem_II(object):

    def __init__(self, var, ts=1): #процедура инициализации класса
        self.var = (var//10, var%10)
        self.ts = ts
        self.Rad = [(2, 4),(6, 8), (12, 14)]

    def caseDriver(self):
        ts, var = self.ts, self.var[1]

        driver = [
            lambda t: 3 * (t ** 2 - 5 * t),
            lambda t: 9 * t - 4 * t ** 2,
            lambda t: 7 * t - 4 * t ** 2,
            lambda t: 3 * (7 * t - 2 * t ** 2),
            lambda t: 3 * t ** 2 - 7 * t,
            lambda t: 11 * t - 6 * t ** 2,
            lambda t: 2 * (t ** 2 - 4),
            lambda t: 4 * t - t ** 2,
            lambda t: 2 * (t ** 2 - 3 * t),
            lambda t: 2 * t ** 2 - 9
        ]

        start = (2, 3, 2, 4, 5, 1, 5, 3, 2, 1)

        if var in (0, 3, 4, 7, 8, 9):
            speed = derivative(driver[var], ts)
            boost = derivative(lambda t: derivative(driver[var], t), ts)
        elif var in (1, 2, 5, 6):
            speed = driver[var](ts)
            boost = derivative(driver[var], ts)

        speedList = [
            ['4', '1'], ['4', '1'], ['5', '3'],
            ['B', 'C'], ['A', 'C'], ['B', '5'],
            ['A', 'C'], ['5', '1'],
            ['A', '3'], ['4', '2']
        ]

        boostList = [
            ['1', 'B', '5'],
            ['1', 'C', '5'],
            ['1', 'A', '4'],
            ['2', 'A', '5'],
            ['3', 'B', '4'],
            ['2', 'C', '4'],
            ['3', 'B', '4'],
            ['1', 'B', '4'],
            ['3', 'B', '5'],
            ['2', 'B', '5']
        ]

        return start[var], speed, boost, speedList[var], boostList[var]

    def pictDriver(self):
        (r1, R1), (r2, R2), (r3, R3) = self.Rad
        var = self.var
        start, speed, boost, speedList, boostList = self.caseDriver()

        match var[0]:
            case 0:
                pict = {
                    '1': [0, 1, -r2 / r3 * R3 / R1, -R3 / R1, -1 / r1, -1 / R2 * r2 / r3 * R3 / R1],
                    '2': [0, -R1 / R3 * r3 / r2, 1, r3 / r2, 1 / r1 * R1 / R3 * r3 / r2, 1 / R2],
                    '3': [0, -R1 / R3, r2 / r3, 1, 1 / r1 * R1 / R3, 1 / R2 * r2 / r3],
                    '4': [0, -r1, r2 / r3 * R3 / R1 * r1, R3 / R1 * r1, 1, 1 / R2 * r2 / r3 * R3 / R1 * r1],
                    '5': [0, -R1 / R3 * r3 / r2 * R2, R2, r3 / r2 * R2, 1 / r1 * R1 / R3 * r3 / r2 * R2, 1]

                }

                pictW = {
                    'A': [pict['1'][start], R1],
                    'B': [pict['3'][start], r3],
                    'C': [pict['2'][start], R2]
                }

            case 1:
                pict = {
                    '1': [0, 1, -R2 / R1, -r3 / r2 * R2 / R1, -1 / r1, -1 / R3 * r3 / r2 * R2 / r1],
                    '2': [0, -R1 / R2, 1, r3 / r2, 1 / r1 * R1 / R2, 1 / R3 * r3 / r2],
                    '3': [0, -R1 / R2 * r2 / r3, r2 / r3, 1, 1 / r1 * R1 / R2 * r2 / r3],
                    '4': [0, -r1, R2 / R1 * r1, r3 / r2 * R2 / R1 * r1, 1, 1 / R3 * r3 / r2 * R2 / R1 * r1],
                    '5': [0, -R1 / R2 * r2 / r3 * R3, r2 / r3 * R3, R3, 1 / r1 * R1 / R2 * r2 / r3 * R3, 1]

                }

                pictW = {
                    'A': [pict['1'][start], R1],
                    'B': [pict['2'][start], r2],
                    'C': [pict['3'][start], R3]
                }

            case 2:
                pict = {
                    '1': [0, 1, -R2 / r3 * R3 / R1, -R3 / R1, 1 / r2 * R2 / r3 * R3 / R1, 1 / r1],
                    '2': [0, -R1 / R3 * r3 / R2, 1, r3 / R2, -1 / r2, -1 / r1 * R1 / R3 * r3 / R2],
                    '3': [0, -R1 / R3, R2 / r3, 1, -1 / r2 * R2 / r3, -1 / r1 * R1 / R3],
                    '4': [0, R1 / R3 * r3 / R2 * r2, -r2, -r3 / R2 * r2, 1, 1 / r1 * R1 / R3 * r3 / R2 * r2],
                    '5': [0, r1, -R2 / r3 * R3 / R1 * r1, -R3 / R1 * r1, 1 / r2 * R2 / r3 * R3 / R1 * r1, 1]

                }

                pictW = {
                    'A': [pict['1'][start], r1],
                    'B': [pict['2'][start], R2],
                    'C': [pict['3'][start], R3]
                }

            case 3:
                pict = {
                    '1': [0, 1, R2 / R1, -R3 / r1, -1 / r2 * R2 / R1, -1 / r3 * R3 / r1],
                    '2': [0, R1 / R2, 1, -R3 / r1 * R1 / R2, -1 / r2, -1 / r3 * R3 / r1 * R1 / R2],
                    '3': [0, -r1 / R3, -R2 / R1 * r1 / R3, 1, 1 / r2 * R2 / R1 * r1 / R3, 1 / r3],
                    '4': [0, -R1 / R2 * r2, -r2, R3 / r1 * R1 / R2 * r2, 1, 1 / r3 * R3 / r1 * R1 / R2 * r2],
                    '5': [0, -r1 / R3 * r3, -R2 / R1 * r1 / R3 * r3, r3, 1 / r2 * R2 / R1 * r1 / R3 * r3, 1]

                }

                pictW = {
                    'A': [pict['1'][start], r1],
                    'B': [pict['2'][start], R2],
                    'C': [pict['3'][start], r3]
                }

            case 4:
                pict = {
                    '1': [0, 1, r2 / R1, -R3 / r1, 1 / r3 * R3 / r1, 1 / R2 * r2 / R1],
                    '2': [0, R1 / r2, 1, -R3 / r1 * R1 / r2, 1 / r3 * R3 / r1 * R1 / r2, 1 / r2],
                    '3': [0, -r1 / R3, -r2 / R1 * r1 / R3, 1, -1 / r3, -1 / R2 * r2 / R1 * r1 / R3],
                    '4': [0, r1 / R3 * r3, r2 / R1 * r1 / R3 * r3, -r3, 1 / R2 * r2 / R1 * r1 / R3 * r3],
                    '5': [0, R1 / r2 * R2, R2, -R3 / r1 * R1 / r2 * R2, 1 / r3 * R3 / r1 * R1 / r2 * R2, 1]

                }

                pictW = {
                    'A': [pict['1'][start], R1],
                    'B': [pict['2'][start], R2],
                    'C': [pict['3'][start], R3]
                }

            case 5:
                pict = {
                    '1': [0, 1, r2 / R1, -R3 / R2 * r2 / R1, 1 / r3 * R3 / R2 * r2 / R1, 1 / r1],
                    '2': [0, R1 / r2, 1, -R3 / R2, 1 / r3 * R3 / R2, 1 / r1 * R1 / r2],
                    '3': [0, -R1 / r2 * R2 / R3, -R2 / R3, 1, -1 / r3, -1 / r1 * R1 / r2 * R2 / R3],
                    '4': [0, R1 / r2 * R2 / R3 * r3, R2 / R3 * r3, -r3, 1, 1 / r1 * R1 / r2 * R2 / R3 * r3],
                    '5': [0, r1, r2 / R1 * r1, -R3 / R2 * r2 / R1 * r1, 1 / r3 * R3 / R2 * r2 / R1 * r1, 1]

                }

                pictW = {
                    'A': [pict['1'][start], r1],
                    'B': [pict['2'][start], r2],
                    'C': [pict['3'][start], R3]
                }

            case 6:
                pict = {
                    '1': [0, 1, -R2 / R3 * r3 / r1, r3 / r1, -1 / R1, -1 / r2 * R2 / R3 * r3 / r1],
                    '2': [0, -r1 / r3 * R3 / R2, 1, -R3 / R2, 1 / R1 * r1 / r3 * R3 / R2, 1 / r2],
                    '3': [0, r1 / r3, -R2 / R3, 1, -1 / R1 * r1 / r3, -1 / r2 * R2 / R3],
                    '4': [0, -R1, R2 / R3 * r3 / r1 * R1, -r3 / r1 * R1, 1, 1 / r2 * R2 / R3 * r3 / r1 * R1],
                    '5': [0, -r1 / r3 * R3 / R2 * r2, r2, -R3 / R2 * r2, 1 / R1 * r1 / r3 * R3 / R2 * r1, 1]

                }

                pictW = {
                    'A': [pict['1'][start], r1],
                    'B': [pict['3'][start], R3],
                    'C': [pict['2'][start], r2]
                }

            case 7:
                pict = {
                    '1': [0, 1, -R2 / r1, -R3 / r2 * R2 / r1, -1 / R1, -1 / r3 * R3 / r2 * R2 / r1],
                    '2': [0, -r1 / R2, 1, R3 / r2, -1 / R1 * r1 / R2, 1 / r3 * R3 / r2],
                    '3': [0, -r1 / R2 * r2 / R3, r2 / R3, 1, 1 / R1 * r1 / R2 * r2 / R3, 1 / r3],
                    '4': [0, -R1, R2 / r1 * R1, R3 / r2 * R2 / r1 * R1, 1, 1 / r3 * R3 / r2 * R2 / r1 * R1],
                    '5': [0, -r1 / R2 * r2 / R3 * r3, r2 / R3 * r3, r3, 1 / R1 * r1 / R2 * r2 / R3 * r3, 1]

                }

                pictW = {
                    'A': [pict['1'][start], R1],
                    'B': [pict['2'][start], R2],
                    'C': [pict['3'][start], R3]
                }

            case 8:
                pict = {
                    '1': [0, 1, r2 / r1, -R3 / R1, -1 / R2 * r2 / r1, -1 / r3 * R3 / R1],
                    '2': [0, r1 / r2, 1, -R3 / R1 * r1 / r2, -1 / R2, -1 / r3 * R3 / R1 * r1 / r2],
                    '3': [0, -R1 / R3, -r2 / r1 * R1 / R3, 1, 1 / R2 * r2 / r1 * R1 / R3, 1 / r3],
                    '4': [0, -r1 / r2 * R2, -R2, R3 / R1 * r1 / r2 * R2, 1, 1 / r3 * R3 / R1 * r1 / r2 * R2],
                    '5': [0, -R1 / R3 * r3, -r2 / r1 * R1 / R3 * r3, r3, 1 / R2 * r2 / r1 * R1 / R3 * r3, 1]

                }

                pictW = {
                    'A': [pict['1'][start], R1],
                    'B': [pict['2'][start], r2],
                    'C': [pict['3'][start], r3]
                }

            case 9:
                pict = {
                    '1': [0, 1, -R2 / R1, -R3 / r2 * R2 / R1, -1 / r1, -1 / r3 * R3 / r2 * R2 / R1],
                    '2': [0, -R1 / R2, 1, R3 / r2, 1 / r1 * R1 / R2, 1 / r3 * R3 / r2],
                    '3': [0, -R1 / R2 * r2 / R3, r2 / R3, 1, 1 / r1 * R1 / R2 * r2 / R3, 1 / r3],
                    '4': [0, -r1, R2 / R1 * r1, R3 / r2 * R2 / R1 * r1, 1, 1 / r3 * R3 / r2 * R2 / R1 * r1],
                    '5': [0, -R1 / R2 * r2 / R3 * r3, r2 / R3 * r3, r3, 1 / r1 * R1 / R2 * r2 / R3 * r3, 1]

                }

                pictW = {
                    'A': [pict['3'][start], R3],
                    'B': [pict['1'][start], R1],
                    'C': [pict['2'][start], r2]
                }

        speedPrint = []
        boostPrint = []

        signSpeed = lambda l: 'ω' if l in ('1', '2', '3') else 'v'
        signBoost = lambda l: 'ε' if l in ('1', '2', '3') else 'a'

        for sp in speedList:
            if sp in ('A', 'B', 'C'):
                speedTire = speed * pictW[sp][0] * pictW[sp][1]
            else:
                speedTire = speed * pict[sp][start]

            speedPrint.append(f'{signSpeed(sp)}_{sp} = {round(speedTire, 2)}')

        for bo in boostList:
            if bo in ('A', 'B', 'C'):
                boostTire = (speed * pictW[bo][0]) ** 2 * abs(pictW[bo][1])
                boostPrint.append(f'{signBoost(bo)}_{bo}_n = {round(boostTire, 2)}')
                boostTire = boost * abs(pictW[bo][0])
                boostPrint.append(f'{signBoost(bo)}_{bo}_𝜏 = {round(boostTire, 2)}')
            else:
                boostTire = boost * abs(pict[bo][start])
                boostPrint.append(f'{signBoost(bo)}_{bo} = {round(boostTire, 2)}')

        return speedPrint, boostPrint

    def printCase(self):
        speed, boost = self.pictDriver()
        vs = ', '.join(f'{vs} см/с' for vs in speed)
        bs = ''.join(f'{vs} см/с^2,\n' for vs in boost)
        fs = f'Значения скоростей: \n{vs}.\nЗначения ускорений \n{bs}'
        return fs

    def plotTk(self, plt):
        (r1, R1), (r2, R2), (r3, R3) = self.Rad
        v = self.var[0]

        def circ(plt, radius, x):
            theta = linspace(0, 2 * pi, 150)

            a = radius * cos(theta) + x
            b = radius * sin(theta)

            return plt.plot(a, b, color='blue', alpha=.6)

        plt.axis([0, 68, -25, 25])

        axer = [
            [0, 1.5 * R1, 2.5 * R1 + 3. * R3, 2.5 * R1 + R3],
            [0, 1.5 * R1, 2.5 * R1 + R2, 2.5 * R1 + 3 * R3],
            [0, 1.5 * r2 + 3.5 * R3 + R1, 1.5 * r2, 1.5 * r2 + 2.5 * R3],
            [0, 3 * R2 + R1, R2, 3 * R2 + R1 + r1 + R3],
            [0, 2 * R3 + r1, 2 * R3 + r1 + 3 * R2, R3],
            [0, 2 * R3 + 3 * R2 + R1, 2 * R3 + R2, R3],
            [0, 1.5 * R1, 2.5 * R1 + 2 * r3 + R3 + R2, 2.5 * R1 + 2 * r3],
            [0, 1.5 * R1, 2.5 * R1 + R2, 2.5 * R1 + 3 * R2 + R3],
            [0, 3.5 * R2 + R1, 1.5 * R2, 3.5 * R2 + 2 * R1 + R3],
            [0, 1.5 * R1, 2.5 * R1 + R2, 2.5 * R1 + 3 * R2 + R3]

        ]

        sopr = [
            [(axer[v][2], axer[v][3]), (r2, r3), (-r2, -r3)],
            [(axer[v][2], axer[v][3]), (r2, r3), (-r2, -r3)],
            [(axer[v][2], axer[v][3]), (R2, r3), (-R2, -r3)],
            [(axer[v][1], axer[v][2]), (R1, R2), (-R1, -R2)],
            [(axer[v][1], axer[v][2]), (R1, r2), (-R1, -r2)],
            [(axer[v][1], axer[v][2]), (R1, r2), (-R1, -r2)],
            [(axer[v][1], axer[v][3]), (r1, r3), (-r1, -r3)],
            [(axer[v][2], axer[v][3]), (r2, R3), (-r2, -R3)],
            [(axer[v][1], axer[v][2]), (r1, r2), (-r1, -r2)],
            [(axer[v][2], axer[v][3]), (r2, R3), (-r2, -R3)]
        ]

        detal = [
            [(axer[v][1] - r1, axer[v][1] - r1), (axer[v][2] + R2, axer[v][2] + R2), (axer[v][2] + R2 - 2.5, -r3)],
            [(axer[v][1] - r1, axer[v][1] - r1), (axer[v][3] + R3, axer[v][3] + R3), (axer[v][3] + R3 - 2.5, -r3)],
            [(axer[v][2] - r2, axer[v][2] - r2), (axer[v][1] + r1, axer[v][1] + r1), (axer[v][1] + r1 - 2.5, -r3)],
            [(axer[v][2] - r2, axer[v][2] - r2), (axer[v][3] + r3, axer[v][3] + r3), (axer[v][3] + r3 - 2.5, -r3)],
            [(axer[v][3] - r3, axer[v][3] - r3), (axer[v][2] + R2, axer[v][2] + R2), (axer[v][2] + R2 - 2.5, -r3)],
            [(axer[v][3] - r3, axer[v][3] - r3), (axer[v][1] + r1, axer[v][1] + r1), (axer[v][1] + r1 - 2.5, -r3)],
            [(axer[v][1] - R1, axer[v][1] - R1), (axer[v][2] + r2, axer[v][2] + r2), (axer[v][2] + r2 - 2.5, -r3)],
            [(axer[v][1] - R1, axer[v][1] - R1), (axer[v][3] + r3, axer[v][3] + r3), (axer[v][3] + r3 - 2.5, -r3)],
            [(axer[v][2] - R2, axer[v][2] - R2), (axer[v][3] + r3, axer[v][3] + r3), (axer[v][3] + r3 - 2.5, -r3)],
            [(axer[v][1] - r1, axer[v][1] - r1), (axer[v][3] + r3, axer[v][3] + r3), (axer[v][3] + r3 - 2.5, -r3)]
        ]

        plt.text(axer[v][1], 0, '1', fontsize=10)
        plt.text(axer[v][2], 0, '2', fontsize=10)
        plt.text(axer[v][3], 0, '3', fontsize=10)
        plt.text(detal[v][0][0], r2, '4', fontsize=10)
        plt.text(detal[v][1][0], -r3 - 2.5, '5', fontsize=10)

        circ(plt, r1, axer[v][1])
        circ(plt, R1, axer[v][1])
        circ(plt, r2, axer[v][2])
        circ(plt, R2, axer[v][2])
        circ(plt, r3, axer[v][3])
        circ(plt, R3, axer[v][3])

        plt.plot(sopr[v][0], sopr[v][1], color='blue', alpha=.5)
        plt.plot(sopr[v][0], sopr[v][2], color='blue', alpha=.5)

        plt.plot(detal[v][0], (r2, -r2), lw=3, color='blue', alpha=.6)
        plt.plot(detal[v][1], (0, -r3), color='blue', alpha=.5)
        self.detal = detal[v][2]


    def plotMath(self):
        self.plotTk(plot)
        rectangle = plot.Rectangle(self.detal, 5, -5, color='blue', alpha=.6)
        plot.gca().add_patch(rectangle)
        plot.subplot(1, 1, 1)
        plot.grid(False)
        plot.show()




TerMex = {
    "Динамика Д1": Dynam_I,
    "Кинематика К1": Kinem_I,
    "Кинематика К2": Kinem_II
}


def graph(var, task):
    figure = Figure(figsize=(5, 4), dpi=80)
    plt = figure.add_subplot(1, 1, 1)
    figCanv = FigureCanvasTkAgg(figure, dt)
    figCanv.get_tk_widget().place(x=350, y=5)
    try:
        TerMex[task](var=var).plotTk(plt)
    except IndexError:
        showerror(title='Ошибка', message=f'Варианта не существует!')


def click():
    global text_case, num_1, num_2, tasks
    varNum = int(num_1.get() + num_2.get())
    try:
        text = TerMex[tasks.get()](var=varNum).printCase()
        canvas.delete(text_case)
        text_case = canvas.create_text(row[1], line[4], anchor='nw', font=("Arial", font_text), text=text, fill="Black")
        graph(varNum, tasks.get())
    except IndexError:
        showerror(title='Ошибка', message=f'Варианта не существует!')


def clicGraph():
    global text_case, num_1, num_2, tasks
    varNum = int(num_1.get() + num_2.get())
    try:
        TerMex[tasks.get()](var=varNum).plotMath()
    except IndexError:
        showerror(title='Ошибка', message=f'Варианта не существует!')

def clickCopy():
    global dt, tasks, num_1, num_2
    varNum = int(num_1.get() + num_2.get())
    try:
        text = TerMex[tasks.get()](var=varNum).printCase()
        dt.clipboard_clear()
        dt.clipboard_append(text)
        showinfo(title='Решение', message='Результат расчёта успешно скопирован!')
    except IndexError:
        showerror(title='Ошибка', message=f'Варианта не существует!')


dt = Tk()

dt.title("GS: Теоретическая механика")
dt.iconbitmap(default='icon_1.ico')
w = dt.winfo_screenwidth()
h = dt.winfo_screenheight()

wr = int(0.59*w)
hr = int(0.465*h)
dt.geometry(f"{wr}x{hr}")
canvas = Canvas(dt, height=hr, width=wr)
canvas.place(x=1, y=1)

dt.minsize(wr, hr)   # минимальные размеры: ширина - 200, высота - 150
dt.maxsize(wr, hr)   # максимальные размеры: ширина - 400, высота - 300

#константы для элементов
font_text = 10
width_text = int(0.015*w)
width_element = int(0.02*w)
heigth_element = int(0.0042*h)
row = [2, 10, 160, 330, 470]
line = [2, 15, 65, 115, 165, 215]

text_task = canvas.create_text(row[1], line[1], anchor='nw',font=("Arial", font_text), text="Выбор задачи", fill="Black")
text_var = canvas.create_text(row[1], line[2], anchor='nw', font=("Arial", font_text), text="Вариант задачи", fill="Black")
text_case = canvas.create_text(row[1], line[4], anchor='nw', font=("Arial", font_text), text="Решение:\nЗдесь будет приведены результаты расчёта",
                                   fill="Black")
tasks = Combobox(dt, width=int(0.95*width_element))
num_1 = Spinbox(dt, from_=0, to=9, width=int(0.35*width_element))
num_2 = Spinbox(dt, from_=0, to=9, width=int(0.35*width_element))
button = Button(text="Вычислить", height=1, width=10, font=("Arial", font_text), command=click)
butPrint = Button(text="Печать графика", height=1, width=12, font=("Arial", font_text), command=clicGraph)
butCopy = Button(text="Решение в буфер", height=1, width=13, font=("Arial", font_text), command=clickCopy)

tasks['values'] = ("Кинематика К1", "Кинематика К2", "Динамика Д1")
tasks.current(1)
tasks["background"] = '#ff0000'

graph(1,  tasks.get())

tasks.place(x=row[2], y=line[1])
num_1.place(x=row[2], y=line[2])
num_2.place(x=row[2]+96, y=line[2])
button.place(x=row[2]+79, y=line[3])
butPrint.place(x=row[1], y=line[3])
butCopy.place(x=row[2]-40, y=line[3])

dt.mainloop()
