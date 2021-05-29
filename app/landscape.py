
from vector_alg import *
from get_landscape import *
from draws import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


from random import random
colors = [(random(), random(), random()) for i in range(5)]


a = 1
name1 = "map.bmp"
name2 = "map2.jpg"
name3 = "map3.jpg"
h, _width, _height = get_landscape(name1, 5)


window_width = 800
window_height = 600


# Процедура инициализации
def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(1.0, 1.0, 1.0, 1.0)  # Белый цвет для первоначальной закраски
    glMatrixMode(GL_PROJECTION)  # Выбираем матрицу проекций
    glLoadIdentity()  # Сбрасываем все предыдущие трансформации
    gluPerspective(90, window_width / window_height, 0.01, 100)  # Задаем перспективу
    # gluOrtho2D(-1.0, 1.0, -1.0, 1.0) # Определяем границы рисования по горизонтали и вертикали
    global anglex, angley, anglez, zoom, filled, _pos, _dir, _up, _speed
    anglex = 0
    angley = 0
    anglez = 0
    zoom = 1.0
    filled = 0
    _pos = Vector3(0.92, 29.53, -38.59)
    _dir = Vector3(0.67, -0.71, 0.23)
    _up = Vector3(0.71, 0.67, 0)
    _speed = 2


# Процедура обработки обычных клавиш
def keyboardkeys(key, x, y):
    global anglex, angley, anglez, zoom, filled, _pos, _dir, _up, _speed
    if key == b'\x1b':
        sys.exit(0)
    if key == b'w':  # вперед назад
        _pos = _pos.plus_v(_dir.x_r(_speed))
    if key == b's':
        _pos = _pos.minus_v(_dir.x_r(_speed))

    if key == b'q':  # крен
        _m = Matrix3x3.m_rot(_dir, pi / 90)
        _up = _m.x_v(_up)
    if key == b'e':
        _m = Matrix3x3.m_rot(_dir, -pi / 90)
        _up = _m.x_v(_up)

    if key == b'a':  # рыскание
        _m = Matrix3x3.m_rot(_up, -pi / 90)
        _dir = _m.x_v(_dir)
    if key == b'd':
        _m = Matrix3x3.m_rot(_up, pi / 90)
        _dir = _m.x_v(_dir)

    if key == b'o':
        _v = _dir.x_v(_up)
        _m = Matrix3x3.m_rot(_v, -pi / 90)
        _dir = _m.x_v(_dir)
        _up = _m.x_v(_up)
    if key == b'p':
        _v = _dir.x_v(_up)
        _m = Matrix3x3.m_rot(_v, pi / 90)
        _dir = _m.x_v(_dir)
        _up = _m.x_v(_up)

    if key == b'-':  # приближение
        zoom /= 1.1
    if key == b'=':
        zoom *= 1.1
    if key == b' ':
        filled = 1 - filled
    glutPostRedisplay()  # Вызываем процедуру перерисовки


# Процедура рисования
def draw(*args, **kwargs):
    global anglex, angley, anglez, zoom, filled, _pos, _dir, _up, _speed, _width, _height

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем текущим цветом фона
    glMatrixMode(GL_MODELVIEW)  # Выбираем модельно-видовую матрицу
    glLoadIdentity()  # Сбрасываем все предыдущие трансформации
    gluLookAt(_pos.x, _pos.y, _pos.z,  # Положение камеры
              _pos.x + _dir.x * zoom, _pos.y + _dir.y * zoom, _pos.z + _dir.z * zoom,
              # Точка, на которую смотрит камера
              _up.x, _up.y, _up.z)  # Направление "верх" камеры
    glRotated(anglex, 1, 0, 0)
    glRotated(angley, 0, 1, 0)
    glRotated(anglez, 0, 0, 1)
    glRotated(-105, 1, 0, 0)
    if filled == 1:
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
    else:
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    for _x in range(_width - 1):
        for _y in range(_height - 1):
            if _x % 2 == 1 and _y % 2 == 1:
                color = colors[(_x + _y) % 5]
                glColor3f(*color)

                glBegin(GL_TRIANGLE_FAN)
                glVertex3d(_x / a, _y / a, h[_x][_y])

                glVertex3d((_x + 1) / a, _y / a, h[_x + 1][_y])
                glVertex3d((_x + 1) / a, (_y + 1) / a, h[_x + 1][_y + 1])
                glVertex3d(_x / a, (_y + 1) / a, h[_x][_y + 1])
                glVertex3d((_x - 1) / a, (_y + 1) / a, h[_x - 1][_y + 1])
                glVertex3d((_x - 1) / a, _y / a, h[_x - 1][_y])
                glVertex3d((_x - 1) / a, (_y - 1) / a, h[_x - 1][_y - 1])
                glVertex3d(_x / a, (_y - 1) / a, h[_x][_y - 1])
                glVertex3d((_x + 1) / a, (_y - 1) / a, h[_x + 1][_y - 1])
                glVertex3d((_x + 1) / a, _y / a, h[_x + 1][_y])

                glEnd()

    glutSwapBuffers()  # Меняем буферы
    glutPostRedisplay()  # Вызываем процедуру перерисовки


glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
glutInitWindowSize(window_width, window_height)
glutInitWindowPosition(50, 50)
glutInit(sys.argv)
glutCreateWindow(b"OpenGL Second Program!")
# Определяем процедуру, отвечающую за рисование
glutDisplayFunc(draw)
# Определяем процедуру, отвечающую за обработку обычных клавиш
glutKeyboardFunc(keyboardkeys)
# Вызываем нашу функцию инициализации
init()
glutMainLoop()
