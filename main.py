# encoding: utf-8

from __future__ import division

import sys
import random

from PyQt5.QtCore import QRectF, pyqtSlot
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem
from PyQt5 import uic


kana_map = (
    ('N', 'WA', 'RA', 'YA', 'MA', 'HA', 'NA', 'TA',  'SA',  'KA', 'A'),
    ('',  'WI', 'RI', '',   'MI', 'HI', 'NI', 'CHI', 'SHI', 'KI', 'I'),
    ('',  '',   'RU', 'YU', 'MU', 'FU', 'NU', 'TSU', 'SU',  'KU', 'U'),
    ('',  'WE', 'RE', '',   'ME', 'HE', 'NE', 'TE',  'SE',  'KE', 'E'),
    ('',  'WO', 'RO', 'YO', 'MO', 'HO', 'NO', 'TO',  'SO',  'KO', 'O'),
)


def get_kana(x, y):
    return kana_map[y][x]


def has_kana(x, y):
    return 0 <= y < len(kana_map) and 0 <= x < len(kana_map[y]) and get_kana(x, y)


def make_kana_list(level, allowed):
    return [(x, y) for x in range(level, 11) for y in allowed if has_kana(x, y)]


class MagicalKanaRect(QGraphicsRectItem):
    def __init__(self, pix):
        super().__init__(0, 0, kana_w, kana_h)
        self.tex_rect = QRectF(0, 0, kana_w, kana_h)
        self.kana = ''
        self.pix = pix

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(self.rect(), self.pix, self.tex_rect)

    def set_kana(self, x, y, is_kata):
        if not has_kana(x, y):
            return
        self.kana = get_kana(x, y)

        if is_kata:
            gap = kata_gap
            x0 = kata_x0
            y0 = kata_y0
        else:
            gap = hira_gap
            x0 = hira_x0
            y0 = hira_y0

        self.tex_rect = QRectF(x0 + x * kana_w, y0 + y * gap, kana_w, kana_h)
        self.update()

    def set_empty_kana(self):
        self.tex_rect = QRectF(0, 0, kana_w, kana_h)
        self.kana = ''
        self.update()

kana_w = 111
kana_h = 100

kata_gap = 140
kata_x0 = 78
kata_y0 = 318

hira_gap = 138
hira_x0 = 1222
hira_y0 = 1190


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('kana.ui', self)

        self.kana = QPixmap('data\\kana.png')

        self.scene = QGraphicsScene()

        self.kana_rect = MagicalKanaRect(self.kana)
        self.scene.addItem(self.kana_rect)
        self.graphicsView.setScene(self.scene)

        self.hiraCheck.clicked.connect(self.on_kana_check_clicked)
        self.kataCheck.clicked.connect(self.on_kana_check_clicked)
        self.lineEdit.returnPressed.connect(self.okButton.click)
        self.vowels = [self.useA, self.useI, self.useU, self.useE, self.useO]

        for checkbox in self.vowels + [self.hiraCheck, self.kataCheck]:
            checkbox.clicked.connect(self.on_nextButton_clicked)
        self.levelSlider.valueChanged.connect(self.on_nextButton_clicked)

        self.on_nextButton_clicked()

    @pyqtSlot()
    def on_kana_check_clicked(self):
        sender = self.sender()
        if not self.hiraCheck.isChecked() and not self.kataCheck.isChecked():
            other = self.hiraCheck if sender == self.kataCheck else self.kataCheck
            other.setChecked(True)

    @pyqtSlot()
    def on_nextButton_clicked(self):
        allowed_vowels = [number for number, checkbox in enumerate(self.vowels) if checkbox.isChecked()]
        if not allowed_vowels:
            self.kana_rect.set_empty_kana()
            return

        kana_list = make_kana_list(self.levelSlider.value(), allowed_vowels)
        x, y = random.choice(kana_list)

        kana_modes = []
        if self.hiraCheck.isChecked():
            kana_modes.append(False)
        if self.kataCheck.isChecked():
            kana_modes.append(True)

        self.kana_rect.set_kana(x, y, random.choice(kana_modes))

    @pyqtSlot()
    def on_okButton_clicked(self):
        text = self.lineEdit.text()
        self.lineEdit.setText('')
        if text.upper() == self.kana_rect.kana:
            self.on_nextButton_clicked()


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
