from math import sqrt, sin, cos, pi
from numpy import arange 

from draw import draw_dot
from reflection import symmetrical_reflection, reflection_x, reflection_y

def param_circle(canvas, colour, center, radius, draw = True):
    """
        Построение окружности при помощи
        параметрического уравнения.
    """

    points = []

    step = 1 / radius

    for t in arange(0, pi/4 + step, step):
        x = radius * cos(t) + center[0]
        y = radius * sin(t) + center[1]

        if draw:
            draw_dot(x, y, colour, canvas)
        points.append([x, y])

    if draw:
        symmetrical_reflection(points, center, colour, canvas)


def param_ellipse(canvas, colour, center, a, b, draw = True):
    """
        Построение окружности при помощи
        параметрического уравнения.
    """

    points = []

    step = 1 / max(a, b)

    for t in arange(0, pi/2 + step, step):
        x = a * cos(t) + center[0]
        y = b * sin(t) + center[1]

        if draw:
            draw_dot(x, y, colour, canvas)
        points.append([x, y])

    if draw:
        reflection_x(points, center, colour, canvas)
        reflection_y(points, center, colour, canvas)