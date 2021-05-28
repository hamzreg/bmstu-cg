from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

is_cutter_create = False


@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 7"

    font_bold = "FreeMono 16 bold"
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


# Отсечение

MASK_LEFT =   0b0001
MASK_RIGHT =  0b0010
MASK_BOTTOM = 0b0100
MASK_TOP =    0b1000

def set_bits(point, cutter):
    bits = 0b0000

    if point[0] < cutter[0]:
        bits += MASK_LEFT

    if point[0] > cutter[2]:
        bits += MASK_RIGHT

    if point[1] < cutter[1]:
        bits += MASK_BOTTOM

    if point[1] > cutter[3]:
        bits += MASK_TOP

    return bits


def find_vertical(section, index, cutter):
    if section[index][1] > cutter[1]:
        return [section[index][0], cutter[1]]
    elif section[index][1] < cutter[3]:
        return [section[index][0], cutter[3]]
    else:
        return section[index]


def simple_clipping(section, cutter, colour):
    """
        Простой алгоритм отсечения.
    """

    s = list()
    for i in range(2):
        s.append(set_bits(section[i], cutter))

    # Полностью видимый отрезок
    if s[0] == 0 and s[1] == 0:
        canvas.create_line(section[0][0], section[0][1], 
                           section[1][0], section[1][1],
                           fill = colour)
        return

    # Полностью невидимый отрезок
    if s[0] & s[1]:
        return

    now_index = 0
    result = list()

    # Нет ли точки внутри отсекателя
    if s[0] == 0:
        now_index = 1
        result.append(section[0])

    elif s[1] == 0:
        result.append(section[1])
        now_index = 1

        section.reverse()
        s.reverse()

    while now_index < 2:
        if section[0][0] == section[1][0]:
            result.append(find_vertical(section, now_index, cutter))
            now_index += 1
            continue

        m = (section[1][1] - section[0][1]) / (section[1][0] - section[0][0])

        # Пересечение с левой границей
        if s[now_index] & MASK_LEFT:
            y = round(m * (cutter[0] - section[now_index][0]) + section[now_index][1])
            if y <= cutter[3] and y >= cutter[1]:
                result.append([cutter[0], y])
                now_index += 1
                continue

        # Пересечение с правой границей
        elif s[now_index] & MASK_RIGHT:
            y = round(m * (cutter[2] - section[now_index][0]) + section[now_index][1])
            if y <= cutter[3] and y >= cutter[1]:
                result.append([cutter[2], y])
                now_index += 1
                continue

        # Горизонтальная прямая
        if m == 0:
            now_index += 1
            continue


        # Пересечение с верхней границей (если рассматриваемая вершина выше верхней границы)
        if s[now_index] & MASK_TOP:
            x = round((cutter[3] - section[now_index][1]) / m + section[now_index][0])
            if x <= cutter[2] and x >= cutter[0]:
                result.append([x, cutter[3]])
                now_index += 1
                continue

        # Пересечение с нижней границей (если рассматриваемая вершина ниже нижней границы)
        elif s[now_index] & MASK_BOTTOM:
            x = round((cutter[1] - section[now_index][1]) / m + section[now_index][0])
            if x <= cutter[2] and x >= cutter[0]:
                result.append([x, cutter[1]])
                now_index += 1
                continue

        now_index += 1

    if result:
        canvas.create_line(result[0][0], result[0][1], 
                           result[1][0], result[1][1], fill = colour)



def cut_sections():
    """
        Отсечение отрезков
        регулярным отсекателем.
    """

    colour = get_result_colour()

    for section in sections:
        if section:
            simple_clipping(section, cutter, colour[1])


# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    canvas.delete(tk.ALL)

    sections.clear()
    sections.append([])


# Цвет
def get_cutter_colour():
    """
        Выбор цвета отсекателя.
    """

    for i in colour_сut_list.curselection():
        index = int(i)
    colour = colour_сut_list.get(index)

    if colour == "Синий":
        return [(0, 0, 255), Colour.blue]
    elif colour == "Зелёный":
        return [(0, 255, 0), Colour.green]
    elif colour == "Красный":
        return [(255, 0, 0), Colour.red]


def get_section_colour():
    """
        Выбор цвета отрезка.
    """

    for i in colour_sec_list.curselection():
        index = int(i)
    colour = colour_sec_list.get(index)

    if colour == "Синий":
        return [(0, 0, 255), Colour.blue]
    elif colour == "Зелёный":
        return [(0, 255, 0), Colour.green]
    elif colour == "Красный":
        return [(255, 0, 0), Colour.red]


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


# Работа с отрезками

def get_click_section(event):
    """
        Получение координат вершин
        отрезка, задаваемых мышкой.
    """

    x = event.x
    y = event.y
    sections[-1].append([x, y])

    if (len(sections[-1]) == 2):
        start_x = sections[-1][0][0]
        start_y = sections[-1][0][1]

        end_x = sections[-1][1][0]
        end_y = sections[-1][1][1]

        sections.append([])

        colour = get_section_colour()

        canvas.create_line(start_x, start_y,
                           end_x, end_y,
                           fill = colour[1])


def get_section_etr():
    """
        Получение координат вершин
        отрезка, задаваемых в 
        полях ввода.
    """

    try:
        start_x = int(start_x_etr.get())
        start_y = int(start_y_etr.get())

        end_x = int(end_x_etr.get())
        end_y = int(end_y_etr.get())

    except:
        messagebox.showerror("Ошибка",
                             "Координаты отрезка должны быть числами.")
        return
    
    sections[-1].append([start_x, start_y])
    sections[-1].append([end_x, end_y])
    sections.append([])
    colour = get_section_colour()

    canvas.create_line(start_x, start_y,
                       end_x, end_y,
                       fill = colour[1])


# Работа с отсекателем
def get_click_cutter(event):
    """
    """

    global cutter
    global is_cutter_create

    if not is_cutter_create:
        cutter[0] = event.x
        cutter[1] = event.y

        is_cutter_create = True
    else:
        up_x = cutter[0]
        up_y = cutter[1]

        low_x = event.x
        low_y = event.y

        cutter[2] = low_x
        cutter[3] = low_y

        clear()

        colour = get_cutter_colour()
        canvas.create_rectangle(up_x, up_y, low_x, low_y,
                                outline = colour[1])


def get_cutter_etr():
    """
        Получение координат вершин
        отсекателя, задаваемых в 
        полях ввода.
    """

    try:
        up_x = int(up_x_etr.get())
        up_y = int(up_y_etr.get())

        low_x = int(low_x_etr.get())
        low_y = int(low_y_etr.get())
    except:
        messagebox.showerror("Ошибка",
                             "Координаты вершин должны быть числами.")
        return

    colour = get_cutter_colour()
    canvas.create_rectangle(up_x, up_y, low_x, low_y,
                            outline = colour[1])
    
    global cutter
    cutter = [up_x, up_y, low_x, low_y]
    

if __name__ == "__main__":
    """
        Создание графического интерфейса.
    """

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Отрезки
    sections = [[]]

    # Осекатель
    cutter = [-1, -1, -1, -1]

    # Холст

    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = Colour.white)
    canvas.place(x = 50, y = 50)

    canvas.bind("<3>", get_click_section)
    canvas.bind("<B1-Motion>", get_click_cutter)


    # Отсекатель
    cutter_lbl = tk.Label(window, text = "ОТСЕКАТЕЛЬ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    cutter_lbl.place(x = 2300, y = 20)

    up_lbl = tk.Label(window, text = "Координаты левой верхней вершины",
                             font = Graphic.font,
                             bg = Colour.back)
    up_lbl.place(x = 2050, y = 80)

    up_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    up_x_lbl.place(x = 1960, y = 140)

    up_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    up_y_lbl.place(x = 2552, y = 140)

    up_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    up_x_etr.place(x = 2060, y = 140)

    up_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    up_y_etr.place(x = 2652, y = 140)

    low_lbl = tk.Label(window, text = "Координаты правой нижней вершины",
                             font = Graphic.font,
                             bg = Colour.back)
    low_lbl.place(x = 2050, y = 200)

    low_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    low_x_lbl.place(x = 1960, y = 260)

    low_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    low_y_lbl.place(x = 2552, y = 260)

    low_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    low_x_etr.place(x = 2060, y = 260)

    low_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    low_y_etr.place(x = 2652, y = 260)

    cutter_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Нарисовать",
                                      command = get_cutter_etr)
    cutter_btn.place(x = 1960, y = 320) 

    # Отрезок
    section_lbl = tk.Label(window, text = "ОТРЕЗОК",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    section_lbl.place(x = 2300, y = 400)

    start_lbl = tk.Label(window, text = "Координаты начала",
                             font = Graphic.font,
                             bg = Colour.back)
    start_lbl.place(x = 2250, y = 460)

    start_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    start_x_lbl.place(x = 1960, y = 520)

    start_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    start_y_lbl.place(x = 2552, y = 520)

    start_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    start_x_etr.place(x = 2060, y = 520)

    start_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    start_y_etr.place(x = 2652, y = 520)

    end_lbl = tk.Label(window, text = "Координаты конца",
                             font = Graphic.font,
                             bg = Colour.back)
    end_lbl.place(x = 2250, y = 580)

    end_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    end_x_lbl.place(x = 1960, y = 640)

    end_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    end_y_lbl.place(x = 2552, y = 640)

    end_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    end_x_etr.place(x = 2060, y = 640)

    end_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    end_y_etr.place(x = 2652, y = 640)

    section_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Нарисовать",
                                      command = get_section_etr)
    section_btn.place(x = 1960, y = 700) 

    # Выбор цвета отсекателя

    colours = ["Синий", "Зелёный", "Красный"]

    colour_cut_lbl = tk.Label(window, text = "ЦВЕТ ОТСЕКАТЕЛЯ",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_cut_lbl.place(x = 2235, y = 780)

    colour_сut_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_сut_list.place(x = 1960, y = 840)

    for colour in colours:
        colour_сut_list.insert(tk.END, colour)

    # Выбор цвета отрезка

    colour_sec_lbl = tk.Label(window, text = "ЦВЕТ ОТРЕЗКА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_sec_lbl.place(x = 2235, y = 980)

    colour_sec_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_sec_list.place(x = 1960, y = 1040)

    for colour in colours:
        colour_sec_list.insert(tk.END, colour)

    # Выбор цвета результата

    colour_res_lbl = tk.Label(window, text = "ЦВЕТ РЕЗУЛЬТАТА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_res_lbl.place(x = 2235, y = 1180)

    colour_res_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_res_list.place(x = 1960, y = 1240)

    for colour in colours:
        colour_res_list.insert(tk.END, colour)

    cut_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Отсечь",
                                 command = cut_sections)
    cut_btn.place(x = 1960, y = 1380) 

    # Очистить экран
    clear_btn = tk.Button(window, font = Graphic.font,
                                  width = 38,
                                  bg = Colour.button,
                                  bd = 6,
                                  text = "Очистить экран",
                                  command = clear)
    clear_btn.place(x = 1960, y = 1530) 

    window.mainloop()
