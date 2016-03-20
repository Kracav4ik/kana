# encoding: utf-8

from __future__ import division

import sys

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene
from PyQt5 import uic


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('kana.ui', self)

        self.kana = QPixmap('data\\kana.png')

        self.scene = QGraphicsScene()
        self.scene.addPixmap(self.kana)
        self.graphicsView.setScene(self.scene)

if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
