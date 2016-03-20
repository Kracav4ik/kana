# encoding: utf-8

from __future__ import division

import sys

from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem
from PyQt5 import uic


class MagicalRectItem(QGraphicsRectItem):
    def __init__(self, pix, x, y, w, h, tex_x, tex_y):
        super().__init__(x, y, w, h)
        self.tex_rect = QRectF(tex_x, tex_y, w, h)
        self.pix = pix

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(self.rect(), self.pix, self.tex_rect)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('kana.ui', self)

        self.kana = QPixmap('data\\kana.png')

        self.scene = QGraphicsScene()
        self.rectitem = MagicalRectItem(self.kana, 0, 0, 111, 100, 411, 318)
        self.scene.addItem(self.rectitem)
        self.graphicsView.setScene(self.scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
