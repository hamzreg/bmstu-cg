from dataclasses import dataclass
import tkinter as tk

from draw import draw_section, draw_spectr, clear_canvas

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    window_length = 2000
    window_heigth = 1500
    window_size = "2000x1500"
    window_title = "Лабораторная работа № 3"

    font_bold = "FreeMono 14 bold"
    font = "FreeMono 14"

    canvas_heigth = 1500
    canvas_width = 1900

@dataclass
class Colour:

    back = "#ABCDEF"
    draw = "#3E8353"
    button = "#DDF1FF"
    text = "#28852F"


def create_interface():
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
                               bg = "white")
    canvas.place(x = 50, y = 50)

    # Выбор алгоритма

    algorithm_lbl = tk.Label(window, text = "Выберите алгоритм построения:",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    algorithm_lbl.place(x = 2000, y = 50)

    algorithms = ["Цифровой дифференциальный анализатор", 
                  "Брезенхем с действительными данными",
                  "Брезенхем с целочисленными данными",
                  "Брезенхем с устранением ступенчатости",
                  "Ву", "Библиотечная функция"]
    algorithm_list = tk.Listbox(selectmode = tk.SINGLE,
                               exportselection = False,
                             height = 6,
                             width = 40,
                             bd = 6,
                             font = Graphic.font)
    algorithm_list.place(x = 2000, y = 110)

    for algorithm in algorithms:
        algorithm_list.insert(tk.END, algorithm)

    # Выбор цвета

    colour_lbl = tk.Label(window, text = "Выберите цвет отрезка:",
                                  font = Graphic.font_bold,
                                  bg = Colour.back)
    colour_lbl.place(x = 2000, y = 400)

    colours = ["Синий", "Белый(фоновый)"]
    colour_list = tk.Listbox(selectmode = tk.SINGLE,
                             exportselection = False,
                             height = 2,
                             width = 40,
                             bd = 6,
                             font = Graphic.font)
    colour_list.place(x = 2000, y = 460)

    for colour in colours:
        colour_list.insert(tk.END, colour)

    # Ввод координат отрезка

    start_lbl = tk.Label(window, text = "Введите координаты начала отрезка:",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    start_lbl.place(x = 2000, y = 600)

    x_start_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_start_lbl.place(x = 2000, y = 660)

    y_start_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    y_start_lbl.place(x = 2520, y = 660)

    x_start_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    x_start_entry.insert(tk.END, "0")
    x_start_entry.place(x = 2100, y = 660)

    y_start_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    y_start_entry.insert(tk.END, "0")
    y_start_entry.place(x = 2620, y = 660)

    end_lbl = tk.Label(window, text = "Введите координаты конца отрезка:",
                               font = Graphic.font_bold,
                               bg = Colour.back)
    end_lbl.place(x = 2000, y = 720)

    x_end_lbl = tk.Label(window, text = "x:",
                             font = Graphic.font,
                             bg = Colour.back)
    x_end_lbl.place(x = 2000, y = 780)

    y_end_lbl = tk.Label(window, text = "y:",
                             font = Graphic.font,
                             bg = Colour.back)
    y_end_lbl.place(x = 2520, y = 780)

    x_end_entry = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    x_end_entry.insert(tk.END, "0")
    x_end_entry.place(x = 2100, y = 780)

    y_end_entry = tk.Entry(window, font = Graphic.font,
                                   width = 8,
                                   justify = tk.CENTER)
    y_end_entry.insert(tk.END, "0")
    y_end_entry.place(x = 2620, y = 780)

    section_button = tk.Button(window, font = Graphic.font,
                                      width = 20,
                                      bg = Colour.button,
                                      bd = 6,
                                      text = "Нарисовать отрезок",
                                      command = lambda : draw_section(canvas, algorithm_list, colour_list,
                                                                      x_start_entry, x_end_entry, y_start_entry, y_end_entry))
    section_button.place(x = 2200, y = 840)

    # Спектр

    lbl = tk.Label(window, text = "Задайте спектр:",
                                 font = Graphic.font_bold,
                                 bg = Colour.back)
    lbl.place(x = 2000, y = 960)

    length_lbl = tk.Label(window, text = "Длина:",
                             font = Graphic.font,
                             bg = Colour.back)
    length_lbl.place(x = 2000, y = 1020)

    diff_lbl = tk.Label(window, text = "Угол(°):",
                             font = Graphic.font,
                             bg = Colour.back)
    diff_lbl.place(x = 2400, y = 1020)

    length_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    length_entry.insert(tk.END, "300")
    length_entry.place(x = 2180, y = 1020)

    diff_entry = tk.Entry(window, font = Graphic.font,
                                     width = 8,
                                     justify = tk.CENTER)
    diff_entry.insert(tk.END, "20")
    diff_entry.place(x = 2620, y = 1020)

    spectr_button = tk.Button(window, font = Graphic.font,
                                      width = 20,
                                      bg = Colour.button,
                                      bd = 5,
                                      text = "Нарисовать спектр",
                                      command = lambda : draw_spectr(canvas, algorithm_list, colour_list,
                                                                     length_entry, diff_entry))
    spectr_button.place(x = 2200, y = 1080)

    # Исследование временной характеристики

    time_button = tk.Button(window, font = Graphic.font,
                                    width = 39,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Исследовать временную характеристику")
    time_button.place(x = 2000, y = 1230)

    # Исследование ступенчатости

    step_button = tk.Button(window, font = Graphic.font,
                                    width = 39,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Исследовать ступенчатость отрезков")
    step_button.place(x = 2000, y = 1300)

    # Очистить экран

    clear_button = tk.Button(window, font = Graphic.font,
                                    width = 39,
                                    bg = Colour.button,
                                    bd = 6,
                                    text = "Очистить экран",
                                    command = lambda : clear_canvas(canvas))
    clear_button.place(x = 2000, y = 1430) 

    # Закрыть

    close_button = tk.Button(window, font = Graphic.font,
                                     width = 39,
                                     bg = Colour.button,
                                     bd = 6,
                                     text = "Закрыть",
                                     command = window.destroy)
    close_button.place(x = 2000, y = 1500)

    window.mainloop()


if __name__ == "__main__":
    create_interface()
