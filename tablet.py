# encoding: utf-8
import ast

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget

from detectors.bbox import AABB
from detectors.line import LineDetector
from utils import Vec2d


KATA_I = [
    LineDetector(3, Vec2d(2, 0), Vec2d(0, 1)),
    LineDetector(3, Vec2d(1, 1), Vec2d(1, 2)),
]


class Curve:
    def __init__(self):
        self.points = []

    def add_point(self, pos, pressure):
        self.points.append((pos, pressure))

    def paint_to(self, painter):
        if len(self.points) > 1:
            painter.setPen(Qt.red)
            paint_path = QPainterPath()
            paint_path.moveTo(*self.points[0][0])
            for pos, _ in self.points[1:]:
                paint_path.lineTo(*pos)
            painter.drawPath(paint_path)

        painter.setPen(Qt.green)
        for pos, _ in self.points:
            painter.drawPoint(*pos)

    def to_string_row(self):
        if not self.points:
            return '[]'
        return '[(%s)]' % '), ('.join('%.4f,%.4f,%.4f' % (pos.x, pos.y, p) for pos, p in self.points)

    def from_row(self, curve_row):
        self.points = []
        for pos_x, pos_y, pressure in curve_row:
            self.add_point(Vec2d(pos_x, pos_y), pressure)

    def __bool__(self):
        return bool(self.points)


class TabletWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.current_curve = None
        ":type: PointsList"

        self.curves_list = []
        ":type: list[PointsList]"

        self.detectors = KATA_I
        ":type: list[LineDetector]"

        self.aabb = AABB(Vec2d(130, 1), Vec2d(330, 200))
        self.create_curve()

    def create_curve(self):
        self.current_curve = Curve()
        self.curves_list.append(self.current_curve)

    def paintEvent(self, event):
        p = QPainter(self)

        p.setBrush(Qt.black)
        p.drawRect(self.rect())
        p.setBrush(Qt.NoBrush)

        if self.aabb:
            p.setPen(Qt.blue)
            p.drawRect(self.aabb.x, self.aabb.y, self.aabb.w, self.aabb.h)

        curves = self.get_curves()
        if len(self.detectors) > len(curves):
            detector = self.detectors[len(curves)]
            detector.paint(p, self.aabb)

        for curve in curves:
            curve.paint_to(p)

    def clear_canvas(self):
        self.curves_list = []
        self.aabb = AABB()
        self.create_curve()
        self.update()

    def get_curves(self):
        return [curve for curve in self.curves_list if curve]

    def tabletEvent(self, event):
        pressure = event.pressure()
        pos = Vec2d.from_qt(event.posF())
        print('Tablet!', pos, pressure)
        self.current_curve.add_point(pos, pressure)
        self.aabb.extend(pos)
        if pressure == 0:
            print('  finished with', len(self.current_curve.points), 'points')
            if len(self.detectors) == len(self.curves_list):
                for curve, detector in zip(self.curves_list, self.detectors):
                    print('detector %s: match %s' % (detector, detector.is_matched_line(curve, self.aabb)))
            self.create_curve()

        event.accept()
        self.update()

    def save(self, path):
        with open(path, 'w') as f:
            f.write('[\n')
            for curve in self.get_curves():
                f.write('    %s,\n' % curve.to_string_row())
            f.write(']\n')

    def load(self, path):
        new_curves = []
        with open(path) as f:
            data = ast.literal_eval(f.read())
            for curve_row in data:
                curve = Curve()
                curve.from_row(curve_row)
                new_curves.append(curve)
            self.curves_list = new_curves
            self.create_curve()
            self.update()
