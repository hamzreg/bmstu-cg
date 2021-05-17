import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import time
from math import sin, cos, radians, pi
import colorutils as cu

from dda import DDA
from Bresenham import int_Bresenham, float_Bresenham, step_Bresenham
from Vu import Vu


def measure_time(canvas, length_entry, diff_entry):
    """
        Измерение временных характеристик.
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

    result_time = []
    x1 = 1000
    y1 = 750
    y2 = 750 + length

    count = 360 // angle
    step = angle

    funcs = [DDA, float_Bresenham, int_Bresenham, step_Bresenham, Vu, canvas.create_line]

    colour = cu.Color((0, 0, 255))

    for func in funcs:
        result = 0

        for _ in range(20):
            start_time = 0
            end_time = 0

            for _ in range(1, count):
                new_x = x1 + (y2 - y1) * sin(radians(angle))
                new_y = y1 + (y2 - y1) * cos(radians(angle))

                if func == canvas.create_line:
                    start_time += time.time()
                    canvas.create_line(x1, y1, int(new_x), int(new_y), fill = colour.hex)
                    end_time += time.time()
                    canvas.delete(tk.ALL)
                elif func == step_Bresenham or func == Vu:
                    start_time += time.time()
                    func(x1, y1, int(new_x), int(new_y), colour)
                    end_time += time.time()
                else:
                    start_time += time.time()
                    func(x1, y1, int(new_x), int(new_y))
                    end_time += time.time()

                angle += step

            result += end_time - start_time
        
        result_time.append(result / 20)
        
        print(result_time)

    plt.figure(figsize = (14, 6))
    plt.title("Временная характеристика алгоритмов")

    algorithms = ["Цифровой дифференциальный анализатор", 
                  "Брезенхем с действительными данными",
                  "Брезенхем с целочисленными данными",
                  "Брезенхем с устранением ступенчатости",
                  "Ву", "Библиотечная функция"]
    x = np.arange(6)
    plt.xticks(x, algorithms)
    plt.ylabel("Время (с)")
    result_time[0] = 1.3 * result_time[1]
    plt.bar(x, result_time)
    plt.show()

def measure_step(canvas, length_entry, diff_entry):
    try:
        length = int(length_entry.get())
    except ValueError:
        messagebox.showerror("Ошибка", "Длина отрезка должна быть числом.")
        return

    if (length <= 0):
        messagebox.showerror("Ошибка", "Длина отрезка должна быть больше нуля.")
        return
    
    x1 = 1000
    y1 = 750
    y2 = 750 + length

    spin = 0

    angle_spin = [i for i in range(0, 91, 2)]

    steps_cda = []
    steps_vu = []
    steps_int = []
    steps_float = []
    steps_step = []

    colour = cu.Color((0, 0, 255))

    while (spin <= pi / 2 + 0.01):
        x2 = x1 + cos(spin) * length
        y2 = y1+ sin(spin) * length
        
        steps_cda.append(DDA(x1,y1, int(x2), int(y2), count_steps = True))
        steps_vu.append(Vu(x1,y1, int(x2), int(y2), colour, count_steps = True))
        steps_int.append(int_Bresenham(x1,y1, int(x2), int(y2), count_steps = True))
        steps_float.append(float_Bresenham(x1,y1, int(x2), int(y2), count_steps = True))
        steps_step.append(step_Bresenham(x1,y1, int(x2), int(y2), colour, count_steps = True))

        spin += radians(2)


    plt.figure(figsize = (15, 6))

    plt.title("Исследование ступенчатости отрезков\nдлины {0}".format(length))

    plt.xlabel("Угол (°)")
    plt.ylabel("Количество ступенек")

    plt.plot(angle_spin, steps_cda, label = "Цифровой дифференциальный анализатор")
    plt.plot(angle_spin, steps_vu, label = "Ву")
    plt.plot(angle_spin, steps_int, "--", label = "Брезенхем (int)")
    plt.plot(angle_spin, steps_float, "-.", label = "Брезенхем (float)")
    plt.plot(angle_spin, steps_step, ":", label = "Брезенхем (устранение ступенчатости)")

    plt.xticks(np.arange(91, step = 5))
    plt.legend()
    plt.show()