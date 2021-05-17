from utils import change_colour
from math import fabs, floor

from math_funcs import sign

def Vu(x_start, y_start, x_end, y_end, colour, count_steps = False):

    if (x_end - x_start == 0) and (y_end - y_start == 0):
        return [[x_start], [y_start]]

    dx = x_end - x_start
    dy = y_end - y_start

    step = 1
    intensity = 255

    dots = [[], [], []]
    steps = 0

    if (fabs(dy) > fabs(dx)):
        m = dx / dy
        add_m = m
    

        if (y_start > y_end):
            add_m *= -1
            step *= -1

        end_y = round(y_end) - 1 if (dy < dx) else (round(y_end) + 1)

        for y in range(round(y_start), end_y, step):
            diff = x_start - floor(x_start)

            first = [int(x_start) + 1, y, change_colour(colour, round(fabs(1 - diff) * intensity))]
            second = [int(x_start), y, change_colour(colour, round(fabs(diff) * intensity))]

            dots[0].append(first[0])
            dots[1].append(first[1])
            dots[2].append(first[2])

            dots[0].append(second[0])
            dots[1].append(second[1])
            dots[2].append(second[2])

            if count_steps and y < y_end:
                if (int(x_start) != int(x_start + m)):
                    steps += 1

            x_start += add_m
    
    else:
        m = dy / dx
        add_m = m

        if (x_start > x_end):
            add_m *= -1
            step *= -1

        end_x = round(x_end) - 1 if (dy > dx) else (round(x_end) + 1)

        for x in range(round(x_start), end_x, step):
            diff = y_start - floor(y_start)

            first = [x, int(y_start) + 1, change_colour(colour, round(fabs(1 - diff) * intensity))]
            second = [x, int(y_start), change_colour(colour, round(fabs(diff) * intensity))]

            dots[0].append(first[0])
            dots[1].append(first[1])
            dots[2].append(first[2])

            dots[0].append(second[0])
            dots[1].append(second[1])
            dots[2].append(second[2])

            if count_steps and x < x_end:
                if (int(y_start) != int(y_start + m)):
                    steps += 1

            y_start += add_m
    
    if count_steps:
        return steps

    return dots
