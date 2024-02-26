from random import uniform
from math import cos, sin, pi, atan
rad = lambda alpha: alpha * pi / 180

def task_1() -> str | float | str:
    URL = True
    n = round(uniform(2.1, 500.1), 1)
    F1 = round(uniform(2.1, 500.1), 1)
    F2 = round(uniform(2.1, 500.1), 1)
    F3 = round(uniform(2.1, 500.1), 1)
    alpha = round(uniform(5.2, 60.7), 1)
    text = f'''Определить модуль равнодействующей.
F1 = {F1} Н, F2 = {F2} Н, F3 = {F3} Н, ​α = {alpha}°.
Модуль R, Н округлить до десятых.
    '''
    result = F2 + F1 + F3 * cos(rad(alpha))
    return text, round(result, 1), URL

print(task_9())
