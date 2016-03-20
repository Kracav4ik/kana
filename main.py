# encoding: utf-8

from __future__ import division

import sys

from PyQt5.QtCore import QRectF, pyqtSlot
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

        kana_w = 111
        kana_h = 100

        kata_gap = 140
        kata_x = 78
        kata_y = 318

        hira_gap = 138
        hira_x = 1222
        hira_y = 1190

        for x in range(0, 11):
            for y in range(5):
                tex_x = kata_x + x * kana_w
                tex_y = kata_y + y * kata_gap
                self.scene.addItem(MagicalRectItem(self.kana, x * kana_w, y * kana_h, kana_w, kana_h, tex_x, tex_y))
                break
            break
        self.graphicsView.setScene(self.scene)

        self.hiraCheck.clicked.connect(self.on_kana_check_clicked)
        self.kataCheck.clicked.connect(self.on_kana_check_clicked)

    @pyqtSlot()
    def on_kana_check_clicked(self):
        sender = self.sender()
        if not self.hiraCheck.isChecked() and not self.kataCheck.isChecked():
            other = self.hiraCheck if sender == self.kataCheck else self.kataCheck
            other.setChecked(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
