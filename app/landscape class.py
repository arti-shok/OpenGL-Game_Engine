from vector_alg import *
from get_landscape import *
from draws import *
from texture import *
from short_ray import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *


map1 = "maps/map.bmp"
map2 = "maps/map2.jpg"
map3 = "maps/egor.jpg"
map5 = "maps/map5.jpg"
tex_grass1 = "textures/map.jpg"
tex_grass2 = "textures/grass 2.jpg"

window_width = 1000
window_height = 800


class App:
    def __init__(self, name_map, name_texture):
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Белый цвет для первоначальной закраски
        glMatrixMode(GL_PROJECTION)  # Выбираем матрицу проекций
        glLoadIdentity()  # Сбрасываем все предыдущие трансформации
        gluPerspective(90, window_width / window_height, 0.01, 100)  # Задаем перспективу
        # gluOrtho2D(-1.0, 1.0, -1.0, 1.0) # Определяем границы рисования по горизонтали и вертикали

        self._h, self._width, self._height = get_landscape(name_map, 10)
        self._a = 1

        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0
        self._zoom = 5.0
        self._filled = 0

        self._obj_pos = Vector3(2, 2, self._h[2][2])
        self._obj_dir = Vector3(10, 0, 0).norm()
        #  self._obj_up = get_normal(self._obj_pos.x, self._obj_pos.y, self._h)
        self._obj_up = Vector3(0, 0, 1)

        __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
        self._cam_pos = self._obj_pos.plus_v(__d_pos)
        self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        self._speed = 1
        self._rotate_speed = 10

        self._tex_id = load_texture_image(name_texture)
        self._tex_k = 2

    def keyboard_keys(self, key, x, y):
        if key == b'\x1b':
            sys.exit(0)

        if key == b'w':  # вперед назад/
            self._obj_pos = self._obj_pos.plus_v(self._obj_dir.x_r(self._speed))
            self._obj_pos.z = get_height(self._obj_pos.x, self._obj_pos.y, self._h)
            __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
            self._cam_pos = self._obj_pos.plus_v(__d_pos)
            self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        if key == b's':
            self._obj_pos = self._obj_pos.minus_v(self._obj_dir.x_r(self._speed))
            self._obj_pos.z = get_height(self._obj_pos.x, self._obj_pos.y, self._h)
            __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
            self._cam_pos = self._obj_pos.plus_v(__d_pos)
            self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        if key == b'a':  # рыскание

            __m = Matrix3x3.m_rot(self._obj_up, self._rotate_speed * -pi / 90)
            #__m = Matrix3x3.m_rot(self._obj_up, self._rotate_speed * -pi / 90)
            self._obj_dir = __m.x_v(self._obj_dir)
            self._obj_dir.z = 0
            __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
            self._cam_pos = self._obj_pos.plus_v(__d_pos)
            self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        if key == b'd':
            __m = Matrix3x3.m_rot(self._obj_up, self._rotate_speed * pi / 90)
            self._obj_dir = __m.x_v(self._obj_dir)
            self._obj_dir.z = 0
            self._obj_dir = self._obj_dir.norm()
            __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
            self._cam_pos = self._obj_pos.plus_v(__d_pos)
            self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        # if key == b'q':  # крен
        #     __m = Matrix3x3.m_rot(self._cube_pos, self._rotate_speed * pi / 90)
        #     self._cam_up = __m.x_v(self._cam_up
        # if key == b'e':
        #     __m = Matrix3x3.m_rot(self._cube_pos, self._rotate_speed * -pi / 90)
        #     self._cam_up = __m.x_v(self._cam_up)

        # if key == b'o':  #  тангаж
        #     __v = self._cube_pos.x_v(self._cam_up)
        #     __m = Matrix3x3.m_rot(__v, self._rotate_speed * -pi / 90)
        #     self._cube_pos = __m.x_v(self._cube_pos)
        #     self._cam_up = __m.x_v(self._cam_up)
        #
        # if key == b'p':
        #     __v = self._cube_pos.x_v(self._cam_up)
        #     __m = Matrix3x3.m_rot(__v, self._rotate_speed * pi / 90)
        #     self._cube_pos = __m.x_v(self._cube_pos)
        #     self._cam_up = __m.x_v(self._cam_up)

        if key == b'-':  # приближение
            self._zoom /= 1.1
        if key == b'=':
            self._zoom *= 1.1
        if key == b' ':
            self._filled = 1 - self._filled

        glutPostRedisplay()  # Вызываем процедуру перерисовки

    def draw(self, *args, **kwargs):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем текущим цветом фона
        glMatrixMode(GL_MODELVIEW)  # Выбираем модельно-видовую матрицу
        glLoadIdentity()  # Сбрасываем все предыдущие трансформации
        gluLookAt(self._cam_pos.x, self._cam_pos.y, self._cam_pos.z,  # Положение камеры
                  self._obj_pos.x,
                  self._obj_pos.y,
                  self._obj_pos.z,  # Точка, на которую смотрит камера
                  self._cam_up.x, self._cam_up.y, self._cam_up.z)  # Направление "верх" камеры
        glRotated(self._angle_x, 1, 0, 0)
        glRotated(self._angle_y, 0, 1, 0)
        glRotated(self._angle_z, 0, 0, 1)
        # glRotated(-105, 1, 0, 0)
        if self._filled == 1:
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        else:
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

        cube(1, self._obj_pos.x, self._obj_pos.y, self._obj_pos.z)

        glBindTexture(GL_TEXTURE_2D, self._tex_id)
        tex_landscape(self._width, self._height, self._a, self._h, self._tex_k)

        glutSwapBuffers()  # Меняем буферы
        glutPostRedisplay()  # Вызываем процедуру перерисовки


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"AAAAAAAAA!")

    app = App(map2, tex_grass2)
    glutDisplayFunc(app.draw)
    # Определяем процедуру, отвечающую за обработку обычных клавиш
    glutKeyboardFunc(app.keyboard_keys)
    # Вызываем нашу функцию инициализации

    glutMainLoop()
