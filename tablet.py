# encoding: utf-8
import time

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPainterPath
from PyQt5.QtWidgets import QWidget


class PointsList:
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
        self.points.append((pos, pressure, current_time))

    def paint_to(self, painter):
        painter.setPen(Qt.red)
        painter.drawPath(self.paint_path)
        painter.setPen(Qt.green)
        for pos, _p, _t in self.points:
            painter.drawPoint(pos)


class TabletWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)

        self.current_list = None
        ":type: PointsList"

        self.points_lists = []
        ":type: list[PointsList]"

        self.create_new_list()

    def create_new_list(self):
        self.current_list = PointsList()
        self.points_lists.append(self.current_list)

    def paintEvent(self, event):
        p = QPainter(self)
        p.setBrush(Qt.black)
        p.drawRect(self.rect())
        p.setBrush(Qt.NoBrush)
        for points_list in self.points_lists:
            points_list.paint_to(p)

    def clear_canvas(self):
        self.points_lists = []
        self.create_new_list()
        self.update()

    def tabletEvent(self, event):
        pressure = event.pressure()
        print('Tablet!', event.x(), event.y(), pressure)
        self.current_list.add_point(event.posF(), pressure)
        if pressure == 0:
            print('  finished with', len(self.current_list.points), 'points')
            self.create_new_list()

        event.accept()
        self.update()
