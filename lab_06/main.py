from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

import numpy as np
import time

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 6"

    font_bold = "FreeMono 16 bold"
    font = "FreeMono 14"

    canvas_heigth = 1400
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

TYPE_PAUSE = 1
TYPE_NOT_PAUSE = 2


# Заполнение

def create_time(work_time):
    """
        Вывод времени заполнения.
    """
    time_etr = tk.Entry(window, font = Graphic.font_bold,
                                bg = Colour.back,
                                width=40)
    time_etr.place(x = 50, y = 50)

    time_str = "Время заполнения: {0:6.4f}".format(work_time)
    time_etr.insert(tk.END, time_str)


def seed_fill(stack, colour, pause):
    """
        Построчное затравочное
        заполнение.
    """

    edge_colour = (0, 0, 0)

    start_time = time.time()

    while stack:
        now_point = stack.pop()
        image_canvas.put(colour[1], now_point)

        x, y = now_point[0] + 1, now_point[1]

        while (image_canvas.get(x, y) != edge_colour and 
              image_canvas.get(x, y) != colour[0]):
            image_canvas.put(colour[1], (x, y))
            x += 1

        rx = x - 1

        x = now_point[0] - 1

        while (image_canvas.get(x, y) != edge_colour and 
               image_canvas.get(x, y) != colour[0]):
            image_canvas.put(colour[1], (x, y))
            x -= 1

        lx = x + 1

        for i in [1, -1]:
            x = lx
            y = now_point[1] + i

            while x <= rx:
                flag = 0

                while (image_canvas.get(x, y) != edge_colour and 
                       image_canvas.get(x, y) != colour[0] and x <= rx):
                    flag = 1
                    x += 1

                if flag:
                    stack.append([x - 1, y])

                    flag = 0

                start_x = x

                while ((image_canvas.get(x, y) == edge_colour 
                        or image_canvas.get(x, y) == colour[0]) 
                        and x < rx):
                    x += 1

                if x == start_x:
                    x += 1

        if pause:
            time.sleep(pause)
            canvas.update()
    end_time = time.time()

    if not pause:
        create_time(end_time - start_time)


def fill():
    """
       Заполнение фигуры заданным цветом,
       с задержкой или без задержки.
    """

    last = dots_box.get(dots_box.size() - 1)

    if last != "     ":
        messagebox.showerror("Ошибка",
                             "Нужно замкнуть фигуру перед заполнением.")
        return

    
    if len(stack) != 1:
        messagebox.showerror("Ошибка",
                             "Затравочный пиксель должен быть задан.")
        return

    colour = get_colour()
    type_id = get_type()

    if type_id == TYPE_PAUSE:
        pause_time = get_pause_time()
        seed_fill(stack, colour, pause_time)
    elif type_id == TYPE_NOT_PAUSE:
        seed_fill(stack, colour, 0)


# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    global points
    global image_canvas

    canvas.delete(tk.ALL)

    image_canvas = tk.PhotoImage(width = Graphic.canvas_width, 
                                 height = Graphic.canvas_heigth)
    canvas.create_image((Graphic.canvas_width / 2, Graphic.canvas_heigth / 2), 
                        image = image_canvas, state = "normal")
    image_canvas.put(Colour.white, to = (0, 0, Graphic.canvas_width, Graphic.canvas_heigth))
    
    dots_box.delete(0, dots_box.size())
    points.clear()
    stack.clear()

    points.append([])
    time_etr.delete(0, tk.END)


# Цвет
def get_colour():
    """
        Выбор цвета заполнения.
    """

    for i in colour_list.curselection():
        index = int(i)
    colour = colour_list.get(index)

    if colour == "Синий":
        return [(0, 0, 255), Colour.blue]
    elif colour == "Зелёный":
        return [(0, 255, 0), Colour.green]
    elif colour == "Красный":
        return [(255, 0, 0), Colour.red]

# Тип
def get_type():
    """
        Выбор типа заполнения.
    """

    for i in fill_list.curselection():
        index = int(i)
    select = fill_list.get(index)

    if select == "С задержкой":
        return TYPE_PAUSE
    elif select == "Без задержки":
        return TYPE_NOT_PAUSE


# Время задержки
def get_pause_time():
    """
        Ввод времени задержки.
    """

    try:
        pause_time = float(pause_time_etr.get())
        return pause_time
    except:
        messagebox.showerror("Ошибка",
                             "Время должно быть вещественным числом.")
        return -1


# Работа с ребрами

def draw_edge(edge):
    """
        Рисование ребра фигуры.
    """

    for point in edge:
        image_canvas.put(Colour.black, (point[0], point[1]))


def brezenham_int(start, end):
    """
        Создание ребра.
    """

    edge = []

    x, y = start[0], start[1]
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    sx = int(np.sign(dx))
    sy = int(np.sign(dy))
    dx, dy = abs(dx), abs(dy)

    if dx > dy:
        change = 0
    else:
        change = 1
        dx, dy = dy, dx

    e = dy + dy - dx

    if not change:
        for _ in range(dx):
            edge.append([x, y])

            if e >= 0:
                y += sy
                e -= dx + dx
            x += sx
            e += dy + dy
    else:
        for _ in range(dx):
            edge.append([x, y])

            if e >= 0:
                x += sx
                e -= dx + dx
            y += sy
            e += dy + dy

    return edge


def close_figure():
    """
        Замкнуть фигуру.
    """

    if len(points[-1]) < 3:
        messagebox.showerror("Ошибка",
                             "Чтобы замкнуть фигуру необходимо минимум 3 точки.")
        return

    if len(points[-1]) > 1:
        start = points[-1][-1]
        end = points[-1][0]
        edge = brezenham_int(start, end)
        draw_edge(edge)

        dots_box.insert(tk.END, " " * 5)
        points.append([])


# Работа с точками
def draw_point(x, y, color):
    """
        Рисование точки.
    """

    image_canvas.put(color, (x, y))


def add_dot(x, y):
    """
        Добавление точки.
    """

    dot_index = len(points[-1]) - 1
    dots_box.insert(tk.END, "{0}. ({1:-4.2f};{2:-4.2f})".format(dot_index + 2, x, y))

    points[-1].append([x, y])

    if len(points[-1]) > 1:
        start = points[-1][-2]
        end = points[-1][-1]
        edge = brezenham_int(start, end)
        draw_edge(edge)


def get_entry_dot():
    """
        Получение координат точки,
        задаваемой в полях ввода.
    """

    try:
        x = int(x_etr.get())
        y = int(y_etr.get())
    except:
        messagebox.showerror("Ошибка",
                             "Координаты точки должны быть числами.")
        return
    
    add_dot(x, y)


def get_click_dot(event):
    """
        Получение координат точки,
        задаваемой мышкой.
    """

    x = event.x 
    y = event.y

    add_dot(x, y)


def add_seed_dot(x, y):
    """
        Добавление координат
        затравочного пикселя.
    """

    if len(stack) == 1:
        stack.clear()

    stack.append([x, y])


def get_seed_dot():
    """
        Получение координат затравочного
        пикселя, задаваемого в полях ввода.
    """

    try:
        x = int(seed_x_etr.get())
        y = int(seed_y_etr.get())
    except:
        messagebox.showerror("Ошибка",
                             "Координаты точки должны быть числами.")
        return
    
    add_seed_dot(x, y)


def get_click_seed_dot(event):
    """
        Получение координат 
        затравочного пикселя,
        задаваемого мышкой.
    """

    x = event.x 
    y = event.y

    seed_x_etr.delete(0, tk.END)
    seed_y_etr.delete(0, tk.END)
    seed_x_etr.insert(tk.END, str(x))
    seed_y_etr.insert(tk.END, str(y))

    add_seed_dot(x, y)


if __name__ == "__main__":
    """
        Создание графического интерфейса.
    """

    # Все точки
    points = [[]]

    # Стек
    stack = []

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Холст

    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = Colour.white)
    canvas.place(x = 50, y = 150)

    image_canvas = tk.PhotoImage(width = Graphic.canvas_width,
                                 height = Graphic.canvas_heigth)
    canvas.create_image((Graphic.canvas_width / 2, Graphic.canvas_heigth / 2),
                         image = image_canvas, state = "normal")
    image_canvas.put(Colour.white, to = (0, 0, Graphic.canvas_width, Graphic.canvas_heigth))

    # Время
    time_etr = tk.Entry(window, font = Graphic.font_bold,
                                bg = Colour.back,
                                width=40)
    time_etr.place(x = 50, y = 50)

    # Добавление точки
    point_lbl = tk.Label(window, text = "Добавление точки",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    point_lbl.place(x = 2220, y = 20)

    x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_lbl.place(x = 1960, y = 80)

    y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    y_lbl.place(x = 2552, y = 80)

    x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    x_etr.place(x = 2060, y = 80)

    y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    y_etr.place(x = 2652, y = 80)

    add_point_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Добавить",
                                      command = get_entry_dot)
    add_point_btn.place(x = 1960, y = 140) 

    # Список точек
    dots_lbl = tk.Label(window, text = "Список точек",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    dots_lbl.place(x = 2280, y = 230)

    dots_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 12,
                          width = 51)
    dots_box.place(x = 1960, y = 290)


    close_fig_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Замкнуть",
                                      command = close_figure)
    close_fig_btn.place(x = 1960, y = 720)

    # Затравочный пиксель
    seed_point_lbl = tk.Label(window, text = "Затравочный пиксель",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    seed_point_lbl.place(x = 2200, y = 800)

    seed_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    seed_x_lbl.place(x = 1960, y = 860)

    seed_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    seed_y_lbl.place(x = 2552, y = 860)

    seed_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)

    seed_x_etr.place(x = 2060, y = 860)

    seed_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)

    seed_y_etr.place(x = 2652, y = 860)

    fill_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Задать",
                                 command = get_seed_dot)
    fill_btn.place(x = 1960, y = 920) 

    # Выбор цвета
    colour_lbl = tk.Label(window, text = "Цвет заполнения",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_lbl.place(x = 2235, y = 1000)

    colours = ["Синий", "Зелёный", "Красный"]
    colour_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_list.place(x = 1960, y = 1060)

    for colour in colours:
        colour_list.insert(tk.END, colour)

    # Выбор типа заполнения
    fill_lbl = tk.Label(window, text = "Тип заполнения",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    fill_lbl.place(x = 2240, y = 1200)

    fill_views = ["С задержкой", "Без задержки"]
    fill_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 2,
                             width = 40,
                             font = Graphic.font)
    fill_list.place(x = 1960, y = 1260)

    for view in fill_views:
        fill_list.insert(tk.END, view)

    pause_time_lbl = tk.Label(window, text = "Время задержки (с): ",
                             font = Graphic.font,
                             bg = Colour.back)
    pause_time_lbl.place(x = 1960, y = 1400)

    pause_time_etr = tk.Entry(window, font = Graphic.font,
                             width = 12,
                             justify = tk.CENTER)

    pause_time_etr.place(x = 2400, y = 1400)

    fill_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Заполнить",
                                 command = fill)
    fill_btn.place(x = 1960, y = 1460) 

    # Очистить экран
    clear_btn = tk.Button(window, font = Graphic.font,
                                  width = 38,
                                  bg = Colour.button,
                                  bd = 6,
                                  text = "Очистить экран",
                                  command = clear)
    clear_btn.place(x = 1960, y = 1530) 

    # Работа с мышью
    canvas.bind('<1>', get_click_dot)
    canvas.bind('<3>', get_click_seed_dot)

    window.mainloop()
