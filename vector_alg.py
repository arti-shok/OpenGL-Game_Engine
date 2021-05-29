import math


class Vector3:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return "(%.2f, %.2f, %.2f)" % (self.x, self.y, self.z)

    def len(self):
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def norm(self):
        ln = self.len()
        if ln == 0:
            return Vector3(0, 0, 0)
        else:
            _x = self.x / ln
            _y = self.y / ln
            _z = self.z / ln
            return Vector3(_x, _y, _z)

    def x_r(self, r):
        try:
            b = float(r)
            _x = self.x * b
            _y = self.y * b
            _z = self.z * b
            return Vector3(_x, _y, _z)
        except ValueError:
            print("value err")

    def plus_v(self, vec):
        _x = self.x + vec.x
        _y = self.y + vec.y
        _z = self.z + vec.z
        return Vector3(_x, _y, _z)

    def minus_v(self, vec):
        _x = self.x - vec.x
        _y = self.y - vec.y
        _z = self.z - vec.z
        return Vector3(_x, _y, _z)

    def dot_v(self, vec):
        return self.x * vec.x + self.y * vec.y + self.z * vec.z

    def x_v(self, vec):
        return Vector3(self.y*vec.z - self.z*vec.y, self.z*vec.x - self.x*vec.z, self.x*vec.y - self.y*vec.x)


class Matrix3x3:
    def __init__(self, vec1, vec2, vec3):
        self.a = vec1
        self.b = vec2
        self.c = vec3

    def __str__(self):
        return f"({self.a}, {self.b}, {self.c})"

    @staticmethod
    def e():
        return Matrix3x3(Vector3(1., 0., 0.),
                         Vector3(0., 1., 0.),
                         Vector3(0., 0., 1.))

    def x_r(self, r):
        try:
            _a = self.a.x_r(r)
            _b = self.b.x_r(r)
            _c = self.c.x_r(r)
            return Matrix3x3(_a, _b, _c)
        except ValueError:
            print("value err")

    def plus_m(self, mat):
        _a = self.a.plus_v(mat.a)
        _b = self.b.plus_v(mat.b)
        _c = self.c.plus_v(mat.c)
        return Matrix3x3(_a, _b, _c)

    def minus_m(self, mat):
        _a = self.a.minus_v(mat.a)
        _b = self.b.minus_v(mat.b)
        _c = self.c.minus_v(mat.c)
        return Matrix3x3(_a, _b, _c)

    def x_v(self, vec):
        return Vector3(self.a.dot_v(vec), self.b.dot_v(vec), self.c.dot_v(vec))

    def x_m(self, mat):
        _vec1 = Vector3(mat.a.x, mat.b.x, mat.c.x)
        _vec2 = Vector3(mat.a.y, mat.b.y, mat.c.y)
        _vec3 = Vector3(mat.a.z, mat.b.z, mat.c.z)
        m_t = Matrix3x3(_vec1, _vec2, _vec3)

        _a = m_t.x_v(self.a)
        _b = m_t.x_v(self.b)
        _c = m_t.x_v(self.c)

        return Matrix3x3(_a, _b, _c)

    @staticmethod
    def m_rot(vec, phi):
        _e = Matrix3x3.e()
        _s = Matrix3x3(Vector3(0, vec.z, -vec.y),
                       Vector3(-vec.z, 0, vec.x),
                       Vector3(vec.y, -vec.x, 0))
        _m1 = _s.x_r(math.sin(phi))
        _m2 = (_s.x_m(_s)).x_r(1-math.cos(phi))
        return _e.plus_m(_m1.plus_m(_m2))
