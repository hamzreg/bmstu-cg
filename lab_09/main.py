from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

from itertools import combinations
import copy


@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 9"

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


def draw_result(figure):
    """
        Нарисовать результат.
    """

    colour = get_result_colour()

    for edge in figure:
        canvas.create_line(edge[0], edge[1], fill= colour[1])


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


def is_point(figure):
    """
        Является ли фигура точкой.
    """

    prev = figure[0]

    for i in range(1, len(figure)):
        if figure[i][0] != prev[0] or figure[i][1] != prev[1]:
            return False
        
        prev = figure[i]
    
    return True


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

    if sign < 0:
        cutter.reverse()

    return True


# Отсечение
def remove_false(sides):
    """
        Удаление ложных ребер.
    """

    for side in sides:
        side.sort()

    return list(filter(lambda x: (sides.count(x) % 2) == 1, sides))


def is_dot_on_side(dot, side):
    """
        Принадлежит ли точка
        отрезку.
    """

    if abs(get_vector_mul(get_vector(dot, side[0]), get_vector(side[1], side[0]))) <= 1e-6:
        if side[0] < dot < side[1] or \
           side[1] < dot < side[0]:
            return True
    return False


def get_sides(side, rest_dots):
    """
        Получение простых отрезков
        многоугольников.
    """

    dots_list = [side[0], side[1]]

    for dot in rest_dots:
        if is_dot_on_side(dot, side):
            dots_list.append(dot)

    dots_list.sort()

    sections_list = list()

    for i in range(len(dots_list) - 1):
        sections_list.append([dots_list[i], dots_list[i + 1]])

    return sections_list


def remove_odd_sides(figure):
    """
       Удаление ложных ребер.
    """

    all_sides = list()
    rest_dots = figure[2:]

    for i in range(len(figure)):
        now_side = [figure[i], figure[(i + 1) % len(figure)]]

        all_sides.extend(get_sides(now_side, rest_dots))

        rest_dots.pop(0)
        rest_dots.append(figure[i])

    return remove_false(all_sides)


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


def is_visible(point, point_f, point_s):
    """
        Проверка видимости при помощи
        векторного произведения.
    """

    first = get_vector(point_f, point_s)
    second = get_vector(point_f, point)

    if get_vector_mul(first, second) <= 0:
        return True
    else:
        return False


def get_intersection(section, edge, normal):
    """
    """

    d = get_vector(section[0], section[1])
    w = get_vector(edge[0], section[0])

    d_scalar = get_scalar_mul(d, normal)
    w_scalar = get_scalar_mul(w, normal)

    t = -w_scalar / d_scalar

    intersection = [section[0][0] + d[0] * t, section[0][1] + d[1] * t]

    return intersection


def sutherland_hodgman(section, position, prev):
    """
        Алгоритм Сазерленда-Ходжмена
        отсечения многоугольников.
    """

    result = []

    first = section[0]
    second = section[1]

    normal = get_normal(first, second, position)

    prev_vision = is_visible(prev[-2], first, second)

    for i in range(-1, len(prev)):
        now_vision = is_visible(prev[i], first, second)

        if prev_vision:
            if now_vision:
                result.append(prev[i])
            else:
                figure_line = [prev[i - 1], prev[i]]

                result.append(get_intersection(figure_line, section, normal))
        else:
            if now_vision:
                figure_line = [prev[i - 1], prev[i]]

                result.append(get_intersection(figure_line, section, normal))

                result.append(prev[i])

        prev_vision = now_vision

    return result


def cut_polygons():
    """
        Отсечение многоугольников.
    """

    if len(cutter) < 3:
        messagebox.showinfo("Ошибка", "Необходимо задать отсекатель.")
        return

    if len(polygon) < 3:
        messagebox.showinfo("Ошибка", "Необходимо задать многоугольник.")
        return

    if not is_closed(cutter):
        messagebox.showinfo("Ошибка", "Необходимо замкнуть отсекатель.")
        return

    if not is_closed(polygon):
        messagebox.showinfo("Ошибка", "Необходимо замкнуть многоугольник.")
        return

    if not check_cutter():
        messagebox.showinfo("Ошибка", "Отсекатель должен быть выпуклым многоугольником.")
        return
    
    if is_point(cutter):
        messagebox.showerror("Ошибка", "Отсекатель не должен быть точкой.")
        return

    result = copy.deepcopy(polygon)

    for i in range(-1, len(cutter) - 1):
        edge = [cutter[i], cutter[i + 1]]

        position = cutter[i + 1]

        result = sutherland_hodgman(edge, position, result)

        if len(result) <= 2:
            return

    result = remove_odd_sides(result)
    draw_result(result)


# Работа с холстом
def clear():
    """
        Очищение экрана.
    """

    canvas.delete(tk.ALL)

    cutter.clear()
    polygon.clear()
    edges.clear()

    dots_pol_box.delete(0, tk.END)
    dots_cut_box.delete(0, tk.END)


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


def get_polygon_colour():
    """
        Выбор цвета многоугольника.
    """

    for i in colour_pol_list.curselection():
        index = int(i)
    colour = colour_pol_list.get(index)

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


def is_closed(figure):
    """
        Замкнута ли фигура.
    """

    closed = False

    if (len(figure) > 3):
        if ((figure[0][0] == figure[-1][0]) and \
            (figure[0][1] == figure[-1][1])):
            closed = True

    return closed


# Работа с многоугольником
def add_pol_dot(x, y, last = False):
    """
       Создание многоугольника.
    """

    polygon.append([x, y])
    now_index = len(polygon)

    if (not last):
        dots_pol_box.insert(tk.END, "{0}. ({1:-4.2f};{2:-4.2f})".format(now_index, x, y))

    if (len(polygon) > 1):
        colour = get_polygon_colour()
        canvas.create_line(polygon[-2], polygon[-1], fill= colour[1])


def get_click_pol_dot(event):
    """
        Получение координат вершин
        многоугольника, задаваемых мышкой.
    """

    x = event.x
    y = event.y

    add_pol_dot(x, y)


def get_pol_dot_etr():
    """
        Получение координат вершин
        многоугольника, задаваемых в 
        полях ввода.
    """

    try:
        x = int(pol_x_etr.get())
        y = int(pol_y_etr.get())
    except:
        messagebox.showerror("Ошибка",
                             "Координаты вершины должны быть числами.")
        return
    
    add_pol_dot(x, y)


def close_polygon():
    """
        Замкнуть многоугольник.
    """

    if (len(polygon) < 3):
        messagebox.showerror("Ошибка",
                             "Для того, чтобы замкнуть фигуру нужно хотя бы 3 точки.")
        return
    
    add_pol_dot(polygon[0][0], polygon[0][1], last = True)


# Работа с отсекателем
def add_cut_dot(x, y, last = False):
    """
       Создание отсекателя.
    """

    cutter.append([x, y])
    now_index = len(cutter)

    if (not last):
        dots_cut_box.insert(tk.END, "{0}. ({1:-4.2f};{2:-4.2f})".format(now_index, x, y))

    if (len(cutter) > 1):
        colour = get_cutter_colour()
        canvas.create_line(cutter[-2], cutter[-1], fill= colour[1])


def get_click_cut_dot(event):
    """
        Получение координат вершин
        отcекателя, задаваемых мышкой.
    """

    x = event.x
    y = event.y

    add_cut_dot(x, y)


def get_cut_dot_etr():
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
    
    add_cut_dot(x, y)


def close_cutter():
    """
        Замкнуть отсекатель.
    """

    if (len(cutter) < 3):
        messagebox.showerror("Ошибка",
                             "Для того, чтобы замкнуть фигуру нужно хотя бы 3 точки.")
        return
    
    add_cut_dot(cutter[0][0], cutter[0][1], last = True)
    

if __name__ == "__main__":
    """
        Создание графического интерфейса.
    """

    window = tk.Tk()
    window.title(Graphic.window_title)
    window.geometry(Graphic.window_size)
    window.config(bg = Colour.back)

    # Отсекатель
    cutter = []
    # Многоугольник
    polygon = []
    # Ребра
    edges = []

    # Холст
    canvas = tk.Canvas(window, width = Graphic.canvas_width,
                               height = Graphic.canvas_heigth,
                               bg = Colour.white)
    canvas.place(x = 50, y = 50)

    canvas.bind("<3>", get_click_pol_dot)
    canvas.bind("<1>", get_click_cut_dot)


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
                                      command= get_cut_dot_etr)
    add_cut_btn.place(x = 1960, y = 410) 

    # Список точек отсекателя
    dots_cut_lbl = tk.Label(window, text = "СПИСОК ВЕРШИН",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    dots_cut_lbl.place(x = 2450, y = 80)

    dots_cut_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 10,
                          width = 30)
    dots_cut_box.place(x = 2325, y = 140)

    cutter_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Замкнуть",
                                      command= close_cutter)
    cutter_btn.place(x = 1960, y = 500) 

    # Многоугольник
    polygon_lbl = tk.Label(window, text = "МНОГОУГОЛЬНИК",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    polygon_lbl.place(x = 2260, y = 580)

    pol_point_lbl = tk.Label(window, text = "КООРДИНАТЫ\nВЕРШИНЫ",
                             font = Graphic.font_bold,
                             bg = Colour.back)
    pol_point_lbl.place(x = 1980, y = 640)

    pol_x_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    pol_x_lbl.place(x = 1960, y = 760)

    pol_y_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    pol_y_lbl.place(x = 1960, y = 860)

    pol_x_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    pol_x_etr.place(x = 2060, y = 760)

    pol_y_etr = tk.Entry(window, font = Graphic.font,
                             width = 8,
                             justify = tk.CENTER)
    pol_y_etr.place(x = 2060, y = 860)

    add_pol_btn = tk.Button(window, font = Graphic.font,
                                      width = 14,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Добавить")
    add_pol_btn.place(x = 1960, y = 970) 

    # Список точек многоугольника
    dots_pol_lbl = tk.Label(window, text = "СПИСОК ВЕРШИН",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    dots_pol_lbl.place(x = 2450, y = 640)

    dots_pol_box = tk.Listbox(selectmode = tk.EXTENDED,
                          height = 10,
                          width = 30)
    dots_pol_box.place(x = 2325, y = 700)

    polygon_btn = tk.Button(window, font = Graphic.font,
                                      width = 38,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Замкнуть",
                                      command= close_polygon)
    polygon_btn.place(x = 1960, y = 1060) 

    # Выбор цвета отсекателя
    colours = ["Синий", "Зелёный", "Красный"]

    colour_cut_lbl = tk.Label(window, text = "ЦВЕТ\nОТСЕКАТЕЛЯ",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_cut_lbl.place(x = 1960, y = 1160)

    colour_сut_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 10,
                             font = Graphic.font)
    colour_сut_list.place(x = 1960, y = 1280)

    for colour in colours:
        colour_сut_list.insert(tk.END, colour)

    # Выбор цвета отрезка

    colour_pol_lbl = tk.Label(window, text = "ЦВЕТ\nМНОГОУГОЛЬНИКА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_pol_lbl.place(x = 2240, y = 1160)

    colour_pol_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 10,
                             font = Graphic.font)
    colour_pol_list.place(x = 2280, y = 1280)

    for colour in colours:
        colour_pol_list.insert(tk.END, colour)

    # Выбор цвета результата

    colour_res_lbl = tk.Label(window, text = "ЦВЕТ\nРЕЗУЛЬТАТА",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_res_lbl.place(x = 2610, y = 1160)

    colour_res_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 3,
                             width = 10,
                             font = Graphic.font)
    colour_res_list.place(x = 2610, y = 1280)

    for colour in colours:
        colour_res_list.insert(tk.END, colour)

    cut_btn = tk.Button(window, font = Graphic.font,
                                 width = 38,
                                 bg = Colour.button,
                                 bd = 6,
                                 text = "Отсечь",
                                 command= cut_polygons)
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
