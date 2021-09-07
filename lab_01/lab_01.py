from math import degrees, acos, sqrt, ceil
import tkinter as tk

Font = "Garamond 10 bold"
ErrorX = 300
ErrorY = 200

InvalidCoordinate = 0
R = 7
MaxX = 1000
MaxY = 680
XCenter = 1100
YCenter = 787.5
TriangleDots = 3

NotExist = 0
Exist = 1

EPS = 1e-7


def CreateMessage(message, name, PlaceX, PlaceY):
    """
        Создание окна с сообщением.
    """

    AnswerWindow = tk.Tk()
    AnswerWindow.title(name)
    AnswerWindow.geometry("850x600")
    AnswerWindow.config(bg = '#EEB78E')

    Answer = tk.Label(AnswerWindow, text = message,
                                    font = Font,
                                    fg = '#1C4825',
                                    bg = '#EEB78E')
    Answer.place(x = PlaceX, y = PlaceY)

    CloseWindow(AnswerWindow, 360, 500)
    AnswerWindow.mainloop()


def FindCross(FirstDot, SecondDot, Height):
    """
        Нахождение точки пересечения высоты
        и противоположной стороны.
    """

    Side = {}
    Side['a'] = FirstDot['y'] - SecondDot['y']
    Side['b'] = SecondDot['x'] - FirstDot['x']
    Side['c'] = FirstDot['x'] * SecondDot['y'] - SecondDot['x'] * FirstDot['y']

    denominator = Side['a'] * Height['b'] \
                  - Height['a'] * Side['b']
    
    Cross = {}
    Cross['x'] = (Height['c'] * Side['b'] - 
         Side['c'] * Height['b']) \
        / denominator
    
    Cross['y'] = (Height['a'] * Side['c'] - 
         Side['a'] * Height['c']) \
        / denominator

    return Cross


def DrawTriangle(MaxNumbers, Dots, factor, GraphItems):
    """
        Вывод треугольника в графическом формате.
    """

    Triangle = MainCanvas.create_polygon(Dots[0][MaxNumbers[0]] / factor + XCenter,
                                         YCenter - Dots[1][MaxNumbers[0]] / factor,
                                         Dots[0][MaxNumbers[1]] / factor + XCenter,
                                         YCenter - Dots[1][MaxNumbers[1]] / factor,
                                         Dots[0][MaxNumbers[2]]  / factor +XCenter,
                                         YCenter - Dots[1][MaxNumbers[2]] / factor,
                                         fill = "",
                                         outline = 'green',
                                         width = 5)
    GraphItems.append(Triangle)


def DrawDots(Dots, GraphDots, Numbers, factor):
    """
        Вывод точек в графическом формате.
    """
    for i in range(len(Dots[0])):
        Dot = MainCanvas.create_oval(Dots[0][i] / factor + XCenter + R,
                                     YCenter - Dots[1][i]  / factor + R,
                                     Dots[0][i] / factor + XCenter - R,
                                     YCenter - Dots[1][i] / factor - R,
                                     fill = "red",
                                     width = 0)
        GraphDots.append(Dot)

        numb = MainCanvas.create_text(Dots[0][i] / factor + XCenter + 3 * R,
                                      YCenter - Dots[1][i] / factor - 3 * R,
                                      text = str(i + 1),
                                      font = Font)
        Numbers.append(numb)


def DrawAngle(GraphItems, MaxOrthocenter, MaxAngle, factor):
    """
        Вывод угла в графическом формате.
    """

    AngleLine = MainCanvas.create_line(XCenter, YCenter,
                                       MaxOrthocenter['x'] / factor + XCenter,
                                       YCenter - MaxOrthocenter['y'] / factor,
                                       fill = 'darkblue',
                                       width = 5)
    GraphItems.append(AngleLine)

    if MaxOrthocenter['x'] > 0:
        Turn = MaxAngle * (-1)
    else:
        Turn = MaxAngle

    Angle = MainCanvas.create_arc(XCenter - 100, YCenter - 100,
                                  XCenter + 100, YCenter + 100,
                                  start=90, extent= Turn, 
                                  style=tk.ARC, outline='darkblue', 
                                  width=5)
    GraphItems.append(Angle)

    ResultOrthocentr = MainCanvas.create_oval(MaxOrthocenter['x'] / factor + XCenter + R,
                                              YCenter - MaxOrthocenter['y']/ factor + R,
                                              MaxOrthocenter['x'] / factor + XCenter - R,
                                              YCenter - MaxOrthocenter['y']/ factor - R,
                                              fill = "yellow")
    GraphItems.append(ResultOrthocentr)


def DrawHeights(FirstDot, SecondDot, ThirdDot,
MaxFirstHeight, MaxSecondHeight, MaxThirdHeight,
MaxNumbers, factor, MaxOrthocenter):
    """
        Вывод высот в графическом виде.
    """

    Cross = FindCross(FirstDot, SecondDot, MaxFirstHeight)
    Part1Height1 = MainCanvas.create_line(Dots[0][MaxNumbers[2]]  / factor + XCenter,
                                          YCenter - Dots[1][MaxNumbers[2]] / factor,
                                          Cross['x'] / factor  + XCenter,
                                          YCenter - Cross['y'] / factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part1Height1)
    Part2Height1 = MainCanvas.create_line(MaxOrthocenter['x'] / factor + XCenter,
                                          YCenter - MaxOrthocenter['y'] / factor,
                                          Cross['x']  / factor  + XCenter,
                                          YCenter - Cross['y']/ factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part2Height1)

    Cross = FindCross(SecondDot, ThirdDot, MaxSecondHeight)
    Part1Height2 = MainCanvas.create_line(Dots[0][MaxNumbers[0]] / factor + XCenter,
                                          YCenter - Dots[1][MaxNumbers[0]] / factor,
                                          Cross['x'] / factor + XCenter,
                                          YCenter - Cross['y']/ factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part1Height2)
    Part2Height2 = MainCanvas.create_line(MaxOrthocenter['x']  / factor + XCenter,
                                          YCenter - MaxOrthocenter['y']/ factor,
                                          Cross['x'] / factor + XCenter,
                                          YCenter - Cross['y']/ factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part2Height2)

    Cross = FindCross(FirstDot, ThirdDot, MaxThirdHeight)
    Part1Height3 = MainCanvas.create_line(Dots[0][MaxNumbers[1]] / factor + XCenter,
                                          YCenter - Dots[1][MaxNumbers[1]] / factor,
                                          Cross['x'] / factor + XCenter,
                                          YCenter - Cross['y']/ factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part1Height3)
    Part2Height3 = MainCanvas.create_line(MaxOrthocenter['x']  / factor + XCenter,
                                          YCenter - MaxOrthocenter['y']/ factor,
                                          Cross['x'] / factor + XCenter,
                                          YCenter - Cross['y']/ factor,
                                          fill = 'blue',
                                          width = 5)
    GraphItems.append(Part2Height3)


def FindFactor(Dots, Orthocenter):
    """
       Нахождение коэффициента масштабирования.
    """

    x = abs(Dots[0][0])
    y = abs(Dots[1][0])

    for i in range(len(Dots[0])):
        if (abs(Dots[0][i]) - x) > EPS:
            x = abs(Dots[0][i])

        if (abs(Dots[1][i]) - y) > EPS:
            y = abs(Dots[1][i])

    if abs(Orthocenter['x']) - x > EPS:
        x = abs(Orthocenter['x'])
    if abs(Orthocenter['y']) - y > EPS:
        y = abs(Orthocenter['y'])
    
    if x - MaxX > EPS:
        if y - MaxY > EPS:
            if y / MaxY - x/MaxX > EPS:
                return ceil(y / MaxY)
        
        return ceil(x / MaxX)
    
    if y - MaxY > EPS:
        return ceil(y / MaxY)
    

    return 1


def FindAngle(Orthocenter):
    """
        Найти угол между осью ординат и 
        прямой, соединяющей ортоцентр и 
        начало координат.
    """

    VectorLen = sqrt(Orthocenter['x'] ** 2 \
          + Orthocenter['y'] ** 2)
    AngleCos = Orthocenter['y'] / VectorLen
    
    return degrees(acos(AngleCos))


def FindOrthocenter(FirstHeight, SecondHeight):
    """
        Найти координаты ортоцентра.
    """

    denominator = FirstHeight['a'] * SecondHeight['b'] \
                  - SecondHeight['a'] * FirstHeight['b']
    
    Orthocenter = {}
    Orthocenter['x'] = (SecondHeight['c'] * FirstHeight['b'] - 
         FirstHeight['c'] * SecondHeight['b']) \
        / denominator
    
    Orthocenter['y'] = (SecondHeight['a'] * FirstHeight['c'] - 
         FirstHeight['a'] * SecondHeight['c']) \
        / denominator

    return Orthocenter


def FindHeight(FirstDot, SecondDot, ThirdDot):
    """
        Найти параметры высоты.
    """

    Height = {}

    Height['a'] = SecondDot['x'] - FirstDot['x']
    Height['b'] = SecondDot['y'] - FirstDot['y']
    Height['c'] = (-1) * Height['a'] * ThirdDot['x'] \
                  - Height['b'] * ThirdDot['y']
    
    return Height


def GetAngle(FirstDot, SecondDot, ThirdDot):
    """
        Найти высоты, ортоцентр и получить угол.
    """

    FirstHeight = FindHeight(FirstDot, SecondDot, ThirdDot)
    SecondHeight = FindHeight(SecondDot, ThirdDot, FirstDot)
    ThirdHeight = FindHeight(FirstDot, ThirdDot, SecondDot)
    Orthocenter = FindOrthocenter(FirstHeight, SecondHeight)
    
    return FindAngle(Orthocenter), FirstHeight, SecondHeight, ThirdHeight, Orthocenter


def CheckTriangle(FirstDot, SecondDot, ThirdDot):
    """
       Проверить, можно ли построить треугольник
       на данных точках.
    """

    FirstSide = ((SecondDot['x'] - FirstDot['x']) ** 2 \
                + (SecondDot['y'] - FirstDot['y']) ** 2) ** 0.5
    SecondSide = ((ThirdDot['x'] - SecondDot['x']) ** 2 \
                + (ThirdDot['y'] - SecondDot['y']) ** 2) ** 0.5
    ThirdSide =  ((ThirdDot['x'] - FirstDot['x']) ** 2 \
                + (ThirdDot['y'] - FirstDot['y']) ** 2) ** 0.5
    
    if (FirstSide + SecondSide) <= ThirdSide or \
        (FirstSide + ThirdSide) <= SecondSide or \
            (SecondSide + ThirdSide) <= FirstSide:
        return NotExist
    
    return Exist
    

def Solve(Dots, GraphItems, GraphDots, Numbers):
    """
        Решение.
    """

    CountDots = len(Dots[0])
    CountTriangles = 0

    if CountDots < TriangleDots:
        CreateMessage('''Необходимо ввести
минимум три точки.''', "Ошибка", ErrorX, ErrorY)
        return

    First, Second, Third = {}, {}, {}
    MaxAngle = 0
    MaxOrthocenter = {}
    MaxFirstHeight, MaxSecondHeight, MaxThirdHeight = {}, {}, {}
    MaxNumbers = []

    for first in range(CountDots - 2):
        First['x'] = Dots[0][first]
        First['y'] = Dots[1][first]
        for second in range(first + 1, CountDots - 1):
            Second['x'] = Dots[0][second]
            Second['y'] = Dots[1][second]
            for third in range(second + 1, CountDots):
                Third['x'] = Dots[0][third]
                Third['y'] = Dots[1][third]

                if not CheckTriangle(First, Second, Third):
                    continue

                CountTriangles += 1
                Angle, FirstHeight, SecondHeight, \
                ThirdHeigth, Orthocenter  = GetAngle(First, Second, Third)

                if Angle >= MaxAngle:
                    MaxAngle = Angle
                    MaxNumbers.clear()

                    MaxNumbers.append(first)
                    MaxNumbers.append(second)
                    MaxNumbers.append(third)

                    MaxOrthocenter = Orthocenter
                    MaxFirstHeight, MaxSecondHeight, \
                    MaxThirdHeight = FirstHeight, SecondHeight, ThirdHeigth
    
    if CountTriangles == 0:
        CreateMessage('''Нельзя составить 
треугольник по заданным точкам.''', "Ошибка", ErrorX - 100, ErrorY)
        return

    factor = FindFactor(Dots, MaxOrthocenter) * 0.05

    DrawTriangle(MaxNumbers, Dots, factor, GraphItems)

    FirstDot, SecondDot, ThirdDot = {}, {}, {}
    FirstDot['x'] = Dots[0][MaxNumbers[0]]
    FirstDot['y'] = Dots[1][MaxNumbers[0]]
    SecondDot['x'] = Dots[0][MaxNumbers[1]]
    SecondDot['y'] = Dots[1][MaxNumbers[1]]
    ThirdDot['x'] = Dots[0][MaxNumbers[2]]
    ThirdDot['y'] = Dots[1][MaxNumbers[2]]
    DrawHeights(FirstDot, SecondDot, ThirdDot,
                MaxFirstHeight, MaxSecondHeight, MaxThirdHeight,
                MaxNumbers, factor, MaxOrthocenter)
    DrawDots(Dots, GraphDots, Numbers, factor)
    DrawAngle(GraphItems, MaxOrthocenter, MaxAngle, factor)

    CreateMessage(f'''
Искомый треугольник образован 
{MaxNumbers[0] + 1} точкой с координатами {FirstDot['x']:.2f};{FirstDot['y']:.2f},
{MaxNumbers[1] + 1} точкой с координатами {SecondDot['x']:.2f};{SecondDot['y']:.2f},
{MaxNumbers[2] + 1} точкой с координатами {ThirdDot['x']:.2f};{ThirdDot['y']:.2f}.

Максимальный угол : {MaxAngle:.2f} °.

Красным цветом обозначены точки.
Зеленым цветом изображается треугольник.
Синим цветом изображаются высоты.
Темно-синим цветом изображается угол.
Желтым цветом обозначается отроцентр.
''', "Ответ", 100, 50)


def CloseWindow(window, x, y):
    """
       Кнопка закрытия на окне.
    """

    BClose = tk.Button(window, text = "Закрыть",
                                font = Font,
                                fg = '#1C4825',
                                bg = 'white', 
                                command = window.destroy)
                                
    BClose.place(x = x, y = y)


def CheckCoordinate(coordinate):
    """
       Проверка корректности введенной точки.
    """

    for symbol in coordinate:
        if ((symbol < '0' or symbol > '9') and
            (symbol != '.' and symbol != '-')):
            return InvalidCoordinate
    
    return True


def DrawDot(event):
    """
       Рисовать точку.
    """

    x = event.x
    y = event.y 

    DotsCount.set(DotsCount.get() + 1)
    Number = str(DotsCount.get())
    Dots[0].append(x - XCenter)
    Dots[1].append(YCenter - y)
    DotsBox.insert(tk.END, Number + ":  {" + str(x - XCenter) + " ; " + str(YCenter - y) + "}")
    # MainCanvas.create_oval(x+R, y+R, x-R, y-R,
    #                        fill = "red",
    #                        width = 0)
    # numb = MainCanvas.create_text(x + 2 * R, y - 2 * R,
    #                               text = Number,
    #                               font = Font)
    # Numbers.append(numb)


def AddDot(Dots, Numbers):
    """
        Добавление точки.
    """

    x = XInput.get()
    
    if not CheckCoordinate(x):
        XInput.delete(0, tk.END)
        YInput.delete(0, tk.END)
        CreateMessage('''Неверно введена 
координата X.''', "Ошибка", ErrorX, ErrorY)
        return

    y = YInput.get()

    if not CheckCoordinate(y):
        XInput.delete(0, tk.END)
        YInput.delete(0, tk.END)
        CreateMessage('''Неверно введена 
координата Y.''', "Ошибка", ErrorX, ErrorY)
        return

    if len(x) == 0 or len(y) == 0:
        CreateMessage('''Координаты точки 
не заданы.''', "Ошибка", ErrorX, ErrorY)
        return
    
    DotsCount.set(DotsCount.get() + 1)
    Number = str(DotsCount.get())
    DotsBox.insert(tk.END, Number + ":  {" + x + " ; " + y + "}")
    Dots[0].append(float(x))
    Dots[1].append(float(y))

    XInput.delete(0, tk.END)
    YInput.delete(0, tk.END)


def ChangeList(index, Dots, XEntry, YEntry):
    """
        Изменение точки в списке.
    """

    x = XEntry.get()
    y = YEntry.get()
    if not CheckCoordinate(x):
        CreateMessage('''Неверно введена 
координата X.''', "Ошибка", ErrorX, ErrorY)
        return

    if not CheckCoordinate(y):
        CreateMessage('''Неверно введена 
координата Y.''', "Ошибка", ErrorX, ErrorY)
        return

    if len(x) == 0 or len(y) == 0:
        CreateMessage('''Координаты точки 
не заданы.''', "Ошибка", ErrorX, ErrorY)
        return

    DotsBox.delete(index)
    DotsBox.insert(index, str(index + 1) + ":  {" + x + " ; " + y + "}")

    Dots[0][index] = float(x)
    Dots[1][index] = float(y)


def ChangeDot():
    """
        Изменение точки.
    """

    select = DotsBox.curselection()

    if len(select) == 0:
        CreateMessage('''Не выделена точка
для изменения.''', "Ошибка", ErrorX, ErrorY)
        return

    for i in select:
        index = int(i)

    Window = tk.Tk()
    Window.title("Изменение координаты")
    Window.geometry("850x500")
    Window.config(bg = '#EEB78E')

    LInput = tk.Label(Window, text = 'Введите координаты точек:',
                              font = Font,
                              fg = '#1C4825',
                              bg = '#EEB78E')
    LInput.place(x = 100, y = 100)

    XLbl = tk.Label(Window, text = 'X: ',
                            font = Font,
                            fg = '#1C4825',
                            bg = '#EEB78E')
    XLbl.place(x = 50, y = 180)

    XEntry = tk.Entry(Window, font = Font,
                              fg = '#1C4825',
                              bg = 'white',
                              width = 25)
    XEntry.place(x = 150, y = 180)

    YLbl = tk.Label(Window, text = 'Y: ',
                            font = Font,
                            fg = '#1C4825',
                            bg = '#EEB78E')
    YLbl.place(x = 50, y = 260)

    YEntry = tk.Entry(Window, font = Font,
                              fg = '#1C4825',
                              bg = 'white',
                              width = 25)
    YEntry.place(x = 150, y = 260)

    BOk = tk.Button(Window, text = "Ок",
                            font = Font,
                            fg = '#1C4825',
                            bg = 'white', 
                            command = lambda : ChangeList(index, Dots,
                                                      XEntry, YEntry))
    BOk.place(x = 100, y = 400)
    CloseWindow(Window, 300,400)

    
    Window.mainloop()


def DelDot(Dots, Numbers):
    """
        Удаление точки.
    """

    select = DotsBox.curselection()

    if len(select) == 0:
        CreateMessage('''Не выделена точка
для удаления.''', "Ошибка", ErrorX, ErrorY)
        return

    for i in select:
        index = int(i)

    Dots[0].pop(index)
    Dots[1].pop(index)
    MainCanvas.delete(GraphDots[index])
    DotsBox.delete(select)
    MainCanvas.delete(Numbers[index])
    Numbers.pop(index)
    GraphDots.pop(index)


def DelSolve(Items):
    """
        Удаление объектов решения.
    """

    CountItems = len(Items)

    if CountItems == 0:
        CreateMessage('''Решение еще
не построено.''', "Ошибка", ErrorX, ErrorY)
        return
    
    for i in range(CountItems):
        MainCanvas.delete(Items[i])


def DelAllDots(Dots, Numbers):
    """
        Удаление всех точек.
    """

    if DotsBox.size() == 0:
        CreateMessage('''На плоскости нет
точек.''', "Ошибка", ErrorX, ErrorY)
        return

    count = len(Dots[0])

    for i in range(count):
        DotsBox.delete(0)
        MainCanvas.delete(Numbers[i])
        MainCanvas.delete(GraphDots[i])

    Dots[0].clear()
    Dots[1].clear()
    DotsCount.set(0)
    Numbers.clear()
    GraphItems.clear()


Dots = [[],[]]
Numbers = []

MainWindow = tk.Tk()
MainWindow.title("Лабораторная работа № 1")
MainWindow.geometry("2000x1500")
MainWindow.config(bg = '#EEB78E')

DotsCount = tk.IntVar()
DotsCount.set(0)

MainCanvas = tk.Canvas(MainWindow, width = 2200,
                                   height = 1575,
                                   bg = "white",
                                   cursor = "pencil")
MainCanvas.place(x = 10, y = 10)

GraphItems = []
GraphDots = []

MainCanvas.create_line(XCenter, 2200, XCenter, 0,
                       fill='black',
                       width=2,
                       arrow=tk.LAST,
                       arrowshape="10 20 10")
MainCanvas.create_line(0, YCenter, 2200, YCenter,
                       fill='black',
                       width=2,
                       arrow=tk.LAST,
                       arrowshape="10 20 10")
MainCanvas.create_oval(XCenter+R, YCenter+R, XCenter-R, YCenter-R,
                       fill = "black",
                       width = 0)

DotsBox = tk.Listbox(selectmode = tk.EXTENDED,
                     height = 25,
                     width = 35)
DotsBox.place(x = 2230, y = 330)

BCondition = tk.Button(MainWindow, text = "Условие задачи",
                                   font = Font,
                                   fg = '#1C4825',
                                   bg = 'white', 
                                   command = lambda : CreateMessage(f'''
Задайте множество точек:
в поле 'x:' введите координату точки x,
в поле 'y:' введите координату точки y.
Программа найдет такой треугольник с 
вершинами в этих точках, у которого угол,
образованный прямой, соединяющей точку 
пересечения высот и начало координат, и
осью ординат максимален.
Изображение появится на белом холсте.''', "Условие задачи", 100, 100))
BCondition.place(x = 2230, y = 10)

BAuthor = tk.Button(MainWindow, text = "Об авторе",
                                font = Font,
                                fg = '#1C4825',
                                bg = 'white', 
                                command = lambda : CreateMessage(f'''
Программа выполнена Хамзиной Региной.
Группа : ИУ7-43Б.''', "Об авторе", 100, 200))
BAuthor.place(x = 2550, y = 10)

LInput = tk.Label(MainWindow, text = 'Введите координаты точек:',
                              font = Font,
                              fg = '#1C4825',
                              bg = '#EEB78E')
LInput.place(x = 2300, y = 90)

XInputLbl = tk.Label(MainWindow, text = 'X: ',
                              font = Font,
                              fg = '#1C4825',
                              bg = '#EEB78E')
XInputLbl.place(x = 2230, y = 170)
XInput = tk.Entry(MainWindow, font = Font,
                              fg = '#1C4825',
                              bg = 'white',
                              width = 25)
XInput.place(x = 2280, y = 170)
YInputLbl = tk.Label(MainWindow, text = 'Y: ',
                              font = Font,
                              fg = '#1C4825',
                              bg = '#EEB78E')
YInputLbl.place(x = 2230, y = 250)
YInput = tk.Entry(MainWindow, font = Font,
                              fg = '#1C4825',
                              bg = 'white',
                              width = 25)
YInput.place(x = 2280, y = 250)

BInput = tk.Button(MainWindow, text = "Добавить точку",
                               font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : AddDot(Dots, Numbers))
BInput.place(x = 2230, y = 1200)


BChange = tk.Button(MainWindow, text = "Изменить точку",
                                font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : ChangeDot())
BChange.place(x = 2550, y = 1200)


BDel = tk.Button(MainWindow, text = "Удалить точку",
                               font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : DelDot(Dots, Numbers))
BDel.place(x = 2230, y = 1280)

BDelAllDots = tk.Button(MainWindow, text = "Удалить все точки",
                               font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : DelAllDots(Dots, Numbers))
                               
BDelAllDots.place(x = 2550, y = 1280)

BSolve = tk.Button(MainWindow, text = "Получить решение",
                               font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : Solve(Dots, GraphItems,
                                                        GraphDots, Numbers))
BSolve.place(x = 2230, y = 1360)

BDelSolve = tk.Button(MainWindow, text = "Удалить решение",
                               font = Font,
                               fg = '#1C4825',
                               bg = 'white', 
                               command = lambda : DelSolve(GraphItems))
                               
BDelSolve.place(x = 2570, y = 1360)



CloseWindow(MainWindow, 2230, y = 1440)
MainCanvas.bind('<1>', DrawDot)
MainWindow.mainloop()
