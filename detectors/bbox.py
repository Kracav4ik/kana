# encoding: utf-8
from utils import min_coords, max_coords


class AABB:
    def __init__(self, *points):
        self.bbl = self.fur = None
        for point in points:
            self.extend(point)

    def extend(self, v):
        if not self:
            self.bbl = self.fur = v
        else:
            self.bbl = min_coords(self.bbl, v)
            self.fur = max_coords(self.fur, v)

    def is_inside(self, v):
        if not self:
            return False
        return self.bbl.x <= v.x <= self.fur.x and self.bbl.y <= v.y <= self.fur.y

    @property
    def x(self):
        return self.bbl.x

    @property
    def y(self):
        return self.bbl.y

    @property
    def w(self):
        return self.fur.x - self.bbl.x

    @property
    def h(self):
        return self.fur.y - self.bbl.y

    def __bool__(self):
        return self.bbl is not None

    def __str__(self):
        return '[%s %s]' % (self.bbl, self.fur)
