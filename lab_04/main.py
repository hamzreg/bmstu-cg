from dataclasses import dataclass
import tkinter as tk
import time
from tkinter import messagebox
import matplotlib.pyplot as plt

from draw import clear_canvas
from canon import canon_circle, canon_ellipse
from parametric import param_circle, param_ellipse
from bresenham import bresenham_circle, bresenham_ellipse
from midpoint import midpoint_circle, midpoint_ellipse

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 4"

    font_bold = "FreeMono 12 bold"
    font = "FreeMono 12"

    canvas_heigth = 1500
    canvas_width = 1800


@dataclass
class Colour:

    back = "#ABCDEF"
    draw = "#3E8353"
    button = "#DDF1FF"
    text = "#28852F"

@dataclass
class Methods:

    canon = 0
    param = 1
    bresenham = 2
    midpoint = 3
    library = 4


def get_method():
    """
        Выбор метода построения.
    """

    for i in algorithm_list.curselection():
        index = int(i)
    method = algorithm_list.get(index)

    if method == "Каноническое ур-ие":
        return Methods.canon
    elif method == "Параметрическое ур-ие":
        return Methods.param
    elif method == "Алгоритм Брезенхема":
        return Methods.bresenham
    elif method == "Алгоритм средней точки":
        return Methods.midpoint
    elif method == "Библиотечная функция":
        return Methods.library


def get_colour():
    """
        Выбор цвета построения.
    """

    for i in colour_list.curselection():
        index = int(i)
    colour = colour_list.get(index)

    if colour == "Синий":
        return "blue"
    elif colour == "Зелёный":
        return "green"
    elif colour == "Чёрный":
        return "black"
    elif colour == "Белый(фоновый)":
        return "white"


def get_count_fig():
    """
        Ввод числа фигур.
    """

    try:
        count_fig = int(count_fig_etr.get())

        return count_fig
    except:
        messagebox.showerror("Ошибка", "Число фигур должно быть числом.")
        return


def get_step():
    """
        Ввод шага спектра.
    """

    try:
        step = int(step_etr.get())

        return step
    except:
        messagebox.showerror("Ошибка", "Шаг должен быть числом.")
        return


def get_spectr_center():
    """
        Ввод координат центра спектра.
    """

    try:
        center_x = int(center_x_etr.get())
        center_y = int(center_y_etr.get())

        return [center_x, center_y]
    except:
        messagebox.showerror("Ошибка", "Координаты центра должны быть вещественными числами.")
        return


def draw_ellipse_spectr(method, colour, center, step, count_fig, a, b, change_axis):
    """
        Рисование спектра эллипсов.
    """

    factor1 = a / b
    factor2 = b / a
    i = 0

    while i < count_fig:
        draw_ellipse(method, colour, center, round(a), round(b))

        if change_axis == 0:
            a += step
            b = a * factor2
        else:
            b += step
            a = b * factor1
        
        i += 1


def get_change_axis():
    """
        Выбор оси для изменения
    """

    for i in axis_list.curselection():
        index = int(i)
    axis = axis_list.get(index)

    if axis == "Полуось a":
        return 0
    elif axis == "Полуось b":
        return 1


def get_start_axises():
    """
        Получение начальных значений полуосей.
    """

    try:
        a = int(start_r_a_etr.get())
        b = int(start_r_b_etr.get())

        return a, b
    except:
        messagebox.showerror("Ошибка", "Полуоси должны быть целыми числами.")
        return


def create_ellipse_spectr():
    """
        Создание спектра эллипсов.
    """

    method = get_method()
    colour = get_colour()
    center = get_spectr_center()
    step = get_step()
    count_fig = get_count_fig()
    a, b = get_start_axises()
    change_axis = get_change_axis()

    draw_ellipse_spectr(method, colour, center, step, count_fig, a, b, change_axis)


def draw_circle_spectr_step(method, colour, center, step, start_r, end_r):
    """
        Рисование спектра окружностей.
    """

    i = 0
    r = start_r
    count_fig = (end_r - start_r) // step + 1

    while i < count_fig:
        draw_circle(method, colour, center, r)
        r += step
        i += 1


def draw_circle_spectr_count_fig(method, colour, center, count_fig, start_r, end_r):
    """
        Рисование спектра окружностей.
    """

    i = 0
    r = start_r
    step = (end_r - start_r) // (count_fig - 1)

    while i < count_fig:
        draw_circle(method, colour, center, r)
        r += step
        i += 1


def draw_circle_spectr_start_r(method, colour, center, step, count_fig, start_r):
    """
        Рисование спектра окружностей.
    """
    i = 0

    while i < count_fig:
        draw_circle(method, colour, center, start_r)

        start_r += step
        i += 1


def draw_circle_spectr_end_r(method, colour, center, step, count_fig, end_r):
    """
        Рисование спектра окружностей.
    """
    i = 0

    while i < count_fig:
        draw_circle(method, colour, center, end_r)

        end_r -= step
        i += 1


def get_end_radius():
    """
        Ввод конечного радиуса.
    """

    try:
       end_radius = int(end_r_etr.get())

       return end_radius
    except:
        messagebox.showerror("Ошибка", "Радиус должен быть числом.")
        return


def get_start_radius():
    """
        Ввод начального радиуса.
    """

    try:
        start_radius = int(start_r_etr.get())

        return start_radius
    except:
        messagebox.showerror("Ошибка", "Радиус должен быть числом.")
        return


def get_not_used():
    """
        Выбор не используемого при
        построении спектра окружностей.
    """

    for i in param_list.curselection():
        index = int(i)
    not_used = param_list.get(index)

    if not_used == "Начальный радиус":
        return 0
    elif not_used == "Конечный радиус":
        return 1
    elif not_used == "Шаг":
        return 2
    elif not_used == "Число окружностей":
        return 3


def create_circle_spectr():
    """
        Создание спектра окружностей.
    """

    method = get_method()
    colour = get_colour()
    center = get_spectr_center()

    not_used = get_not_used()

    if not_used == 0:
        end_radius = get_end_radius()
        step = get_step()
        count_fig = get_count_fig()
        draw_circle_spectr_end_r(method, colour, center, step, count_fig, end_radius)
    elif not_used == 1:
        start_radius = get_start_radius()
        step = get_step()
        count_fig = get_count_fig()
        draw_circle_spectr_start_r(method, colour, center, step, count_fig, start_radius)
    elif not_used == 2:
        start_radius = get_start_radius()
        end_radius = get_end_radius()
        count_fig = get_count_fig()
        draw_circle_spectr_count_fig(method, colour, center, count_fig, start_radius, end_radius)
    elif not_used == 3:
        start_radius = get_start_radius()
        end_radius = get_end_radius()
        step = get_step()
        draw_circle_spectr_step(method, colour, center, step, start_radius, end_radius)


def get_center():
    """
        Ввод координат центра.
    """

    try:
        center_x = int(x_entry.get())
        center_y = int(y_entry.get())

        return [center_x, center_y]
    except:
        messagebox.showerror("Ошибка", "Координаты центра должны быть вещественными числами.")
        return


def draw_ellipse(method, colour, center, a, b):
    """
        Рисование эллипса.
    """

    if method == Methods.canon:
        canon_ellipse(canvas, colour, center, a, b)
    elif method == Methods.param:
        param_ellipse(canvas, colour, center, a, b)
    elif method == Methods.bresenham:
        bresenham_ellipse(canvas, colour, center, a, b)
    elif method == Methods.midpoint:
        midpoint_ellipse(canvas, colour, center, a, b)
    elif method == Methods.library:
        canvas.create_oval(center[0] - a, center[1] - b,
                           center[0] + a, center[1] + b,
                           outline= colour)
def get_axises():
    """
        Получение значений полуосей.
    """

    try:
        a = int(r_a_entry.get())
        b = int(r_b_entry.get())

        return a, b
    except:
        messagebox.showerror("Ошибка", "Полуоси должны быть целыми числами.")
        return



def create_ellipse():
    """
        Создание эллипса.
    """

    method = get_method()
    colour = get_colour()
    center = get_center()
    a, b = get_axises()

    draw_ellipse(method, colour, center, a, b)


def get_radius():
    """
        Ввод радиуса.
    """

    try:
        radius = int(circle_r_entry.get())

        return radius
    except:
        messagebox.showerror("Ошибка", "Радиус должен быть числом.")
        return


def draw_circle(method, colour, center, radius):
    """
        Рисование окружности.
    """

    if method == Methods.canon:
        canon_circle(canvas, colour, center, radius)
    elif method == Methods.param:
        param_circle(canvas, colour, center, radius)
    elif method == Methods.bresenham:
        bresenham_circle(canvas, colour, center, radius)
    elif method == Methods.midpoint:
        midpoint_circle(canvas, colour, center, radius)
    elif method == Methods.library:
        canvas.create_oval(center[0] - radius, center[1] - radius,
                           center[0] + radius, center[1] + radius,
                           outline= colour)

def create_circle():
    """
        Создание окружности.
    """

    method = get_method()
    colour = get_colour()
    center = get_center()
    radius = get_radius()

    draw_circle(method, colour, center, radius)


def compare_methods_ellipse():
    """
       Графики зависимости времени 
       работы алгоритма от радиуса.
    """
    plt.title("Зависимость времени работы алгоритма от изменения полуоси")

    start_a = 1000
    start_b = 500
    factor = start_b / start_a

    step = 1000
    count_fig = 20

    colour = "white"
    xc = 900
    yc = 750

    axises = [start_a + i * step for i in range(count_fig)]

    times = []
    methods = [canon_ellipse, param_ellipse, bresenham_ellipse, midpoint_ellipse]

    for i in range(len(algorithms)):
        times.append(list())

        for a in axises:
            if i != 4:
                b = round(a * factor)
                start_time = time.time()
                methods[i](canvas, colour, [xc, yc], a, b)
                times[-1].append((time.time() - start_time))
            else:
                b = round(a * factor)
                start_time = time.time()
                canvas.create_oval(xc - a, yc - b,
                           xc + a, yc + b,
                           outline= colour)
                times[-1].append((time.time() - start_time))

    for i in range(len(algorithms)):
        plt.plot(axises, times[i], label= algorithms[i])

    plt.legend()

    plt.xlabel("Полуось", fontsize = 20) 
    plt.ylabel("Время", fontsize = 20)

    plt.grid()
    plt.show()


def compare_methods_circle():
    """
       Графики зависимости времени 
       работы алгоритма от радиуса.
    """
    plt.title("Зависимость времени работы алгоритма от радиуса")

    start_radius = 500
    step = 1000
    count_fig = 20
    colour = "white"
    xc = 900
    yc = 750
    radiuses = [start_radius + i * step for i in range(count_fig)]
    times = []
    methods = [canon_circle, param_circle, bresenham_circle, midpoint_circle]

    for i in range(len(algorithms)):
        times.append(list())

        for r in radiuses:
            if i != 4:
                start_time = time.time()
                methods[i](canvas, colour, [xc, yc], r)
                times[-1].append((time.time() - start_time))
            else:
                start_time = time.time()
                canvas.create_oval(xc - r, yc - r,
                           xc + r, yc + r,
                           outline= colour)
                times[-1].append((time.time() - start_time))

    for i in range(len(algorithms)):
        plt.plot(radiuses, times[i], label= algorithms[i])

    plt.legend(fontsize = 20)

    plt.xlabel("Радиус", fontsize = 20) 
    plt.ylabel("Время", fontsize = 20)

    plt.grid()
    plt.show()


if __name__ == "__main__":

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Холст

    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = "white")
    canvas.place(x = 50, y = 20)

    # Выбор алгоритма

    algorithm_lbl = tk.Label(window, text = "АЛГОРИТМ",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    algorithm_lbl.place(x = 1900, y = 20)

    algorithms = ["Каноническое ур-ие", 
                  "Параметрическое ур-ие",
                  "Алгоритм Брезенхема",
                  "Алгоритм средней точки",
                  "Библиотечная функция"]
    algorithm_list = tk.Listbox(selectmode = tk.SINGLE,
                               exportselection = False,
                             height = 5,
                             width = 24,
                             bd = 6,
                             font = Graphic.font)
    algorithm_list.place(x = 1900, y = 70)

    for algorithm in algorithms:
        algorithm_list.insert(tk.END, algorithm)

    # Выбор цвета

    colour_lbl = tk.Label(window, text = "ЦВЕТ",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_lbl.place(x = 2440, y = 20)

    colours = ["Синий", "Белый(фоновый)"]
    colour_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 2,
                             width = 24,
                             bd = 6,
                             font = Graphic.font)
    colour_list.place(x = 2440, y = 70)

    for colour in colours:
        colour_list.insert(tk.END, colour)

    # Ввод координат центра

    center_lbl = tk.Label(window, text = "КООРДИНАТЫ ЦЕНТРА ФИГУРЫ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    center_lbl.place(x = 2150, y = 290)

    x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_lbl.place(x = 2100, y = 350)

    y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    y_lbl.place(x = 2440, y = 350)

    x_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    x_entry.insert(tk.END, "900")
    x_entry.place(x = 2200, y = 350)

    y_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    y_entry.insert(tk.END, "750")
    y_entry.place(x = 2540, y = 350)

    # Построение окружности

    circle_lbl = tk.Label(window, text = "ОКРУЖНОСТЬ",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    circle_lbl.place(x = 1900, y = 450)

    circle_r_lbl = tk.Label(window, text = "R:",
                             font = Graphic.font,
                             bg = Colour.back)
    circle_r_lbl.place(x = 1900, y = 510)

    circle_r_entry = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    circle_r_entry.insert(tk.END, "300")
    circle_r_entry.place(x = 2000, y = 510)

    circle_button = tk.Button(window, font = Graphic.font,
                                      width = 23,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Построить окружность",
                                      command= create_circle)
    circle_button.place(x = 1900, y = 630)

    # Ввод радиусов

    r_lbl = tk.Label(window, text = "ЭЛЛИПС",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    r_lbl.place(x = 2440, y = 450)


    r_a_lbl = tk.Label(window, text = "R полуоси a:",
                             font = Graphic.font,
                             bg = Colour.back)
    r_a_lbl.place(x = 2440, y = 510)

    r_a_entry = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    r_a_entry.insert(tk.END, "300")
    r_a_entry.place(x = 2750, y = 510)

    r_b_lbl = tk.Label(window, text = "R полуоси b:",
                             font = Graphic.font,
                             bg = Colour.back)
    r_b_lbl.place(x = 2440, y = 570)

    r_b_entry = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    r_b_entry.insert(tk.END, "150")
    r_b_entry.place(x = 2750, y = 570)

    ellipse_button = tk.Button(window, font = Graphic.font,
                                      width = 23,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Построить эллипс",
                                      command= create_ellipse)
    ellipse_button.place(x = 2440, y = 630)

    # Спектр

    spectr_lbl = tk.Label(window, text = "СПЕКТР",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    spectr_lbl.place(x = 2350, y = 730)

    center_x_lbl = tk.Label(window, text = "X центра",
                             font = Graphic.font,
                             bg = Colour.back)
    center_x_lbl.place(x = 1900, y = 790)

    center_x_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    center_x_etr.insert(tk.END, "900")
    center_x_etr.place(x = 1900, y = 850)

    center_y_lbl = tk.Label(window, text = "Y центра",
                             font = Graphic.font,
                             bg = Colour.back)
    center_y_lbl.place(x = 2210, y = 790)

    center_y_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    center_y_etr.insert(tk.END, "750")
    center_y_etr.place(x = 2210, y = 850)

    step_lbl = tk.Label(window, text = "Шаг",
                             font = Graphic.font,
                             bg = Colour.back)
    step_lbl.place(x = 2440, y = 790)

    step_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    step_etr.insert(tk.END, "50")
    step_etr.place(x = 2440, y = 850)

    count_fig_lbl = tk.Label(window, text = "Число фигур",
                             font = Graphic.font,
                             bg = Colour.back)
    count_fig_lbl.place(x = 2700, y = 790)

    count_fig_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    count_fig_etr.insert(tk.END, "5")
    count_fig_etr.place(x = 2750, y = 850)

    # Для окружности

    circle_spectr_lbl = tk.Label(window, text = "СПЕКТР ОКРУЖНОСТЕЙ",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    circle_spectr_lbl.place(x = 1900, y = 910)

    start_r_lbl = tk.Label(window, text = "Rн",
                             font = Graphic.font,
                             bg = Colour.back)
    start_r_lbl.place(x = 1900, y = 970)

    start_r_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    start_r_etr.insert(tk.END, "100")
    start_r_etr.place(x = 1900, y = 1030)

    end_r_lbl = tk.Label(window, text = "Rк",
                             font = Graphic.font,
                             bg = Colour.back)
    end_r_lbl.place(x = 2210, y = 970)

    end_r_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    end_r_etr.insert(tk.END, "300")
    end_r_etr.place(x = 2210, y = 1030)

    param_lbl = tk.Label(window, text = "Не используем:",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    param_lbl.place(x = 1900, y = 1090)

    params = ["Начальный радиус", "Конечный радиус", "Шаг", "Число окружностей"]

    param_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 4,
                             width = 24,
                             bd = 6,
                             font = Graphic.font)
    param_list.place(x = 1900, y = 1150)

    for param in params:
        param_list.insert(tk.END, param)

    circle_spectr_button = tk.Button(window, font = Graphic.font,
                                    width = 23,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Построить спектр\n окружностей", 
                                    command= create_circle_spectr)
    circle_spectr_button.place(x = 1900, y = 1340) 

    # Для эллипса

    circle_spectr_lbl = tk.Label(window, text = "СПЕКТР ЭЛЛИПСОВ",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    circle_spectr_lbl.place(x = 2440, y = 910)

    start_r_a_lbl = tk.Label(window, text = "Полуось a",
                             font = Graphic.font,
                             bg = Colour.back)
    start_r_a_lbl.place(x = 2440, y = 970)

    start_r_a_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    start_r_a_etr.insert(tk.END, "200")
    start_r_a_etr.place(x = 2440, y = 1030)

    start_r_b_lbl = tk.Label(window, text = "Полуось b",
                             font = Graphic.font,
                             bg = Colour.back)
    start_r_b_lbl.place(x = 2730, y = 970)

    start_r_b_etr = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    start_r_b_etr.insert(tk.END, "100")
    start_r_b_etr.place(x = 2750, y = 1030)

    axis_lbl = tk.Label(window, text = "Изменяем:",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    axis_lbl.place(x = 2440, y = 1090)

    axises = ["Полуось a", "Полуось b"]

    axis_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 2,
                             width = 24,
                             bd = 6,
                             font = Graphic.font)
    axis_list.place(x = 2440, y = 1150)

    for axis in axises:
        axis_list.insert(tk.END, axis)
    
    ellipse_spectr_button = tk.Button(window, font = Graphic.font,
                                    width = 23,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Построить спектр\nэллипсов",
                                    command= create_ellipse_spectr)
    ellipse_spectr_button.place(x = 2440, y = 1340) 

    # Исследование временной характеристики

    time_circle_button = tk.Button(window, font = Graphic.font,
                                    width = 23,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Сравнение алгоритмов\nдля окружности",
                                    command= compare_methods_circle)
    time_circle_button.place(x = 1900, y = 1460)

    time_ellipse_button = tk.Button(window, font = Graphic.font,
                                    width = 23,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Сравнение алгоритмов\n для эллипса",
                                    command= compare_methods_ellipse)
    time_ellipse_button.place(x = 2440, y = 1460)

    # Очистить экран

    clear_button = tk.Button(window, font = Graphic.font,
                                    width = 23,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Очистить экран",
                                    command = lambda : clear_canvas(canvas))
    clear_button.place(x = 50, y = 1535) 

    window.mainloop()
