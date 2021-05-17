from math import sqrt

from draw import draw_dot
from reflection import symmetrical_reflection, reflection_x, reflection_y

def canon_circle(canvas, colour, center, radius):
    """
        Построение окружности при помощи
        канонического уравнения.
    """

    points = []

    for x in range(center[0], round(center[0] + radius / sqrt(2) + 1)):
        y = center[1] + sqrt(radius ** 2 - (x - center[0]) ** 2)
        draw_dot(x, y, colour, canvas)
        points.append([x, y])

    symmetrical_reflection(points, center, colour, canvas)


def canon_ellipse(canvas, colour, center, a, b):
    """
        Построение окружности при помощи
        канонического уравнения.
    """

    points = []

    for x in range(0, a + 1):
        y = round(sqrt(1 - (x / a) ** 2) * b)
        draw_dot(x + center[0], y + center[1], colour, canvas)
        points.append([x + center[0], y + center[1]])

    for y in range(0, b + 1):
        x = round(sqrt(1 - (y / b)**2) * a)
        draw_dot(x + center[0], y + center[1], colour, canvas)
        points.append([center[0] + x, center[1] + y])

    reflection_x(points, center, colour, canvas)
    reflection_y(points, center, colour, canvas)
