from dda import DDA
from Bresenham import float_Bresenham, int_Bresenham, step_Bresenham
from Vu import Vu

from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox
from math import sin, cos, radians
import colorutils as cu

@dataclass
class Constants:
    x_center = 1000
    y_center = 750


def draw_intens(canvas, dots):

    for i in range(len(dots[0])):
        canvas.create_line(dots[0][i], dots[1][i],
                           dots[0][i] + 1, dots[1][i],
                           fill = dots[2][i].hex)

def draw_dots(canvas, dots, colour):
    """
        Рисование точек.
    """

    for i in range(len(dots[0])):
        canvas.create_line(dots[0][i], dots[1][i],
                           dots[0][i] + 1, dots[1][i],
                           fill = colour.hex)


def draw_section(canvas, algorithms, colours, x_start_entry, x_end_entry, y_start_entry, y_end_entry):
    """
        Рисование отрезка.
    """

    index_algorithm = algorithms.curselection()[0]
    algorithm = algorithms.get(index_algorithm)

    index_colour = colours.curselection()[0]
    colour = colours.get(index_colour)

    try:
        x_start = int(x_start_entry.get())
        y_start = int(y_start_entry.get())

        x_end = int(x_end_entry.get())
        y_end = int(y_end_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Координаты отрезка должны быть числами.")
        return
    
    if colour == "Синий":
        colour = cu.Color((0, 0, 255))
    else:
        colour = cu.Color((255, 255, 255))

    if algorithm == "Цифровой дифференциальный анализатор":
        dots = DDA(x_start, y_start, x_end, y_end)
    elif algorithm == "Брезенхем с действительными данными":
        dots = float_Bresenham(x_start, y_start, x_end, y_end)
    elif algorithm == "Брезенхем с целочисленными данными":
        dots = int_Bresenham(x_start, y_start, x_end, y_end)
    elif algorithm == "Брезенхем с устранением ступенчатости":
        dots = step_Bresenham(x_start, y_start, x_end, y_end, colour)
        draw_intens(canvas, dots)
        return
    elif algorithm == "Ву":
        dots = Vu(x_start, y_start, x_end, y_end, colour)
        draw_intens(canvas, dots)
        return
    elif algorithm == "Библиотечная функция":
        canvas.create_line(x_start, y_start, x_end, y_end, fill = colour.hex)
        return

    draw_dots(canvas, dots, colour)
    

def draw_spectr(canvas, algorithms, colours, length_entry, diff_entry):
    """
        Рисование отрезков в заданном спектре углов.
    """

    try:
        length = int(length_entry.get())
        angle = int(diff_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Длина отрезка и угол спектра должны быть числами.")
        return

    if (length <= 0):
        messagebox.showerror("Ошибка", "Длина отрезка должна быть больше нуля.")
        return

    if (angle <= 0):
        messagebox.showerror("Ошибка", "Угол должен быть больше нуля.")
        return

    
    x_start = 1000
    y_start = 750
    x_end = 1000
    y_end = 750 + length

    count = 360 // angle
    step = angle

    index_algorithm = algorithms.curselection()[0]
    algorithm = algorithms.get(index_algorithm)

    index_colour = colours.curselection()[0]
    colour = colours.get(index_colour)
    
    if colour == "Синий":
        colour = cu.Color((0, 0, 255))
    else:
        colour = cu.Color((255, 255, 255))

    if algorithm == "Цифровой дифференциальный анализатор":
        func = DDA
    elif algorithm == "Брезенхем с действительными данными":
        func = float_Bresenham
    elif algorithm == "Брезенхем с целочисленными данными":
        func = int_Bresenham
    elif algorithm == "Брезенхем с устранением ступенчатости":
        func = step_Bresenham
    elif algorithm == "Ву":
        func = Vu
    elif algorithm == "Библиотечная функция":
        func = canvas.create_line
    
    spectr = [[x_start, y_start, x_end, y_end]]

    for _ in range(1, count):
        new_x_end = Constants.x_center + (y_end - Constants.y_center) * sin(radians(angle))
        new_y_end = Constants.y_center + (y_end - Constants.y_center) * cos(radians(angle))

        angle += step
        dots = [int(x_start), int(y_start), int(new_x_end), int(new_y_end)]
        spectr.append(dots)
    
    for dots in spectr:
        if func == canvas.create_line:
            canvas.create_line(dots[0], dots[1], dots[2], dots[3], fill = colour.hex)
        elif func == step_Bresenham or func == Vu:
            points = func(dots[0], dots[1], dots[2], dots[3], colour)
            draw_intens(canvas, points)
        else:
            points = func(dots[0], dots[1], dots[2], dots[3])
            draw_dots(canvas, points, colour)

def clear_canvas(canvas):
    canvas.delete(tk.ALL)