from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

from tkinter.constants import Y
import matplotlib.pyplot as plt
from numpy import arange

from math import pi, sin, cos

from numpy.core.fromnumeric import transpose

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 10"

    font_bold = "FreeMono 14 bold"
    font = "FreeMono 14"

    canvas_heigth = 1500
    canvas_width = 1800

@dataclass
class Colour:
    """
        Цвета.
    """

    back = "#ABCDEF"
    draw = "#3E8353"
    button = "#DDF1FF"
    text = "#28852F"

    black = "#000000"
    white = "#FFFFFF"
    red = "#FF0000"
    green = "#00FF00"
    blue = "#0000FF"


X_DOT = 0
Y_DOT = 1
Z_DOT = 2

FROM = 0
TO = 1
STEP = 2

FROM_SPIN_BOX = -1000.0
TO_SPIN_BOX = 1000.0
STEP_SPIN_BOX = 0.1

DEFAULT_SCALE = 45
DEFAULT_ANGLE = 30


trans_matrix = []

# Операции
def create_trans_matrix():
    """
        Создание транспонированной
        матрицы.
    """

    global trans_matrix

    trans_matrix.clear()

    for i in range(4):
        tmp_arr = []

        for j in range(4):
            tmp_arr.append(int(i == j))
            
        trans_matrix.append(tmp_arr)


def turn_matrix(matrix):
    """
        Повернуть матрицу.
    """

    global trans_matrix

    result = [[0 for i in range(4)] for j in range(4)]

    for i in range(4):
        for j in range(4):
            for k in range(4):
                result[i][j] += trans_matrix[i][k] * matrix[k][j]

    trans_matrix = result


def spin_x():
    """
        Поворот по оси X.
    """

    try:
        angle = float(turn_x_etr.get()) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол должен быть числом.")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан.")
        return

    rotating_matrix = [[1, 0, 0, 0],
                     [0, cos(angle), sin(angle), 0],
                     [0, -sin(angle), cos(angle), 0],
                     [0, 0, 0, 1]   ]

    turn_matrix(rotating_matrix)

    build_graph()


def spin_y():
    """
       Поворот по оси Y.
    """

    try:
        angle = float(turn_y_etr.get()) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол должен быть числом.")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан.")
        return

    rotating_matrix = [[cos(angle), 0, -sin(angle), 0],
                     [0, 1, 0, 0],
                     [sin(angle), 0, cos(angle), 0],
                     [0, 0, 0, 1]   ]

    turn_matrix(rotating_matrix)

    build_graph()


def spin_z():
    """
       Поворот по оси Z.
    """

    try:
        angle = float(turn_z_etr.get()) / 180 * pi
    except:
        messagebox.showerror("Ошибка", "Угол должен быть числом.")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан.")
        return

    rotating_matrix = [[cos(angle), sin(angle), 0, 0],
                     [-sin(angle), cos(angle), 0, 0],
                     [0, 0, 1, 0],
                     [0, 0, 0, 1]   ]

    turn_matrix(rotating_matrix)

    build_graph()


def scale_graph():
    """
        Масштабирование.
    """

    try:
        scale_param = float(k_etr.get())
    except:
        messagebox.showerror("Ошибка", "Коэффициент масштабирования должен быть числом.")
        return

    if (len(trans_matrix) == 0):
        messagebox.showerror("Ошибка", "График не задан.")
        return

    build_graph(scale_param = scale_param)


def trans_dot(dot, scale_param):
    """
        Транспонирование точки.
    """

    dot.append(1) 

    res_dot = [0, 0, 0, 0]

    for i in range(4):
        for j in range(4):
            res_dot[i] += dot[j] * trans_matrix[j][i]

    for i in range(3):
        res_dot[i] *= scale_param

    res_dot[0] += Graphic.canvas_width // 2
    res_dot[1] += Graphic.canvas_heigth // 2

    return res_dot[:3]


def is_visible(dot):
    """
        Проверка точки на видимость.
    """

    return (0 <= dot[X_DOT] <= Graphic.canvas_width) and \
            (0 <= dot[Y_DOT] <= Graphic.canvas_heigth)


def draw_pixel(x, y):
    """
        Рисование пикселя.
    """

    colour = get_result_colour()

    canvas.create_line(x, y, x + 1, y + 1, fill = colour[1])


def draw_dot(x, y, high_horizon, low_horizon):
    """
        Рисование точки.
    """

    if (not is_visible([x, y])):
        return False

    if (y > high_horizon[int(x)]):
        high_horizon[int(x)] = y
        draw_pixel(x, y)
    elif (y < low_horizon[int(x)]):
        low_horizon[int(x)] = y
        draw_pixel(x, y)

    return True


def draw_horizon_part(dot1, dot2, high_horizon, low_horizon):
    """
        Рисование горизонтальной части.
    """

    if (dot1[X_DOT] > dot2[X_DOT]):
        dot1, dot2 = dot2, dot1

    dx = dot2[X_DOT] - dot1[X_DOT]
    dy = dot2[Y_DOT] - dot1[Y_DOT]

    if (dx > dy):
        l = dx
    else:
        l = dy

    dx /= l
    dy /= l

    x = dot1[X_DOT]
    y = dot1[Y_DOT]

    for _ in range(int(l) + 1):
        if (not draw_dot(round(x), y, high_horizon, low_horizon)):
            return

        x += dx
        y += dy


def draw_horizon(function, high_horizon, low_horizon, limits, z, scale_param):
    """
        Рисование горизонта.
    """

    f = lambda x: function(x, z)

    prev = None

    for x in arange(limits[FROM], limits[TO] + limits[STEP], limits[STEP]):
        cur = trans_dot([x, f(x), z], scale_param)

        if (prev):
            draw_horizon_part(prev, cur, high_horizon, low_horizon)

        prev = cur


def draw_horizon_limits(f, x_limits, z_limits, scale_param):
    """
    """

    colour = get_result_colour()

    for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
        dot1 = trans_dot([x_limits[FROM], f(x_limits[FROM], z), z], scale_param)
        dot2 = trans_dot([x_limits[FROM], f(x_limits[FROM], z + x_limits[STEP]), z + x_limits[STEP]], scale_param)

        canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = colour[1])

        dot1 = trans_dot([x_limits[TO], f(x_limits[TO], z), z], scale_param)
        dot2 = trans_dot([x_limits[TO], f(x_limits[TO], z + x_limits[STEP]), z + x_limits[STEP]], scale_param)

        canvas.create_line(dot1[X_DOT], dot1[Y_DOT], dot2[X_DOT], dot2[Y_DOT], fill = colour[1])


def build_graph(new_graph = False, scale_param = DEFAULT_SCALE):
    clear()

    if (new_graph):
        create_trans_matrix()

    f = get_func()
    x_limits, z_limits = get_limits()


    high_horizon = [0 for i in range(Graphic.canvas_width + 1)]
    low_horizon = [Graphic.canvas_heigth for i in range(Graphic.canvas_width + 1)]

    #  Горизонт
    for z in arange(z_limits[FROM], z_limits[TO] + z_limits[STEP], z_limits[STEP]):
        draw_horizon(f, high_horizon, low_horizon, x_limits, z, scale_param)

    # Границы горизонта
    draw_horizon_limits(f, x_limits, z_limits, scale_param)


# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    canvas.delete(tk.ALL)


def get_result_colour():
    """
        Выбор цвета результата.
    """

    for i in colour_res_list.curselection():
        index = int(i)
    colour = colour_res_list.get(index)

    if colour == "Синий":
        return [(0, 0, 255), Colour.blue]
    elif colour == "Зелёный":
        return [(0, 255, 0), Colour.green]
    elif colour == "Красный":
        return [(255, 0, 0), Colour.red]
    

def get_func():
    """
        Получить функцию поверхности.
    """

    for i in func_box.curselection():
        index = int(i)
        
    func = lambda x, z: sin(x) * cos(z)

    print(index)
    if (index == 1):
        func = lambda x, z: sin(x) * sin(z)
    elif (index == 2):
        func = lambda x, z: sin(cos(x)) * sin(z)
    elif (index == 3):
        func = lambda x, z: cos(x) * z / 3
    elif (index == 4):
        func = lambda x, z: cos(x) * cos(sin(z))

    return func


def get_limits():
    """
        Получить пределы
        значений x и z.
    """

    try:
        start_x = float(start_x_etr.get())
        end_x = float(end_x_etr.get())
        x_step = float(step_x_etr.get())

        x_limits = [start_x, end_x, x_step]

        start_z = float(start_z_etr.get())
        end_z = float(end_z_etr.get())
        z_step = float(step_z_etr.get())

        z_limits = [start_z, end_z, z_step]
    
        return x_limits, z_limits
    except:
        return -1, -1


if __name__ == "__main__":
    """
        Создание графического интерфейса.
    """

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Холст
    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = Colour.white)
    canvas.place(x = 50, y = 50)

    # Функции
    func_lbl = tk.Label(window, text = "ФУНКЦИИ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    func_lbl.place(x = 2360, y = 20)

    funcs = ["sin(x) * sin(z)", "sin(cos(x)) * sin(z)", "cos(x) * z / 3", "cos(x) * cos(sin(z))"]

    func_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 4,
                          width = 52)
    func_box.place(x = 1960, y = 80)

    for func in funcs:
        func_box.insert(tk.END, func)

    # Многоугольник
    limits_lbl = tk.Label(window, text = "ПРЕДЕЛЫ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    limits_lbl.place(x = 2350, y = 250)

    x_lbl = tk.Label(window, text = "Ось x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_lbl.place(x = 1960, y = 310)

    start_x_lbl = tk.Label(window, text = "от ",
                             font = Graphic.font,
                             bg = Colour.back)
    start_x_lbl.place(x = 2120, y = 310)

    start_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    start_x_etr.insert(0, "-10")
    start_x_etr.place(x = 2180, y = 310)

    end_x_lbl = tk.Label(window, text = "до ",
                             font = Graphic.font,
                             bg = Colour.back)
    end_x_lbl.place(x = 2320, y = 310)

    end_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    end_x_etr.place(x = 2380, y = 310)

    step_x_lbl = tk.Label(window, text = "с шагом ",
                             font = Graphic.font,
                             bg = Colour.back)
    end_x_etr.insert(0, "10")
    step_x_lbl.place(x = 2560, y = 310)

    step_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    step_x_etr.insert(0, "0.1")
    step_x_etr.place(x = 2730, y = 310)

    z_lbl = tk.Label(window, text = "Ось z:",
                             font = Graphic.font,
                             bg = Colour.back)
    z_lbl.place(x = 1960, y = 370)

    start_z_lbl = tk.Label(window, text = "от ",
                             font = Graphic.font,
                             bg = Colour.back)
    start_z_lbl.place(x = 2120, y = 370)

    start_z_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    start_z_etr.insert(0, "-10")
    start_z_etr.place(x = 2180, y = 370)

    end_z_lbl = tk.Label(window, text = "до ",
                             font = Graphic.font,
                             bg = Colour.back)
    end_z_lbl.place(x = 2320, y = 370)

    end_z_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    end_z_etr.insert(0, "10")
    end_z_etr.place(x = 2380, y = 370)

    step_z_lbl = tk.Label(window, text = "с шагом ",
                             font = Graphic.font,
                             bg = Colour.back)
    step_z_lbl.place(x = 2560, y = 370)

    step_z_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    step_z_etr.insert(0, "0.1")
    step_z_etr.place(x = 2730, y = 370)

    # Вращение

    turn_lbl = tk.Label(window, text = "ВРАЩЕНИЕ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    turn_lbl.place(x = 2350, y = 430)

    ox_lbl = tk.Label(window, text = "Ось x:",
                             font = Graphic.font,
                             bg = Colour.back)
    ox_lbl.place(x = 1960, y = 490)

    turn_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    turn_x_etr.insert(0, "30")
    turn_x_etr.place(x = 2180, y = 490)

    turn_x_btn = tk.Button(window, font = Graphic.font,
                                 width = 19,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Повернуть",
                                 command= spin_x)
    turn_x_btn.place(x = 2390, y = 490) 

    oy_lbl = tk.Label(window, text = "Ось y:",
                             font = Graphic.font,
                             bg = Colour.back)
    oy_lbl.place(x = 1960, y = 580)

    turn_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    turn_y_etr.insert(0, "30")
    turn_y_etr.place(x = 2180, y = 580)

    turn_y_btn = tk.Button(window, font = Graphic.font,
                                 width = 19,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Повернуть",
                                 command= spin_y)
    turn_y_btn.place(x = 2390, y = 580) 

    oz_lbl = tk.Label(window, text = "Ось z:",
                             font = Graphic.font,
                             bg = Colour.back)
    oz_lbl.place(x = 1960, y = 670)

    turn_z_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    turn_z_etr.insert(0, "30")
    turn_z_etr.place(x = 2180, y = 670)

    turn_z_btn = tk.Button(window, font = Graphic.font,
                                 width = 19,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Повернуть",
                                 command= spin_z)
    turn_z_btn.place(x = 2390, y = 670) 

    # Масштабирование

    scale_lbl = tk.Label(window, text = "МАСШТАБИРОВАНИЕ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    scale_lbl.place(x = 2300, y = 760)

    k_lbl = tk.Label(window, text = "Коэффициент:",
                             font = Graphic.font,
                             bg = Colour.back)
    k_lbl.place(x = 1960, y = 820)

    k_etr = tk.Entry(window, font = Graphic.font,
                             width = 5,
                             justify = tk.CENTER)
    k_etr.insert(0, "45")
    k_etr.place(x = 2250, y = 820)

    scale_btn = tk.Button(window, font = Graphic.font,
                                 width = 19,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Масштабировать",
                                 command= scale_graph)
    scale_btn.place(x = 2390, y = 820)

    # Выбор цвета результата

    colours = ["Синий", "Зелёный", "Красный"]

    colour_res_lbl = tk.Label(window, text = "ЦВЕТ РЕЗУЛЬТАТА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_res_lbl.place(x = 2300, y = 960)

    colour_res_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_res_list.place(x = 1960, y = 1020)

    for colour in colours:
        colour_res_list.insert(tk.END, colour)

    cut_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Нарисовать",
                                 command = lambda: build_graph(new_graph = True))
    cut_btn.place(x = 1960, y = 1420) 

    # Очистить экран
    clear_btn = tk.Button(window, font = Graphic.font,
                                  width = 38,
                                  bg = Colour.button,
                                  bd = 6,
                                  text = "Очистить экран",
                                  command = clear)
    clear_btn.place(x = 1960, y = 1500) 

    window.mainloop()