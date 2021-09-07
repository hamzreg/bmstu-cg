import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
import copy
import numpy as np
from math import cos, sin, radians, pi
from dataclasses import dataclass

@dataclass
class Graphic:
    """
        Константы графического модуля.
    """

    BackColour = "#6dbe85"
    DrawColour = "#3e8353"
    ButtonColour = "#91c9a2"
    TextColour = "#28852f"

    Font = "FreeMono 14 bold"

    LineWidth = 3

    CanvX = 1600
    CanvY = 1600

    GridSize = 50


@dataclass
class Error:
    """
        Константы для исправления ошибок.
    """

    X = 300
    Y = 200


@dataclass
class MathConstants:
    """
        Математические константы.
    """

    MinAngle = 0
    MaxAngle = 360
    factor = 10


def CloseWindow(window, x, y):
    """
       Кнопка закрытия на окне.
    """

    CloseButton = tk.Button(window, text = "Закрыть",
                                    font = Graphic.Font,
                                    bg = Graphic.ButtonColour, 
                                    command = window.destroy)

    CloseButton.place(x = x, y = y)


def CreateMessage(message, name, PlaceX, PlaceY):
    """
        Создание окна с сообщением.
    """

    MessageWindow = tk.Tk()
    MessageWindow.title(name)
    MessageWindow.geometry("850x600")
    MessageWindow.config(bg = Graphic.BackColour)

    Message = tk.Label(MessageWindow, text = message,
                                    font = Graphic.Font,
                                    bg = Graphic.BackColour)
    Message.place(x = PlaceX, y = PlaceY)

    CloseWindow(MessageWindow, 360, 500)
    MessageWindow.mainloop()


def CheckCoordinate(coordinate):
    """
       Проверка корректности введенной точки.
    """

    for symbol in coordinate:
        if ((symbol < '0' or symbol > '9') and
            (symbol != '.' and symbol != '-')):
            return False
    
    return True


def BackOneStep():
    """
        Возврат на один шаг назад.
    """

    if (len(AllItems) == 1):
        CreateMessage('''Это начальное состояние 
изображения.''', "Предупреждение", 200, Error.Y)
        return
    
    AllItems.pop()
    
    Center(AllItems[len(AllItems) - 1][3][0][0], AllItems[len(AllItems) - 1][3][1][0])
    DrawImage(AllItems[len(AllItems) - 1][0], AllItems[len(AllItems) - 1][1], AllItems[len(AllItems) - 1][2])


def Start():
    """
        Возврат к начальному изображению.
    """

    global AllItems, Items

    InputAngle.delete(0, tk.END)
    InputAngle.insert(tk.END, "0")

    InputX.delete(0, tk.END)
    InputX.insert(tk.END, "0")

    InputY.delete(0, tk.END)
    InputY.insert(tk.END, "0")

    InputdX.delete(0, tk.END)
    InputdX.insert(tk.END, "0")

    InputdY.delete(0, tk.END)
    InputdY.insert(tk.END, "0")

    InputkX.delete(0, tk.END)
    InputkX.insert(tk.END, "1")

    InputkY.delete(0, tk.END)
    InputkY.insert(tk.END, "1")

    Center(0,0.5 * MathConstants.factor)

    Items = list(StartImage())

    AllItems.clear()

    AllItems.append(copy.deepcopy(Items))


def FindAstroid(t):
    """
       Нахождение координаты астроиды.
    """

    x = MathConstants.factor * cos(t) ** 3
    y = MathConstants.factor * sin(t) ** 3 - 0.5 * MathConstants.factor

    return x, y + MathConstants.factor


def CreateAstroid():
    """
        Создание списка координат астроид.
    """

    Astroid = [[], []]

    for i in range(MathConstants.MinAngle, MathConstants.MaxAngle + 1):
        x, y = FindAstroid(radians(i))
        Astroid[0].append(x)
        Astroid[1].append(y)
    
    return Astroid


def FindCircle(t, coeff):
    """
       Нахождение координаты окружности.
    """

    x = coeff * cos(t)
    y = coeff * sin(t) - 0.5 * MathConstants.factor

    return x, y + MathConstants.factor


def CreateCircle():
    """
        Создание списка координат окружности.
    """

    Circle = [[], []]

    for i in range(MathConstants.MinAngle, MathConstants.MaxAngle + 1):
        x, y = FindCircle(radians(i), MathConstants.factor / 3)
        Circle[0].append(x)
        Circle[1].append(y)
    
    return Circle


def DrawImage(Astroid, Circle, Cube):
    """
        Построение изображения.
    """

    CreateGraph()

    Graph.plot(Astroid[0], Astroid[1], linewidth = Graphic.LineWidth,
                                       color = Graphic.DrawColour)
    Graph.plot(Circle[0], Circle[1], linewidth = Graphic.LineWidth,
                                     color = Graphic.DrawColour)
    Graph.plot(Cube[0], Cube[1], linewidth = Graphic.LineWidth,
                                 color = Graphic.DrawColour)

    Canvas.draw()


def Center(CenterX, CenterY):
    """
        Вывод координат центра изображения.
    """

    Center = tk.Label(Window, text = f"Координаты центра изображения : {CenterX:.2f} ; {CenterY:.2f}",
                              font = Graphic.Font,
                              bg = Graphic.BackColour)
    Center.place(x = 1700, y = 90)


def StartImage():
    """
        Начальное изображение.
    """

    Astroid = CreateAstroid()
    Circle = CreateCircle()
    Cube = [[-MathConstants.factor, -MathConstants.factor, 
             MathConstants.factor, MathConstants.factor],
            [MathConstants.factor - 0.5 * MathConstants.factor, 
             -MathConstants.factor - 0.5 * MathConstants.factor,
             -MathConstants.factor - 0.5 * MathConstants.factor, 
             MathConstants.factor - 0.5 * MathConstants.factor]]
    
    C = [[0], [0.5 * MathConstants.factor - 0.5 * MathConstants.factor]]

    Center(C[0][0], C[1][0])
    DrawImage(Astroid, Circle, Cube)

    return Astroid, Circle, Cube, C


def Turn(Items, Angle, TurnX, TurnY):
    """
        Поворот изображения.
    """

    Sinus = sin(radians(Angle))
    Cosinus = cos(radians(Angle))

    Matrix = np.array([[Cosinus, -Sinus], [Sinus, Cosinus]])

    for i in range(len(Items)):
        for j in range(len(Items[i][0])):
            Items[i][0][j] -= TurnX 
            Items[i][1][j] -= TurnY

            diff = np.dot(Matrix, [Items[i][0][j], Items[i][1][j]])

            Items[i][0][j] = diff[0] + TurnX 
            Items[i][1][j] = diff[1] + TurnY

    Center(Items[3][0][0], Items[3][1][0])
    AllItems.append(copy.deepcopy(Items))    
    DrawImage(Items[0], Items[1], Items[2])


def GetTurn():
    """
       Получение значений для поворота изображения.
       Поворот.
    """

    xc = InputX.get()
    
    if not CheckCoordinate(xc):
        CreateMessage('''X центра масштабирования - 
вещественное число.''', "Ошибка", 150, Error.Y)
        return

    yc = InputY.get()

    if not CheckCoordinate(yc):
        CreateMessage('''Y центра масштабирования -
вещественное число.''', "Ошибка", 150, Error.Y)
        return

    Angle = InputAngle.get()
    
    if not CheckCoordinate(Angle):
        CreateMessage('''Угол в градусах - 
вещественное число.''', "Ошибка", 250, Error.Y)
        return
    
    Items = copy.deepcopy(AllItems[len(AllItems) - 1])
    Turn(Items, float(Angle), float(xc), float(yc))


def Scale(Items, kx, ky, ScaleX, ScaleY):
    """
        Масштабирование изображения.
    """

    for i in range(len(Items)):
        for j in range(len(Items[i][0])):
            Items[i][0][j] = kx * Items[i][0][j] + ScaleX * (1 - kx)
            Items[i][1][j] = ky * Items[i][1][j] + ScaleX * (1 - ky)


    Center(Items[3][0][0], Items[3][1][0])
    AllItems.append(copy.deepcopy(Items))    
    DrawImage(Items[0], Items[1], Items[2])


def GetScale():
    """
       Получение значений для масштабирования изображения.
       Масштабирование.
    """

    xc = InputX.get()
    
    if not CheckCoordinate(xc):
        CreateMessage('''X центра масштабирования - 
вещественное число.''', "Ошибка", 150, Error.Y)
        return

    yc = InputY.get()

    if not CheckCoordinate(yc):
        CreateMessage('''Y центра масштабирования -
вещественное число.''', "Ошибка", 150, Error.Y)
        return

    kx = InputkX.get()
    
    if not CheckCoordinate(kx):
        CreateMessage('''Коэффицент по Х - 
вещественное число.''', "Ошибка", 200, Error.Y)
        return

    ky = InputkY.get()

    if not CheckCoordinate(ky):
        CreateMessage('''Коэффициент по Y -
вещественное число.''', "Ошибка", 200, Error.Y)
        return
    
    Items = copy.deepcopy(AllItems[len(AllItems) - 1])
    Scale(Items, float(kx), float(ky), float(xc), float(yc))


def Move(Items, dx, dy):
    """
        Перенос изображения.
    """

    for i in range(len(Items)):
        for j in range(len(Items[i][0])):
            Items[i][0][j] += dx
            Items[i][1][j] += dy

    Center(Items[3][0][0], Items[3][1][0])
    AllItems.append(copy.deepcopy(Items))    
    DrawImage(Items[0], Items[1], Items[2])


def GetMove():
    """
       Получение значений для переноса изображения.
       Перенос.
    """

    dx = InputdX.get()
    
    if not CheckCoordinate(dx):
        CreateMessage('''Смещение по Х - 
вещественное число.''', "Ошибка", 200, Error.Y)
        return

    dy = InputdY.get()

    if not CheckCoordinate(dy):
        CreateMessage('''Смещение по Y -
вещественное число.''', "Ошибка", 200, Error.Y)
        return
    
    Items = copy.deepcopy(AllItems[len(AllItems) - 1])
    Move(Items, float(dx), float(dy))


def CreateGraph():
    """
       Создание чистого поля.
    """

    global Graph

    Figure.clear()

    Graph = Figure.add_subplot(1, 1, 1)
    Graph.set_xlim([-Graphic.GridSize, Graphic.GridSize])
    Graph.set_ylim([-Graphic.GridSize, Graphic.GridSize])
    Graph.tick_params(labelsize = 20)
    Graph.grid()

    Figure.subplots_adjust(right = 0.97, left = 0.06, bottom = 0.06, top = 0.97)

    Canvas.draw()


if __name__ == "__main__":
    """
        Создание основных графических объектов.
    """

    Window = tk.Tk()
    Window.title("Лабораторная работа № 2")
    Window.geometry("2000x1500")
    Window.config(bg=Graphic.BackColour)

    AllItems = []

    Figure = plt.Figure(facecolor=Graphic.BackColour)
    Canvas = FigureCanvasTkAgg(Figure, master = Window)
    canvas = Canvas.get_tk_widget()
    canvas.place(x = 0, y = 0, width = Graphic.CanvX, height = Graphic.CanvY)
    CreateGraph()

    Items = list(StartImage())

    AllItems.append(copy.deepcopy(Items))
    Canvas.draw()

    # Условие и об авторе

    CondButton = tk.Button(Window, text = "Показать условие",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : CreateMessage('''
    Нарисовать рисунок, затем
    его перенести,
    промасштабировать, повернуть.
    Уравнение астроиды : 
        x = b * cos ^ 3 (t)
        y = b * sin ^ 3 (t)
        t ∈ [0;2π]''', "Условие", 50, 100))
    CondButton.place(x = 1700, y = 10)

    AuthorButton = tk.Button(Window, text = "Об авторе",
                                     bg = Graphic.ButtonColour,
                                     font = Graphic.Font,
                                     command = lambda : CreateMessage('''
    Программа выполнена
    Хамзиной Региной.
    Группа : ИУ7-43Б.''', "Об авторе", 150, 150))
    AuthorButton.place(x = 2120, y = 10)

    # Перенос

    MoveLbl = tk.Label(Window, text = "Введите смещение по x и y для переноса :",
                               font = Graphic.Font,
                               bg = Graphic.BackColour)
    MoveLbl.place(x = 1700, y = 170)

    LbldX = tk.Label(Window, text = "dX : ",
                             font = Graphic.Font,
                             bg = Graphic.BackColour)
    LbldX.place(x = 1700, y = 250)

    InputdX = tk.Entry(Window, font = Graphic.Font,
                               bg = Graphic.ButtonColour)
    InputdX.insert(tk.END, "0")
    InputdX.place(x = 1800, y = 250)

    LbldY = tk.Label(Window, text = "dY : ",
                             font = Graphic.Font,
                             bg = Graphic.BackColour)
    LbldY.place(x = 1700, y = 330)

    InputdY = tk.Entry(Window, font = Graphic.Font,
                               bg = Graphic.ButtonColour)
    InputdY.insert(tk.END, "0")
    InputdY.place(x = 1800, y = 330)

    MoveButton = tk.Button(Window, text = "Перенести",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : GetMove())
    MoveButton.place(x = 1700, y = 410)

    # Центр поворота и масштабирования

    ChangeCenter = tk.Label(Window, text = "Введите координаты центра поворота и масштабирования :",
                                    font = Graphic.Font,
                                    bg = Graphic.BackColour)
    ChangeCenter.place(x = 1700, y = 490)

    LblX = tk.Label(Window, text = "X : ",
                            font = Graphic.Font,
                            bg = Graphic.BackColour)
    LblX.place(x = 1700, y = 570)

    InputX = tk.Entry(Window, font = Graphic.Font,
                              bg = Graphic.ButtonColour)
    InputX.insert(tk.END, "0")
    InputX.place(x = 1800, y = 570)

    LblY = tk.Label(Window, text = "Y : ",
                            font = Graphic.Font,
                            bg = Graphic.BackColour)
    LblY.place(x = 1700, y = 650)

    InputY = tk.Entry(Window, font = Graphic.Font,
                              bg = Graphic.ButtonColour)
    InputY.insert(tk.END, "0")
    InputY.place(x = 1800, y = 650)

    # Масштабирование

    ScaleLbl = tk.Label(Window, text = "Введите коэффициенты масштабирования по x и y :",
                                font = Graphic.Font,
                                bg = Graphic.BackColour)
    ScaleLbl.place(x = 1700, y = 730)

    LblkX = tk.Label(Window, text = "kX : ",
                             font = Graphic.Font,
                             bg = Graphic.BackColour)
    LblkX.place(x = 1700, y = 810)

    InputkX = tk.Entry(Window, font = Graphic.Font,
                               bg = Graphic.ButtonColour)
    InputkX.insert(tk.END, "1")
    InputkX.place(x = 1800, y = 810)

    LblkY = tk.Label(Window, text = "kY : ",
                             font = Graphic.Font,
                             bg = Graphic.BackColour)
    LblkY.place(x = 1700, y = 890)

    InputkY = tk.Entry(Window, font = Graphic.Font,
                               bg = Graphic.ButtonColour)
    InputkY.insert(tk.END, "1")
    InputkY.place(x = 1800, y = 890)

    MoveButton = tk.Button(Window, text = "Масштабировать",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : GetScale())
    MoveButton.place(x = 1700, y = 970)

    # Поворот

    TurnLbl = tk.Label(Window, text = "Введите угол поворота :",
                               font = Graphic.Font,
                               bg = Graphic.BackColour)
    TurnLbl.place(x = 1700, y = 1050)

    InputAngle = tk.Entry(Window, font = Graphic.Font,
                                  bg = Graphic.ButtonColour)
    InputAngle.insert(tk.END, "0")
    InputAngle.place(x = 1700, y = 1110)

    TurnButton = tk.Button(Window, text = "Повернуть",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : GetTurn())
    TurnButton.place(x = 1700, y = 1190)

    # Возврат

    BackButton = tk.Button(Window, text = "Вернуться на один шаг назад",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : BackOneStep())
    BackButton.place(x = 1700, y = 1350)

    StartButton = tk.Button(Window, text = "Вернуться к исходному изображению",
                                   bg = Graphic.ButtonColour,
                                   font = Graphic.Font,
                                   command = lambda : Start())
    StartButton.place(x = 1700, y = 1430)

    # Закрыть

    CloseWindow(Window, 1700, 1510)

    Window.mainloop()
