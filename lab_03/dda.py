def DDA(x_start, y_start, x_end, y_end):
    """
        Алгоритм цифрового дифференциального анализатора.
    """

    diff = abs(x_end - x_start) if abs(x_end - x_start) > abs(y_end - y_start) \
                                 else abs(y_end - y_start)
    
    dx = (x_end - x_start) / diff
    dy = (y_end - y_start) / diff

    x = x_start
    y = y_start
    dots = [[x], [y]]

    for _ in range(diff):
        x += dx
        y += dy

        dots[0].append(x)
        dots[1].append(y)
    
    return dots
