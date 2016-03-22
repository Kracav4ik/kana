# encoding: utf-8
import time
import ast

from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget


class Curve:
    def __init__(self):
        self.start_time = 0
        self.points = []
        self.paint_path = QPainterPath()

    def add_point(self, pos, pressure):
        current_time = time.time()
        if not self.points:
            self.paint_path.moveTo(pos)
            self.start_time = current_time
        else:
            self.paint_path.lineTo(pos)
        self.points.append((pos, pressure, current_time - self.start_time))

    def paint_to(self, painter):
        painter.setPen(Qt.red)
        painter.drawPath(self.paint_path)
        painter.setPen(Qt.green)
        for pos, _p, _t in self.points:
            painter.drawPoint(pos)

    def to_string_row(self):
        if not self.points:
            return '[]'
        return '[(%s)]' % '), ('.join('%.4f,%.4f,%.4f' % (pos.x(), pos.y(), p) for pos, p, _ in self.points)

    def from_row(self, curve_row):
        self.points = []
        self.paint_path = QPainterPath()
        for pos_x, pos_y, pressure in curve_row:
            self.add_point(QPointF(pos_x, pos_y), pressure)

    def __bool__(self):
        return bool(self.points)


class TabletWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.current_curve = None
        ":type: PointsList"

        self.curves_list = []
        ":type: list[PointsList]"

        self.create_curve()

    def create_curve(self):
        self.current_curve = Curve()
        self.curves_list.append(self.current_curve)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setBrush(Qt.black)
        p.drawRect(self.rect())
        p.setBrush(Qt.NoBrush)
        for curve in self.curves_list:
            curve.paint_to(p)

    def clear_canvas(self):
        self.curves_list = []
        self.create_curve()
        self.update()

    def tabletEvent(self, event):
        pressure = event.pressure()
        print('Tablet!', event.x(), event.y(), pressure)
        self.current_curve.add_point(event.posF(), pressure)
        if pressure == 0:
            print('  finished with', len(self.current_curve.points), 'points')
            self.create_curve()

        event.accept()
        self.update()

    def save(self, path):
        with open(path, 'w') as f:
            f.write('[\n')
            for curve in self.curves_list:
                if not curve:
                    continue
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
