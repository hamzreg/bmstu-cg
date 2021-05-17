from math import sqrt, sin, cos, pi
from numpy import arange 

from draw import draw_dot
from reflection import symmetrical_reflection, reflection_x, reflection_y

def param_circle(canvas, colour, center, radius):
    """
        Построение окружности при помощи
        параметрического уравнения.
    """

    points = []

    step = 1 / radius

    for t in arange(0, pi/4 + step, step):
        x = radius * cos(t) + center[0]
        y = radius * sin(t) + center[1]

        draw_dot(x, y, colour, canvas)
        points.append([x, y])

    symmetrical_reflection(points, center, colour, canvas)


def param_ellipse(canvas, colour, center, a, b):
    """
        Построение окружности при помощи
        параметрического уравнения.
    """

    points = []

    step = 1 / max(a, b)

    for t in arange(0, pi/2 + step, step):
        x = a * cos(t) + center[0]
        y = b * sin(t) + center[1]

        draw_dot(x, y, colour, canvas)
        points.append([x, y])

    reflection_x(points, center, colour, canvas)
    reflection_y(points, center, colour, canvas)