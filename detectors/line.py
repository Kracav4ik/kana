# encoding: utf-8
from PyQt5.QtCore import Qt

from detectors import normalize, denormalize_vec
from detectors.bbox import AABB
from utils import Vec2d

from PyQt5.QtGui import QPainter


def _make_aabb(grid_size, cell_indices):
    return AABB(*[Vec2d(*[(i + d) / grid_size for i in cell_indices]) for d in range(2)])


class LineDetector:
    def __init__(self, grid_size, from_cell, to_cell):
        self.grid_size = grid_size
        self.from_bbox = _make_aabb(self.grid_size, from_cell)
        self.to_bbox = _make_aabb(self.grid_size, to_cell)

    def is_matched_line(self, curve, aabb):
        """
        :type curve: tablet.Curve
        :type aabb: detectors.bbox.AABB
        """
        curve = normalize(curve, aabb)
        return self.from_bbox.is_inside(curve.points[0][0]) and self.to_bbox.is_inside(curve.points[-1][0])

    def paint(self, painter, aabb):
        """
        :type painter: QPainter
        :type aabb: detectors.bbox.AABB
        """
        if not aabb:
            return
        painter.setPen(Qt.yellow)
        w = aabb.w / self.grid_size
        h = aabb.h / self.grid_size
        for bbox in [self.from_bbox, self.to_bbox]:
            bbl = denormalize_vec(bbox.bbl, aabb)
            painter.drawRect(bbl.x, bbl.y, w, h)

    def __str__(self):
        return 'LineDetector(%s -> %s)' % (self.from_bbox, self.to_bbox)
