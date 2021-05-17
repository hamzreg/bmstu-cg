from draw import draw_dot

def reflection_z(points, center, colour, canvas):
    for i in range(len(points)):
        x = points[i][0] - center[0]
        y = points[i][1] - center[1]
        x, y = y, x
        x += center[0]
        y += center[1]
        draw_dot(x, y, colour, canvas)
        points.append([x, y])


def reflection_y(points, center, colour, canvas):
    for i in range(len(points)):
        x = points[i][0] - center[0]
        y = points[i][1] - center[1]
        x *= -1
        x += center[0]
        y += center[1]
        draw_dot(x, y, colour, canvas)
        points.append([x, y])


def reflection_x(points, center, colour, canvas):
    for i in range(len(points)):
        x = points[i][0] - center[0]
        y = points[i][1] - center[1]
        y *= -1
        x += center[0]
        y += center[1]
        draw_dot(x, y, colour, canvas)
        points.append([x, y])


def symmetrical_reflection(points, center, colour, canvas):
    reflection_z(points, center, colour, canvas)
    reflection_y(points, center, colour, canvas)
    reflection_x(points, center, colour, canvas)

