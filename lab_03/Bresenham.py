from math import fabs
from math_funcs import sign

def float_Bresenham(x_start, y_start, x_end, y_end):
    """
        Алгоритм Брезенхема с действительными данными.
    """

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
    
    m = dy / dx
    error = m - 0.5

    dots = [[], []]

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)

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
    
    return dots


def int_Bresenham(x_start, y_start, x_end, y_end):
    """
        Алгоритм Брезнхема с целочисленными значениями.
    """

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

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)

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
    
    return dots

def step_Bresenham(x_start, y_start, x_end, y_end):
    """
        Алгоритм Брезенхема с устранением ступенчатости.
    """

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

    m = dy / dx
    error = 0.5
    w = 1 - m

    dots = [[], []]

    x = x_start
    y = y_start

    for _ in range(dx + 1):
        dots[0].append(x)
        dots[1].append(y)

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
    
    return dots
