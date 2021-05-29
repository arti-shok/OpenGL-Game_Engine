from OpenGL.GL import *
from math import cos, sin, pi


def cylinder():
    r = 0.5

    glBegin(GL_TRIANGLE_FAN)

    glVertex3d(0, 0, -0.5)
    for i in range(21):
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20),
                   -0.5)

    glEnd()

    glBegin(GL_QUAD_STRIP)

    for i in range(21):
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20), -0.5)
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20), 0.5)

    glEnd()

    glBegin(GL_TRIANGLE_FAN)

    glVertex3d(0, 0, 0.5)
    for i in range(21):
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20), 0.5)

    glEnd()


def cone():
    r = 0.5

    glBegin(GL_TRIANGLE_FAN)

    glVertex3d(0, 0, -0.5)
    for i in range(21):
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20), -0.5)

    glEnd()

    glBegin(GL_TRIANGLE_FAN)

    glVertex3d(0, 0, 0.5)
    for i in range(21):
        glVertex3d(r * cos(2 * pi * i / 20),
                   r * sin(2 * pi * i / 20), -0.5)

    glEnd()


def sphere(r=0.5, dx=0, dy=0, dz=0):

    for j in range(-9, 9):
        glBegin(GL_QUAD_STRIP)
        for i in range(21):
            glVertex3d(r * cos(pi * j / 18) * cos(2 * pi * i / 20) + dx,
                       r * cos(pi * j / 18) * sin(2 * pi * i / 20) + dy,
                       r * sin(pi * j / 18) + dz)
            glVertex3d(r * cos(pi * (j + 1) / 18) * cos(2 * pi * i / 20) + dx,
                       r * cos(pi * (j + 1) / 18) * sin(2 * pi * i / 20) + dy,
                       r * sin(pi * (j + 1) / 18) + dz)

        glEnd()


def thor():
    r = 0.5
    r2 = r * 0.3

    for i in range(20):
        glBegin(GL_QUAD_STRIP)

        for j in range(21):
            glVertex3d((r + r2 * cos(2 * pi * j / 20)) * cos(2 * pi * i / 20),
                       (r + r2 * cos(2 * pi * j / 20)) * sin(2 * pi * i / 20),
                       r2 * sin(2 * pi * j / 20))
            glVertex3d((r + r2 * cos(2 * pi * j / 20)) * cos(2 * pi * (i + 1) / 20),
                       (r + r2 * cos(2 * pi * j / 20)) * sin(2 * pi * (i + 1) / 20),
                       r2 * sin(2 * pi * j / 20))

        glEnd()


def cube(a=0.5, dx=0, dy=0, dz=0):
    glBegin(GL_QUADS)
    glVertex3d(a + dx, a + dy, a + dz)
    glVertex3d(-a + dx, a + dy, a + dz)
    glVertex3d(-a + dx, -a + dy, a + dz)
    glVertex3d(a + dx, -a + dy, a + dz)

    glVertex3d(a + dx, a + dy, -a + dz)
    glVertex3d(-a + dx, a + dy, -a + dz)
    glVertex3d(-a + dx, -a + dy, -a + dz)
    glVertex3d(a + dx, -a + dy, -a + dz)

    glVertex3d(a + dx, a + dy, a + dz)
    glVertex3d(a + dx, a + dy, -a + dz)
    glVertex3d(a + dx, -a + dy, -a + dz)
    glVertex3d(a + dx, -a + dy, a + dz)

    glVertex3d(-a + dx, a + dy, a + dz)
    glVertex3d(-a + dx, a + dy, -a + dz)
    glVertex3d(-a + dx, -a + dy, -a + dz)
    glVertex3d(-a + dx, -a + dy, a + dz)

    glVertex3d(a + dx, a + dy, a + dz)
    glVertex3d(a + dx, a + dy, -a + dz)
    glVertex3d(-a + dx, a + dy, -a + dz)
    glVertex3d(-a + dx, a + dy, a + dz)

    glVertex3d(a + dx, -a + dy, a + dz)
    glVertex3d(a + dx, -a + dy, -a + dz)
    glVertex3d(-a + dx, -a + dy, -a + dz)
    glVertex3d(-a + dx, -a + dy, a + dz)

    glEnd()


def tex_landscape(w, h, a, h_map, k):
    for _x in range(w - 1):
        for _y in range(h - 1):
            if _x % 2 == 1 and _y % 2 == 1:

                glBegin(GL_TRIANGLE_FAN)
                glTexCoord2f((_x % k) / k, (_y % k) / k)
                glVertex3d(_x / a, _y / a, h_map[_x][_y])
                tx = 1 if (_x + 1) % k == 0 else ((_x + 1) % k) / k
                # if (_x + 1) % k == 0:
                #     tx = 1
                # else:
                #     tx = ((_x + 1) % k) / k

                if (_y + 1) % k == 0:
                    ty = 1
                else:
                    ty = ((_y + 1) % k) / k

                glTexCoord2f(tx, (_y % k) / k)
                glVertex3d((_x + 1) / a, _y / a, h_map[_x + 1][_y])

                glTexCoord2f(tx, ty)
                glVertex3d((_x + 1) / a, (_y + 1) / a, h_map[_x + 1][_y + 1])

                glTexCoord2f((_x % k) / k, ty)
                glVertex3d(_x / a, (_y + 1) / a, h_map[_x][_y + 1])

                glTexCoord2f(((_x - 1) % k) / k, ty)
                glVertex3d((_x - 1) / a, (_y + 1) / a, h_map[_x - 1][_y + 1])

                glTexCoord2f(((_x - 1) % k) / k, (_y % k) / k)
                glVertex3d((_x - 1) / a, _y / a, h_map[_x - 1][_y])

                glTexCoord2f(((_x - 1) % k) / k, ((_y - 1) % k) / k)
                glVertex3d((_x - 1) / a, (_y - 1) / a, h_map[_x - 1][_y - 1])

                glTexCoord2f((_x % k) / k, ((_y - 1) % k) / k)
                glVertex3d(_x / a, (_y - 1) / a, h_map[_x][_y - 1])

                glTexCoord2f(tx, ((_y - 1) % k) / k)
                glVertex3d((_x + 1) / a, (_y - 1) / a, h_map[_x + 1][_y - 1])

                glTexCoord2f(tx, (_y % k) / k)
                glVertex3d((_x + 1) / a, _y / a, h_map[_x + 1][_y])

                glEnd()


def sky_box(width=2, height=2, h=128, x0=0, y0=0, z0=0):
    glBegin(GL_QUADS)
    glTexCoord2f(0.25, 0.75)
    glVertex3f(x0, y0, z0 + h)
    glTexCoord2f(0.5, 0.75)
    glVertex3f(x0 + width, y0, z0 + h)
    glTexCoord2f(0.5, 1.0)
    glVertex3f(x0 + width, y0 + height, z0 + h)
    glTexCoord2f(0.25, 1.0)
    glVertex3f(x0, y0 + height, z0 + h)  # up
    
    glTexCoord2f(0.25, 0.5)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(0.25, 0.25)
    glVertex3f(x0, y0 + height, z0)
    glTexCoord2f(0.5, 0.25)
    glVertex3f(x0 + width, y0 + height, z0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(x0 + width, y0, z0)  # down
    
    glTexCoord2f(1.0, 0.5)
    glVertex3f(x0, y0 + height, z0)
    glTexCoord2f(1.0, 0.75)
    glVertex3f(x0, y0 + height, z0 + h)
    glTexCoord2f(0.75, 0.75)
    glVertex3f(x0 + width, y0 + height, z0 + h)
    glTexCoord2f(0.75, 0.5)
    glVertex3f(x0 + width, y0 + height, z0)
    
    glTexCoord2f(0.25, 0.5)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(0.5, 0.5)
    glVertex3f(x0 + width, y0, z0)
    glTexCoord2f(0.5, 0.75)
    glVertex3f(x0 + width, y0, z0 + h)
    glTexCoord2f(0.25, 0.75)
    glVertex3f(x0, y0, z0 + h)  # left
    
    glTexCoord2f(0.5, 0.5)
    glVertex3f(x0 + width, y0, z0)
    glTexCoord2f(0.75, 0.5)
    glVertex3f(x0 + width, y0 + height, z0)
    glTexCoord2f(0.75, 0.75)
    glVertex3f(x0 + width, y0 + height, z0 + h)
    glTexCoord2f(0.5, 0.75)
    glVertex3f(x0 + width, y0, z0 + h)  # front
    
    glTexCoord2f(0.25, 0.5)
    glVertex3f(x0, y0, z0)
    glTexCoord2f(0.25, 0.75)
    glVertex3f(x0, y0, z0 + h)
    glTexCoord2f(0., 0.75)
    glVertex3f(x0, y0 + height, z0 + h)
    glTexCoord2f(0., 0.5)
    glVertex3f(x0, y0 + height, z0)  # back
    glEnd()
