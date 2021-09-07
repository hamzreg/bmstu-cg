from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

from itertools import combinations

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 8"

    font_bold = "FreeMono 14 bold"
    font = "FreeMono 14"

    canvas_heigth = 1450
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


def get_vector(first, second):
    """
        Получить вектор.
    """

    return [second[0] - first[0], second[1] - first[1]]


def get_vector_mul(first, second):
    """
        Получить векторное произведение.
    """

    return (first[0] * second[1] - first[1] * second[0])


def get_scalar_mul(first, second):
    """
        Получить скалярное произведение.
    """

    return (first[0] * second[0] + first[1] * second[1])


# Проверка на выпуклость
def get_factors(x1, y1, x2, y2):
    """
        Получить коэффициенты
        отрезка.
    """

    a = y1 - y2
    b = x2 - x1
    c = x1 * y2 - x2 * y1

    return a, b, c


def find_intersection(a1, b1, c1, a2, b2, c2):
    """
        Найти пересечение.
    """

    d = a1 * b2 - a2 * b1
    d1 = (-c1) * b2 - b1 * (-c2)
    d2 = a1 * (-c2) - (-c1) * a2

    if d == 0:
        return -5, -5

    x = d1 / d
    y = d2 / d

    return x, y


def is_coord_between(left, right, coord):
    """
        Проверка нахождения координаты
        между двумя координатами.
    """

    return (min(left, right) <= coord and coord <= max(left, right))


def is_point_between(left, right, point):
    """
        Проверка нахождения точки
        между двумя координатами.
    """

    return is_coord_between(left[0], right[0], point[0]) and \
           is_coord_between(left[1], right[1], point[1])


def check_connect(first, second):
    """
        Проверка соединения сторон
        отсекателя.
    """

    if ((first[0][0] == second[0][0] and first[0][1] == second[0][1]) or \
        (first[1][0] == second[1][0] and first[1][1] == second[1][1]) or \
        (first[0][0] == second[1][0] and first[0][1] == second[1][1]) or \
        (first[1][0] == second[0][0] and first[1][1] == second[0][1])):
        return True
    
    return False


def check_intersection():
    """
        Проверка на отсутствие
        пересечений.
    """
    
    sides = []

    for i in range(len(cutter) - 1):
        sides.append([cutter[i], cutter[i + 1]])

    sides_combs = list(combinations(sides, 2))

    for i in range(len(sides_combs)):
        first = sides_combs[i][0]
        second = sides_combs[i][1]

        if check_connect(first, second):
            continue

        a1, b1, c1 = get_factors(first[0][0], first[0][1],
                                 first[1][0], first[1][1])
        a2, b2, c2 = get_factors(second[0][0], second[0][1],
                                 second[1][0], second[1][1])
        
        intersection = find_intersection(a1, b1, c1,
                                         a2, b2, c2)

        if (is_point_between(first[0], first[1], intersection) and \
            is_point_between(second[0], second[1], intersection)):
            return True

    return False


def check_cutter():
    """
       Проверка отсекателя
       на выпуклость.
    """

    if (len(cutter) < 3):
        return False

    sign = 0

    if (get_vector_mul(get_vector(cutter[1], cutter[2]), get_vector(cutter[0], cutter[1])) > 0):
        sign = 1
    else:
        sign = -1

    for i in range(3, len(cutter)):
        if sign * get_vector_mul(get_vector(cutter[i - 1], cutter[i]),
                                 get_vector(cutter[i - 2], cutter[i - 1])) < 0:
            return False

    if check_intersection():
        return False

    return True


# Отсечение
def get_normal(first, second, pos):
    """
        Получить нормаль.
    """

    vector_f = get_vector(first, second)
    vector_pos = get_vector(second, pos)

    if vector_f[1]:
        normal = [1, -vector_f[0] / vector_f[1]]
    else:
        normal = [0, 1]

    if get_scalar_mul(vector_pos, normal) < 0:
        normal[0] = -normal[0]
        normal[1] = -normal[1]
    
    return normal


def cyrus_beck(section, count):
    """
        Алгоритм Кируса-Бека
        отсечения отрезка.
    """

    first = section[0]
    second = section[1]

    d = [second[0] - first[0], second[1] - first[1]]

    t_bottom = 0
    t_top = 1

    for i in range(-2, count - 2):
        normal = get_normal(cutter[i], cutter[i + 1], cutter[i + 2])

        w = [first[0] - cutter[i][0], first[1] - cutter[i][1]]

        d_scalar = get_scalar_mul(d, normal)
        w_scalar = get_scalar_mul(w, normal)

        if d_scalar == 0:
            if w_scalar < 0:
                return
            else:
                continue

        t = -w_scalar / d_scalar

        if d_scalar > 0:
            if t <= 1:
                t_bottom = max(t_bottom, t)
            else:
                return
        elif d_scalar < 0:
            if t >= 0:
                t_top = min(t_top, t)
            else:
                return

        if t_bottom > t_top:
            break

    first_res = [round(first[0] + d[0] * t_bottom), round(first[1] + d[1] * t_bottom)]
    second_res = [round(first[0] + d[0] * t_top), round(first[1] + d[1] * t_top)]
    
    colour = get_result_colour()

    if t_bottom <= t_top:
        canvas.create_line(first_res, second_res, fill = colour[1])


def find_start_point():
    """
        Нахождение начальной точки.
    """

    max_y = cutter[0][1]
    point_index = 0

    for i in range(len(cutter)):
        if cutter[i][1] > max_y:
            max_y = cutter[i][1]
            point_index = i

    cutter.pop()

    for _ in range(point_index):
        cutter.append(cutter.pop(0))

    cutter.append(cutter[0])

    if (cutter[-2][0] > cutter[1][0]):
        cutter.reverse()


def cut_sections():
    """
        Отсечение отрезков
        нерегулярным отсекателем.
    """

    if len(cutter) < 3:
        messagebox.showinfo("Ошибка", "Необходимо задать отсекатель.")
        return

    if not is_closed():
        messagebox.showinfo("Ошибка", "Необходимо замкнуть отсекатель.")
        return

    if not check_cutter():
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником.")
        return
    
    cutter_colour = get_cutter_colour()
    canvas.create_polygon(cutter, outline=cutter_colour[1], fill = "white")

    find_start_point()
    point = cutter.pop()

    for section in sections:
        if section:
            cyrus_beck(section, len(cutter))
    
    cutter.append(point)


# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    canvas.delete(tk.ALL)

    sections.clear()
    sections.append([])
    cutter.clear()
    dots_box.delete(0, tk.END)


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
def draw_sections():

    for section in sections:
        if len(section) != 0:
            x1 = section[0][0]
            y1 = section[0][1]

            x2 = section[1][0]
            y2 = section[1][1]

            colour = get_section_colour()

            canvas.create_line(x1, y1, x2, y2, fill = colour[1])


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
def is_closed():
    """
        Замкнут ли отсекатель.
    """

    closed = False

    if (len(cutter) > 3):
        if ((cutter[0][0] == cutter[-1][0]) and \
            (cutter[0][1] == cutter[-1][1])):
            closed = True

    return closed


def add_dot(x, y, last = False):
    """
       Создание отсекателя.
    """

    cutter.append([x, y])
    now_index = len(cutter)

    if (not last):
        dots_box.insert(tk.END, "{0}. ({1:-4.2f};{2:-4.2f})".format(now_index, x, y))

    if (len(cutter) > 1):
        colour = get_cutter_colour()
        canvas.create_line(cutter[-2], cutter[-1], fill= colour[1])


def get_click_dot(event):
    """
        Получение координат вершин
        отcекателя, задаваемых мышкой.
    """

    x = event.x
    y = event.y

    add_dot(x, y)


def get_dot_etr():
    """
        Получение координат вершин
        отсекателя, задаваемых в 
        полях ввода.
    """

    try:
        x = int(cut_x_etr.get())
        y = int(cut_y_etr.get())
    except:
        messagebox.showerror("Ошибка",
                             "Координаты вершины должны быть числами.")
        return
    
    add_dot(x, y)


def close_cutter():
    """
        Замкнуть отсекатель.
    """

    if (len(cutter) < 3):
        messagebox.showerror("Ошибка",
                             "Для того, чтобы замкнуть фигуру нужно хотя бы 3 точки.")
        return
    
    add_dot(cutter[0][0], cutter[0][1], last = True)
    

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
    cutter = []

    # Холст
    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = Colour.white)
    canvas.place(x = 50, y = 50)

    canvas.bind("<3>", get_click_section)
    canvas.bind("<1>", get_click_dot)


    # Отсекатель
    cutter_lbl = tk.Label(window, text = "ОТСЕКАТЕЛЬ",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    cutter_lbl.place(x = 2260, y = 20)

    cut_point_lbl = tk.Label(window, text = "КООРДИНАТЫ\nВЕРШИНЫ",
                             font = Graphic.font_bold,
                             bg = Colour.back)
    cut_point_lbl.place(x = 1980, y = 80)

    cut_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    cut_x_lbl.place(x = 1960, y = 200)

    cut_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    cut_y_lbl.place(x = 1960, y = 300)

    cut_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    cut_x_etr.place(x = 2060, y = 200)

    cut_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    cut_y_etr.place(x = 2060, y = 300)

    add_cut_btn = tk.Button(window, font = Graphic.font,
                                      width = 14,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Добавить",
                                      command= get_dot_etr)
    add_cut_btn.place(x = 1960, y = 410) 

    # Список точек
    dots_lbl = tk.Label(window, text = "СПИСОК ВЕРШИН",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    dots_lbl.place(x = 2450, y = 80)

    dots_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 10,
                          width = 30)
    dots_box.place(x = 2325, y = 140)

    cutter_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Замкнуть",
                                      command= close_cutter)
    cutter_btn.place(x = 1960, y = 500) 

    # Отрезок
    section_lbl = tk.Label(window, text = "ОТРЕЗОК",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    section_lbl.place(x = 2300, y = 580)

    start_lbl = tk.Label(window, text = "Координаты начала",
                             font = Graphic.font,
                             bg = Colour.back)
    start_lbl.place(x = 2220, y = 620)

    start_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    start_x_lbl.place(x = 1960, y = 680)

    start_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    start_y_lbl.place(x = 2552, y = 680)

    start_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    start_x_etr.place(x = 2060, y = 680)

    start_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    start_y_etr.place(x = 2652, y = 680)

    end_lbl = tk.Label(window, text = "Координаты конца",
                             font = Graphic.font,
                             bg = Colour.back)
    end_lbl.place(x = 2220, y = 740)

    end_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    end_x_lbl.place(x = 1960, y = 800)

    end_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    end_y_lbl.place(x = 2552, y = 800)

    end_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    end_x_etr.place(x = 2060, y = 800)

    end_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    end_y_etr.place(x = 2652, y = 800)

    section_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Нарисовать",
                                      command= get_section_etr)
    section_btn.place(x = 1960, y = 860) 

    # Выбор цвета отсекателя

    colours = ["Синий", "Зелёный", "Красный"]

    colour_cut_lbl = tk.Label(window, text = "ЦВЕТ ОТСЕКАТЕЛЯ",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_cut_lbl.place(x = 2235, y = 940)

    colour_сut_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_сut_list.place(x = 1960, y = 1000)

    for colour in colours:
        colour_сut_list.insert(tk.END, colour)

    # Выбор цвета отрезка

    colour_sec_lbl = tk.Label(window, text = "ЦВЕТ ОТРЕЗКА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_sec_lbl.place(x = 2235, y = 1140)

    colour_sec_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_sec_list.place(x = 1960, y = 1200)

    for colour in colours:
        colour_sec_list.insert(tk.END, colour)

    # Выбор цвета результата

    colour_res_lbl = tk.Label(window, text = "ЦВЕТ РЕЗУЛЬТАТА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_res_lbl.place(x = 2235, y = 1340)

    colour_res_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 40,
                             font = Graphic.font)
    colour_res_list.place(x = 1960, y = 1400)

    for colour in colours:
        colour_res_list.insert(tk.END, colour)

    cut_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Отсечь",
                                 command= cut_sections)
    cut_btn.place(x = 1960, y = 1530) 

    # Очистить экран
    clear_btn = tk.Button(window, font = Graphic.font,
                                  width = 38,
                                  bg = Colour.button,
                                  bd = 6,
                                  text = "Очистить экран",
                                  command = clear)
    clear_btn.place(x = 50, y = 1530) 

    window.mainloop()
