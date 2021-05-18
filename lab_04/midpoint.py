from math import sqrt

from draw import draw_dot
from reflection import symmetrical_reflection, reflection_x, reflection_y

def midpoint_circle(canvas, colour, center, radius, draw = True):
    """
        Построение окружности при помощи
        алгоритма средней точки.
    """

    points = []

    x = radius
    y = 0

    points.append([center[0] + x, center[1] + y])

    if draw:
        draw_dot(center[0] + x, center[1] + y, colour, canvas)

    f = 1 - radius

    while x > y:
        y += 1

        if f >= 0:
            x -= 1
            f -= x + x

        f += y + y + 1

        points.append([center[0] + x, center[1] + y])

        if draw:
            draw_dot(center[0] + x, center[1] + y, colour, canvas)

    if draw:
        symmetrical_reflection(points, center, colour, canvas)


def midpoint_ellipse(canvas, colour, center, a, b, draw = True):
    """
        Построение окружности при помощи
        алгоритма средней точки.
    """

    points = []

    sqr_a, sqr_b = a * a, b * b
    limit = round(a / sqrt(1 + sqr_b / sqr_a))
    x, y = 0, b

    if draw:
        draw_dot(x + center[0], y + center[1], colour, canvas)
    points.append([x + center[0], y + center[1]])

    f = sqr_b - round(sqr_a * (b - 1 / 4))
    while x < limit:
        if f > 0:
            y -= 1
            f -= 2 * sqr_a * y
        x += 1
        f += sqr_b * (2 * x + 1)
        points.append([x + center[0], y + center[1]])

        if draw:
            draw_dot(x + center[0], y + center[1], colour, canvas)

    limit = round(b / sqrt(1 + sqr_a / sqr_b))

    y, x = 0, a
    points.append([x + center[0], y + center[1]])

    if draw:
        draw_dot(x + center[0], y + center[1], colour, canvas)
    f = sqr_a - round(sqr_b * (a - 1 / 4))

    while y < limit:
        if f > 0:
            x -= 1
            f -= 2 * sqr_b * x
        y += 1
        f += sqr_a * (2 * y + 1)
        points.append([x + center[0], y + center[1]])

        if draw:
            draw_dot(x + center[0], y + center[1], colour, canvas)

    if draw:
        reflection_x(points, center, colour, canvas)
        reflection_y(points, center, colour, canvas)