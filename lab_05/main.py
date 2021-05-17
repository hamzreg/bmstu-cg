from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

import time

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 5"

    font_bold = "FreeMono 16 bold"
    font = "FreeMono 14"

    canvas_heigth = 1400
    canvas_width = 1800

@dataclass
class Colour:

    back = "#ABCDEF"
    draw = "#3E8353"
    button = "#DDF1FF"
    text = "#28852F"

def create_time(work_time):
    # Время выполнения

    time_str = "Время заполнения: {0:6.4f}".format(work_time)
    time_etr.insert(tk.END, time_str)

# Алгоритм
def get_intersections(start, end, dots):
    """
        Поиск пересечений.
    """

    if start[1] == end[1]:
        return
    
    if start[1] > end[1]:
        start, end = end, start
    
    dy = 1
    dx = (end[0] - start[0]) / (end[1] - start[1])
    
    x, y = start[0], start[1]

    while y < end[1]:
        dots.append([round(x), round(y)])

        y += dy
        x += dx

def reverse_pixel(colour, x, y):
    colour_pixel = image_canvas.get(round(x), round(y))

    if colour_pixel != colour[0]:
        image_canvas.put(colour[1], (round(x), round(y)))
    elif colour_pixel == colour[0]:
        image_canvas.put("#FFFFFF", (round(x), round(y)))


def not_pause_fill(colour, dots):
    """
        Заполнение без задержки.
    """

    start = time.time()

    septum = dots[0][0]

    for i in range(len(dots)):
        if dots[i][0] < septum:
            for j in range(dots[i][0] + 1, septum + 1):
                reverse_pixel(colour, j, dots[i][1])
        elif dots[i][0] > septum:
            for j in range(dots[i][0], septum, -1):
                reverse_pixel(colour, j, dots[i][1])
    
    end = time.time()
    create_time(end - start)
    

def pause_fill(colour, dots):
    """
        Заполнение с задержкой.
    """

    septum = dots[0][0]

    for i in range(len(dots)):
        if dots[i][0] < septum:
            for j in range(dots[i][0] + 1, septum + 1):
                canvas.after(1, reverse_pixel(colour, j, dots[i][1]))
                canvas.update()
        elif dots[i][0] > septum:
            for j in range(dots[i][0], septum, -1):
                canvas.after(1, reverse_pixel(colour, j, dots[i][1]))
                canvas.update()


def fill():
    last = dots_box.get(dots_box.size() - 1)

    if last != "     ":
        messagebox.showerror("Ошибка", "Нужно замкнуть фигуру перед заполнением.")
        return

    colour = get_colour()
    type_id = get_type()

    time_etr.delete(0, tk.END)

    if type_id == 1:
        pause_fill(colour, dots),
    elif type_id == 2:
        not_pause_fill(colour, dots)



# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    global dots
    global points
    global image_canvas

    canvas.delete(tk.ALL)

    image_canvas = tk.PhotoImage(width = Graphic.canvas_width, height = Graphic.canvas_heigth)
    canvas.create_image((Graphic.canvas_width / 2, Graphic.canvas_heigth / 2), image = image_canvas, state = "normal")
    
    dots_box.delete(0, dots_box.size())
    dots.clear()
    points.clear()

    points.append([])
    time_etr.delete(0, tk.END)

def draw_point(x, y, color):
    image_canvas.put(color, (x, y))


def draw_edge(start, end):
    """
        Рисование ребра фигуры.
    """

    canvas.create_line(start[0], start[1],
                       end[0], end[1])

def close_figure():
    """
        Замкнуть фигуру.
    """

    if len(points[-1]) < 3:
        messagebox.showerror("Ошибка", "Чтобы замкнуть фигуру необходимо минимум 3 точки.")
        return
    if len(points[-1]) > 1:
        start = points[-1][-1]
        end = points[-1][0]

        get_intersections(start, end, dots)
        draw_edge(start, end)

        dots_box.insert(tk.END, " " * 5)
        points.append([])

# Цвет
def get_colour():
    """
        Выбор цвета заполнения.
    """

    for i in colour_list.curselection():
        index = int(i)
    colour = colour_list.get(index)

    if colour == "Синий":
        return [(0, 0, 255), "#0000FF"]
    elif colour == "Зелёный":
        return [(0, 255, 0), "#00FF00"]
    elif colour == "Красный":
        return [(255, 0, 0), "#FF0000"]

# Тип
def get_type():
    """
        Выбор типа заполнения.
    """

    for i in fill_list.curselection():
        index = int(i)
    select = fill_list.get(index)

    if select == "С задержкой":
        return 1
    elif select == "Без задержки":
        return 2



# Работа с точками

def add_dot(x, y):
    """
        Добавление точки.
    """

    if len(points) > 1 and len(points[-1]) == 0:
        dots.clear()

    dot_index = len(points[-1]) - 1

    dots_box.insert(tk.END, "{0}. ({1:-4.2f};{2:-4.2f})".format(dot_index + 2, x, y))
    points[-1].append([x, y])

    if len(points[-1]) > 1:
        start = points[-1][-2]
        end = points[-1][-1]

        get_intersections(end, start, dots)
        draw_edge(start, end)

    elif len(points[-1]) == 1:
        draw_point(points[-1][0][0], points[-1][0][1], "black")


def get_entry_dot():
    """
        Получение координат точки,
        задаваемой в полях ввода.
    """

    try:
        x = float(x_etr.get())
        y = float(y_etr.get())
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


if __name__ == "__main__":
    """
        Создание графического интерфейса.
    """

    # Все точки
    points = [[]]

    # Пересечения
    dots = []

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Холст

    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = "white")
    canvas.place(x = 50, y = 150)

    image_canvas = tk.PhotoImage(width = Graphic.canvas_width, height = Graphic.canvas_heigth)
    canvas.create_image((Graphic.canvas_width / 2, Graphic.canvas_heigth / 2), image = image_canvas, state = "normal")

    # Время
    time_etr = tk.Entry(window, font = Graphic.font_bold,
                                bg = Colour.back,
                                width=40)
    time_etr.place(x = 50, y = 50)

    # Добавление точки

    point_lbl = tk.Label(window, text = "Добавление точки",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    point_lbl.place(x = 2220, y = 50)

    x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_lbl.place(x = 1960, y = 150)

    y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    y_lbl.place(x = 2552, y = 150)

    x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    x_etr.insert(tk.END, "0")
    x_etr.place(x = 2060, y = 150)

    y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    y_etr.insert(tk.END, "0")
    y_etr.place(x = 2652, y = 150)

    add_point_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Добавить",
                                      command = get_entry_dot)
    add_point_btn.place(x = 1960, y = 210) 

    close_fig_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Замкнуть",
                                      command = close_figure)
    close_fig_btn.place(x = 1960, y = 780) 

    # Список точек

    dots_lbl = tk.Label(window, text = "Список точек",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    dots_lbl.place(x = 2280, y = 300)

    dots_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 12,
                          width = 51)
    dots_box.place(x = 1960, y = 360)

    # Выбор цвета

    colour_lbl = tk.Label(window, text = "Цвет заполнения",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_lbl.place(x = 2235, y = 930)

    colours = ["Синий", "Зелёный", "Красный"]
    colour_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_list.place(x = 1960, y = 990)

    for colour in colours:
        colour_list.insert(tk.END, colour)

    # Выбор типа заполнения

    fill_lbl = tk.Label(window, text = "Тип заполнения",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    fill_lbl.place(x = 2240, y = 1130)

    fill_views = ["С задержкой", "Без задержки"]
    fill_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 2,
                             width = 40,
                             font = Graphic.font)
    fill_list.place(x = 1960, y = 1190)

    for view in fill_views:
        fill_list.insert(tk.END, view)

    fill_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Заполнить",
                                 command = fill)
    fill_btn.place(x = 1960, y = 1290) 

    # Очистить экран

    clear_btn = tk.Button(window, font = Graphic.font,
                                  width = 38,
                                  bg = Colour.button,
                                  bd = 6,
                                  text = "Очистить экран",
                                  command = clear)
    clear_btn.place(x = 1960, y = 1490) 

    # Работа с мышью
    canvas.bind('<1>', get_click_dot)

    window.mainloop()
