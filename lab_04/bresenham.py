from draw import draw_dot
from reflection import symmetrical_reflection, reflection_x, reflection_y

def bresenham_circle(canvas, colour, center, radius, draw = True):
    """
        Построение окружности при помощи
        алгоритма Брезенхема.
    """

    points = []

    x = 0
    y = radius
    points.append([x + center[0], y + center[1]])

    if draw:
        draw_dot(x + center[0], y + center[1], colour, canvas)
    delta = 2 - radius - radius

    while x < y:
        if delta <= 0:
            d1 = delta + delta + y + y - 1
            x += 1
            if d1 >= 0:
                y -= 1
                delta += 2 * (x - y + 1)
            else:
                delta += x + x + 1

        else:
            d2 = 2 * (delta - x) - 1
            y -= 1
            if d2 < 0:
                x += 1
                delta += 2 * (x - y + 1)
            else:
                delta -= y + y - 1
        points.append([x + center[0], y + center[1]])

        if draw:
            draw_dot(x + center[0], y + center[1], colour, canvas)

    if draw:
        symmetrical_reflection(points, center, colour, canvas)


def bresenham_ellipse(canvas, colour, center, a, b, draw = True):
    """
        Построение эллипса при помощи
        алгоритма Брезенхема.
    """

    points = []

    x = 0
    y = b
    sqr_b = b * b
    sqr_a = a * a
    points.append([x + center[0], y + center[1]])

    if draw:
        draw_dot(x + center[0], y + center[1], colour, canvas)
    delta = sqr_b - sqr_a * (b + b + 1)

    while y > 0:
        if delta <= 0:
            d1 = delta + delta + sqr_a * (y + y - 1)
            x += 1
            delta += sqr_b * (x + x + 1)
            if d1 >= 0:
                y -= 1
                delta += sqr_a * (-y - y + 1)

        else:
            d2 = delta + delta + sqr_b * (-x - x - 1)
            y -= 1
            delta += sqr_a * (-y - y + 1)
            if d2 < 0:
                x += 1
                delta += sqr_b * (x + x + 1)
        points.append([x + center[0], y + center[1]])

        if draw:
            draw_dot(x + center[0], y + center[1], colour, canvas)

    if draw:
        reflection_x(points, center, colour, canvas)
        reflection_y(points, center, colour, canvas)