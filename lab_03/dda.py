def DDA(x_start, y_start, x_end, y_end, count_steps = False):
    """
        Алгоритм цифрового дифференциального анализатора.
    """

    if (x_end - x_start == 0) and (y_end - y_start == 0):
        return [[x_start], [y_start]]

    diff = abs(x_end - x_start) if abs(x_end - x_start) > abs(y_end - y_start) \
                                 else abs(y_end - y_start)
    
    dx = (x_end - x_start) / diff
    dy = (y_end - y_start) / diff

    x = round(x_start)
    y = round(y_start)
    dots = [[x], [y]]
    steps = 0

    for _ in range(diff):
        x += dx
        y += dy

        dots[0].append(round(x))
        dots[1].append(round(y))

        if count_steps:
            if not ((round(x + dx) == round(x) and round(y + dy) != round(y)) or 
                    (round(x + dx) != round(x) and round(y + dy) == round(y))):
                steps += 1
    
    if count_steps:
        return steps

    return dots
