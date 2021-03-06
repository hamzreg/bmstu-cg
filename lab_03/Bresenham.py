from utils import change_colour
from math import fabs
from math_funcs import sign

def float_Bresenham(x_start, y_start, x_end, y_end, count_steps = False):
    """
        Алгоритм Брезенхема с действительными данными.
    """

    if (x_end - x_start == 0) and (y_end - y_start == 0):
        return [[x_start], [y_start]]

    dx = x_end - x_start
    dy = y_end - y_start

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dx < dy:
        dx, dy = dy, dx
        change = 1
    else:
        change = 0
    
    m = dy / dx # тангенс угла наклона отрезка
    error = m - 0.5 # удобнее анализировать знак ошибки, так истинное значение ошибки смещается на -0,5

    dots = [[], []]
    steps = 0

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)

        add_x = x
        add_y = y

        if error >= 0:
            if change:
                x += x_sign
            else:
                y += y_sign
            
            error -= 1
        
        if change:
            y += y_sign
        else:
            x += x_sign
        
        error += m

        if count_steps:
            if not((add_x == x and add_y != y) or
                    (add_x != x and add_y == y)):
                steps += 1
    
    if count_steps:
        return steps

    return dots


def int_Bresenham(x_start, y_start, x_end, y_end, count_steps = False):
    """
        Алгоритм Брезнхема с целочисленными значениями.
    """

    if (x_end - x_start == 0) and (y_end - y_start == 0):
        return [[x_start], [y_start]]

    dx = x_end - x_start
    dy = y_end - y_start

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        change = 1
    else:
        change = 0

    error = 2 * dy - dx

    dots = [[], []]
    steps = 0

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)

        add_x = x
        add_y = y

        if error >= 0:
            if change:
                x += x_sign
            else:
                y += y_sign
            
            error -= 2 * dx

        if change:
            y += y_sign
        else:
            x += x_sign
            
        error += 2 * dy
    
        if count_steps:
            if (add_x != x and add_y != y):
                steps += 1
    
    if count_steps:
        return steps

    return dots


def step_Bresenham(x_start, y_start, x_end, y_end, colour, count_steps = False):
    """
        Алгоритм Брезенхема с устранением ступенчатости.
    """

    if (x_end - x_start == 0) and (y_end - y_start == 0):
        return [[x_start], [y_start], [colour]]

    dx = x_end - x_start
    dy = y_end - y_start

    x_sign = sign(dx)
    y_sign = sign(dy)

    dx, dy = abs(dx), abs(dy)

    if dy > dx:
        dx, dy = dy, dx
        change = 1
    else:
        change = 0

    intensity = 255
    m = dy / dx # тангенс угла наклона отрезка
    error = 0.5 * intensity
    m *= intensity
    w = intensity - m 

    dots = [[], [], []]
    steps = 0

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)
        dots[2].append(change_colour(colour, round(error)))

        add_x = x
        add_y = y

        if (error > w):
            x += x_sign
            y += y_sign
            
            error -= w
        else:
            if change:
                y += y_sign
            else:
                x += x_sign
            
            error += m

        if count_steps:
            if not((add_x == x and add_y != y) or
                    (add_x != x and add_y == y)):
                steps += 1
    
    if count_steps:
        return steps

    return dots
