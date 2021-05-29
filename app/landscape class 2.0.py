from vector_alg import *
from get_landscape import *
from draws import *
from texture import *
from short_ray import *

from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *

from time import time

map1 = "../maps/map.bmp"
map2 = "../maps/map2.jpg"
map3 = "../maps/egor.jpg"
map5 = "../maps/map5.jpg"
map6 = "../maps/map6.jpg"
tex_grass1 = "../textures/map.jpg"
tex_grass2 = "../textures/grass 2.jpg"
skybox1 = "../textures/SkyBox.jpg"
skybox2 = "../textures/skybox_sand.jpg"
skybox3 = "../textures/skybox_woow.jpg"



window_width = 1000
window_height = 800


class App:
    def __init__(self, name_map, name_texture, name_skybox):
        glEnable(GL_DEPTH_TEST)
        glClearColor(1.0, 1.0, 1.0, 1.0)  # Белый цвет для первоначальной закраски
        glMatrixMode(GL_PROJECTION)  # Выбираем матрицу проекций
        glLoadIdentity()  # Сбрасываем все предыдущие трансформации
        gluPerspective(90, window_width / window_height, 0.1, 1000)  # Задаем перспективу
        # gluOrtho2D(-1.0, 1.0, -1.0, 1.0) # Определяем границы рисования по горизонтали и вертикали

        self._h, self._width, self._height = get_landscape(name_map, 2)
        self._a = 1

        self._angle_x = 0
        self._angle_y = 0
        self._angle_z = 0
        self._zoom = 5.0
        self._filled = 0

        self._obj_pos = Vector3(self._width // 2, self._height // 2,
                                get_height(self._width // 2, self._height // 2, self._h))
        self._obj_dir = Vector3(10, 0, 0).norm()

        #  self._obj_up = get_normal(self._obj_pos.x, self._obj_pos.y, self._h)
        self._obj_up = Vector3(0, 0, 1)

        __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
        self._cam_pos = self._obj_pos.plus_v(__d_pos)
        self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

        self._speed = 20
        self._rotate_speed = 25

        self._tex_id = load_texture_image(name_texture)
        self._sky_box_id = load_texture_image(name_skybox)
        self._tex_k = 16

        self._prev_time = time()
        self._d_time = 0

        self._display_list = glGenLists(1)
        glNewList(self._display_list, GL_COMPILE)
        glEnable(GL_TEXTURE_2D)
        glColor3d(1, 1, 1)
        glBindTexture(GL_TEXTURE_2D, self._tex_id)
        tex_landscape(self._width, self._height, self._a, self._h, self._tex_k)

        glBindTexture(GL_TEXTURE_2D, self._sky_box_id)
        sky_box(width=self._width, height=self._height, z0=-(self._width + self._height) // 4,
                h=(self._width + self._height) // 2)
        glEndList()

        self._button_list = [0] * 7

    def up_keyboard_keys(self, key, x, y):
        if key == b'w':
            self._button_list[0] = 0
        if key == b's':
            self._button_list[1] = 0
        if key == b'a':
            self._button_list[2] = 0
        if key == b'd':
            self._button_list[3] = 0
        if key == b'-':
            self._button_list[4] = 0
        if key == b'=':
            self._button_list[5] = 0
        if key == b' ':
            self._button_list[6] = 0

    def special_keyboard_keys(self, key, x, y):
        pass

    def common_keyboard_keys(self, key, x, y):
        if key == b'\x1b':
            sys.exit(0)
        if key == b'w':  # вперед назад
            self._button_list[0] = 1
        if key == b's':
            self._button_list[1] = 1

        if key == b'a':  # рыскание
            self._button_list[2] = 1
        if key == b'd':
            self._button_list[3] = 1

        if key == b'-':  # приближение
            self._button_list[4] = 1
        if key == b'=':
            self._button_list[5] = 1
            self._zoom *= 1.1
        if key == b' ':
            self._button_list[6] = 1

        glutPostRedisplay()  # Вызываем процедуру перерисовки

    def draw(self, *args, **kwargs):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)  # Очищаем экран и заливаем текущим цветом фона
        glMatrixMode(GL_MODELVIEW)  # Выбираем модельно-видовую матрицу
        glLoadIdentity()  # Сбрасываем все предыдущие трансформации

        __curr_time = time()
        self._d_time = __curr_time - self._prev_time
        self._prev_time = __curr_time
        print(self._button_list[6])
        if self._button_list[0] == 1:
            self._obj_pos = self._obj_pos.plus_v(self._obj_dir.x_r(self._speed * self._d_time))
            self._obj_pos.z = get_height(int(self._obj_pos.x * self._a), int(self._obj_pos.y * self._a), self._h)
        if self._button_list[1] == 1:
            self._obj_pos = self._obj_pos.minus_v(self._obj_dir.x_r(self._speed * self._d_time))
            self._obj_pos.z = get_height(int(self._obj_pos.x * self._a), int(self._obj_pos.y * self._a), self._h)
        if self._button_list[2] == 1:
            __m = Matrix3x3.m_rot(self._obj_up, self._d_time * self._rotate_speed * -pi / 90)
            self._obj_dir = __m.x_v(self._obj_dir)
            self._obj_dir.z = 0
            self._obj_dir = self._obj_dir.norm()
        if self._button_list[3] == 1:
            __m = Matrix3x3.m_rot(self._obj_up, self._d_time * self._rotate_speed * pi / 90)
            self._obj_dir = __m.x_v(self._obj_dir)
            self._obj_dir.z = 0
            self._obj_dir = self._obj_dir.norm()
        if self._button_list[4] == 1:
            self._zoom += 10 * self._d_time
        if self._button_list[5] == 1:
            self._zoom -= 10 * self._d_time
        if self._button_list[6] == 1:
            self._filled = 1 - self._filled


        __d_pos = (self._obj_up.x_r(self._zoom)).minus_v(self._obj_dir.x_r(self._zoom))
        self._cam_pos = self._obj_pos.plus_v(__d_pos)
        self._cam_up = (self._obj_up.x_v(self._obj_dir)).x_v(__d_pos)

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



        # glBindTexture(GL_TEXTURE_2D, self._tex_id)
        # tex_landscape(self._width, self._height, self._a, self._h, self._tex_k)
        glCallList(self._display_list)

        glDisable(GL_TEXTURE_2D)
        glColor3d(1, 0, 0)
        cube(1, self._obj_pos.x, self._obj_pos.y, self._obj_pos.z + 1)
        glutSwapBuffers()  # Меняем буферы
        glutPostRedisplay()  # Вызываем процедуру перерисовки


if __name__ == "__main__":
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(window_width, window_height)
    glutInitWindowPosition(0, 0)
    glutCreateWindow(b"AAAAAAAAA!")

    app = App(map6, tex_grass2, skybox3)
    glutDisplayFunc(app.draw)
    # Определяем процедуру, отвечающую за обработку обычных клавиш
    glutIgnoreKeyRepeat(1)
    glutKeyboardUpFunc(app.up_keyboard_keys)

    glutKeyboardFunc(app.common_keyboard_keys)
    glutSpecialFunc(app.special_keyboard_keys)

    # Вызываем нашу функцию инициализации

    glutMainLoop()
