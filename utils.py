# encoding: utf-8
import numbers

import math


class Vec2d:
    """Двумерный вектор"""

    def __init__(self, x=0, y=0):
        self.data = (x, y)

    @property
    def x(self):
        return self.data[0]

    @property
    def y(self):
        return self.data[1]

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        return not (self == other)

    def __pos__(self):
        return self

    def __neg__(self):
        return Vec2d(-self.x, -self.y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return self + (-other)

    def __mul__(self, other):
        assert isinstance(other, numbers.Real), '%r must be a number' % other
        return Vec2d(self.x*other, self.y*other)

    def __rmul__(self, other):
        return self * other

    def __truediv__(self, other):
        return self * (1/other)

    def __abs__(self):
        return Vec2d(abs(self.x), abs(self.y))

    def len2(self):
        return self.x**2 + self.y**2

    def len(self):
        return math.sqrt(self.len2())

    def norm(self):
        if self.x == 0 and self.y == 0:
            return self
        return self / self.len()

    def __str__(self):
        return '(%s, %s)' % self.data

    def __repr__(self):
        return 'Vec2d(%s, %s)' % self.data

    @staticmethod
    def from_qt(qt_point):
        return Vec2d(qt_point.x(), qt_point.y())


def dot(v1, v2):
    """Скалярное произведение
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return v1.x * v2.x + v1.y * v2.y


def cross(v1, v2):
    """Векторное произведение
    :type v1: Vec2d
    :type v2: Vec2d
    """
    return v1.x * v2.y - v1.y * v2.x
