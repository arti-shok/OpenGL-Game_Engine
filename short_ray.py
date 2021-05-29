from vector_alg import Vector3, Matrix3x3
from get_landscape import get_landscape


def sign(x):
	if x > 0:
		return 1
	elif x < 0:
		return -1
	elif x == 0:
		return 0


def get_h_map(filename):
	with open(filename, "r") as file:
		_w = int(file.readline())
		_h = int(file.readline())
		_h_map = []
		for _x in range(_w):
			_h_map.append([])
			for _y in range(_h):
				_h_map[_x].append(float(file.readline()))
	return _h_map


def get_height(x, y, h_map):
	_x = int(x)
	_y = int(y)
	if _x == x and _y == y:
		return h_map[x][y]
	if (_x + _y) % 2 == 0:
		_p1 = _x, _y, h_map[_x][_y]
		_p2 = _x + 1, _y + 1, h_map[_x + 1][_y + 1]
		if x - _x > y - _y:
			_p3 = _x + 1, _y, h_map[_x + 1][_y]
		else:
			_p3 = _x, _y + 1, h_map[_x][_y + 1]
	else:
		_p1 = _x, _y + 1, h_map[_x][_y + 1]
		_p2 = _x + 1, _y, h_map[_x + 1][_y]
		if x - _x < 1 - y + _y:
			_p3 = _x, _y, h_map[_x][_y]
		else:
			_p3 = _x + 1, _y + 1, h_map[_x + 1][_y + 1]

	vec1 = Vector3(*_p1)
	vec2 = Vector3(*_p2)
	vec3 = Vector3(*_p3)
	vec12 = vec2.minus_v(vec1)
	vec13 = vec3.minus_v(vec1)
	_n = vec12.x_v(vec13)

	_d = -_n.dot_v(vec1)
	return -(_n.x*x + _n.y*y + _d)/_n.z


def get_normal(x, y, h_map):
	_x = int(x)
	_y = int(y)
	if x == _x and y == _y:
		n1 = get_normal(x - 0.01, y - 0.01, h_map)
		n2 = get_normal(x + 0.01, y - 0.01, h_map)
		n3 = get_normal(x - 0.01, y + 0.01, h_map)
		n4 = get_normal(x + 0.01, y + 0.01, h_map)
		return (n1.plus_v(n2.plus_v(n3.plus_v(n4)))).x_r(1/4)
	elif x == _x:
		n1 = get_normal(x - 0.01, y, h_map)
		n2 = get_normal(x + 0.01, y, h_map)
		return (n1.plus_v(n2)).x_r(1/2)
	elif y == _y:
		n1 = get_normal(x, y - 0.01, h_map)
		n2 = get_normal(x, y + 0.01, h_map)
		return (n1.plus_v(n2)).x_r(1/2)
	
	if (_x + _y) % 2 == 0:
		_p1 = _x, _y, h_map[_x][_y]
		_p2 = _x + 1, _y + 1, h_map[_x + 1][_y + 1]
		if x - _x > y - _y:
			_p3 = _x + 1, _y, h_map[_x + 1][_y]
		else:
			_p3 = _x, _y + 1, h_map[_x][_y + 1]
	else:
		_p1 = _x, _y + 1, h_map[_x][_y + 1]
		_p2 = _x + 1, _y, h_map[_x + 1][_y]
		if x - _x < 1 - y + _y:
			_p3 = _x, _y, h_map[_x][_y]
		else:
			_p3 = _x + 1, _y + 1, h_map[_x + 1][_y + 1]

	vec1 = Vector3(*_p1)
	vec2 = Vector3(*_p2)
	vec3 = Vector3(*_p3)
	vec12 = vec2.minus_v(vec1)
	vec13 = vec3.minus_v(vec1)
	_n = vec12.x_v(vec13)

	return _n.norm()


def visible_q(vec1, vec2, h_map):
	_dv = vec2.minus_v(vec1)

	if abs(_dv.x) > abs(_dv.y):
		_sign = sign(_dv.x)
		_x, _y, _z = vec1.x, vec1.y, vec1.z
		for i in range(int(abs(_dv.x))):
			_x += _sign
			_y += _dv.y/_dv.x
			_z += _dv.z/_dv.x

			_h = get_height(_x, _y, h_map)

			if _h > _z:
				return False
	else:
		_sign = sign(_dv.y)
		_x, _y, _z = vec1.x, vec1.y, vec1.z
		for i in range(int(abs(_dv.y))):
			_y += _sign
			_x += _dv.x / _dv.y
			_z += _dv.z / _dv.y

			_h = get_height(_x, _y, h_map)

			if _h > _z:
				return False
	return True


