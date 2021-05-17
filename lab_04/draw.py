from dataclasses import dataclass
import tkinter as tk
from tkinter import messagebox

@dataclass
class Constants:
    x_center = 1000
    y_center = 750

def clear_canvas(canvas):
    canvas.delete(tk.ALL)

def draw_dot(x, y, colour, canvas):
    """
        Рисование точки.
    """

    canvas.create_line(x, y, x + 1, y, fill = colour)