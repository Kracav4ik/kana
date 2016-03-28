# encoding: utf-8

from __future__ import division

import random
import sys

from PyQt5 import uic
from PyQt5.QtCore import QRectF, pyqtSlot, Qt, QPoint
from PyQt5.QtGui import QPixmap, QColor, QPainter, QPolygon, QBrush, QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsScene, QGraphicsRectItem, QHeaderView, QFileDialog, \
    QWidget

from two_sides import has_kana, get_kana, make_kana_list, HIRA, KATA, KANA_X_MAX


# noinspection PyAttributeOutsideInit
class MagicalKanaRect(QGraphicsRectItem):
    def __init__(self, pix):
        super().__init__(0, 0, kana_w, kana_h)
        self.__init()
        self.pix = pix

    def __init(self):
        self.tex_rect = QRectF(0, 0, kana_w, kana_h)
        self.kana = ''
        self.kana_x = 0
        self.kana_y = 1
        self.is_kata = True

    def paint(self, painter, option, widget=None):
        painter.drawPixmap(self.rect(), self.pix, self.tex_rect)

    def set_kana(self, x, y, is_kata):
        if not has_kana(x, y):
            return
        self.kana = get_kana(x, y)
        self.kana_x = x
        self.kana_y = y
        self.is_kata = is_kata

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
        self.__init()
        self.update()


kana_w = 111
kana_h = 100

kata_gap = 140
kata_x0 = 78
kata_y0 = 318

hira_gap = 138
hira_x0 = 1222
hira_y0 = 1190

VALUE = 224
BASE = 0.25


class RingStats:
    def __init__(self, limit):
        self.limit = limit
        self.ringbuffer = []

    def add_value(self, value):
        self.ringbuffer.append(value)
        if len(self.ringbuffer) > self.limit:
            self.ringbuffer = self.ringbuffer[-self.limit:]

    def __bool__(self):
        return bool(self.ringbuffer)

    def get_mean(self):
        assert self, 'No data in the ringbuffer'
        return sum(self.ringbuffer) / len(self.ringbuffer)


class StatsTable:
    def __init__(self):
        self.table = {}
        for x, y in make_kana_list():
            self.table[(x, y)] = RingStats(10)

    def put_data(self, x, y, data):
        stats = self.table.get((x, y))
        if stats is None:
            return
        stats.add_value(data)

    def get_color(self, x, y):
        stats = self.table.get((x, y))
        if not stats:
            return None
        hits = stats.get_mean()
        if hits != 1:
            hits *= 0.9
        green = VALUE * min(1, BASE + 2*(1 - BASE)*hits)
        red = VALUE * min(1, BASE + 2*(1 - BASE)*(1 - hits))
        return QColor(red, green, VALUE * BASE)


class StatsWidget(QWidget):
    def __init__(self, row, col, allowed_fun):
        super().__init__()
        self.allowed_fun = allowed_fun
        self.row = row
        self.col = col
        self.upper = QBrush(Qt.lightGray, Qt.Dense6Pattern)
        self.lower = QBrush(Qt.lightGray, Qt.Dense6Pattern)

    def set_couple(self, upper, lower):
        if upper is not None:
            self.upper = upper
        if lower is not None:
            self.lower = lower
        self.update()

    def paintEvent(self, event):
        if self.allowed_fun():
            p = QPainter(self)
            p.setPen(Qt.NoPen)
            w, h = self.width(), self.height()
            points = [QPoint(0, 0), QPoint(w, 0), QPoint(0, h), QPoint(w, h)]

            p.setBrush(self.upper)
            p.drawConvexPolygon(QPolygon(points[:3]))
            p.setBrush(self.lower)
            p.drawConvexPolygon(QPolygon(points[1:]))

            p.setPen(Qt.black)
            font = QFont('Arial', 8)
            p.setFont(font)
            p.drawText(2, 2 + h/2, get_kana(KANA_X_MAX - 1 - self.col, self.row, KATA))
            p.drawText(2 + w/2, h - 2, get_kana(KANA_X_MAX - 1 - self.col, self.row, HIRA))
        else:
            super().paintEvent(event)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        uic.loadUi('kana.ui', self)

        self.kana = QPixmap('data\\kana.jpg')

        self.scene = QGraphicsScene()

        self.kana_rect = MagicalKanaRect(self.kana)
        self.scene.addItem(self.kana_rect)
        self.graphicsView.setScene(self.scene)

        self.kanaTable.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.kanaTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        for row in range(self.kanaTable.rowCount()):
            for col in range(self.kanaTable.columnCount()):
                if not self.kanaTable.item(row, col):
                    cell_widget = StatsWidget(row, col, self.showStats.isChecked)
                    self.kanaTable.setCellWidget(row, col, cell_widget)
                    self.showStats.clicked.connect(cell_widget.update)
        self.hira_stats = StatsTable()
        self.kata_stats = StatsTable()

        self.hiraCheck.clicked.connect(self.on_kana_check_clicked)
        self.kataCheck.clicked.connect(self.on_kana_check_clicked)
        self.lineEdit.returnPressed.connect(self.okButton.click)
        self.vowels = [self.useA, self.useI, self.useU, self.useE, self.useO]

        for checkbox in self.vowels + [self.hiraCheck, self.kataCheck]:
            checkbox.clicked.connect(self.on_nextButton_clicked)
        self.levelSlider.valueChanged.connect(self.on_nextButton_clicked)

        self.clearButton.clicked.connect(self.tabletWidget.clear_canvas)

        for button in [self.hiraButton, self.kataButton]:
            button.clicked.connect(self.on_katahira_clicked)
        self.kana_letters = []

        self.on_nextButton_clicked()
        self.on_nextWordButton_clicked()

    def __set_kana_letters(self, letters):
        self.kana_letters = list(letters)
        text = ''
        kana = HIRA if self.hiraButton.isChecked() else KATA
        for x, y in self.kana_letters:
            text += get_kana(x, y, kana)
        self.kanaLabel.setText(text)

    def __update_color_at(self, x, y):
        upper_color, lower_color = [stats.get_color(x, y) for stats in (self.kata_stats, self.hira_stats)]
        x = self.kanaTable.columnCount() - 1 - x
        if x not in range(self.kanaTable.columnCount()) or y not in range(self.kanaTable.rowCount()):
            return
        cell = self.kanaTable.cellWidget(y, x)
        cell.set_couple(upper_color, lower_color)

    @pyqtSlot()
    def on_kana_check_clicked(self):
        sender = self.sender()
        if not self.hiraCheck.isChecked() and not self.kataCheck.isChecked():
            other = self.hiraCheck if sender == self.kataCheck else self.kataCheck
            other.setChecked(True)

    @pyqtSlot(bool)
    def on_katahira_clicked(self, checked):
        sender = self.sender()
        other = self.hiraButton if sender == self.kataButton else self.kataButton
        other.setChecked(not checked)
        self.__set_kana_letters(self.kana_letters)

    @pyqtSlot()
    def on_nextButton_clicked(self):
        allowed_vowels = [number for number, checkbox in enumerate(self.vowels) if checkbox.isChecked()]
        if not allowed_vowels:
            self.kana_rect.set_empty_kana()
            return

        kana_list = make_kana_list(self.levelSlider.value(), allowed_vowels)
        if len(kana_list) > 1:
            kana_list = [(x, y) for x, y in kana_list if get_kana(x, y) != self.kana_rect.kana]
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
        correct = text.upper() == self.kana_rect.kana
        x, y = self.kana_rect.kana_x, self.kana_rect.kana_y
        stats_table = self.kata_stats if self.kana_rect.is_kata else self.hira_stats
        stats_table.put_data(x, y, 1 if correct else 0)
        self.__update_color_at(x, y)
        if correct:
            self.on_nextButton_clicked()

    @pyqtSlot()
    def on_saveButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker
        save_path, _ = QFileDialog.getSaveFileName(self, 'Сохранение иероглифа', '', 'Кана (*.kana);;Все файлы (*)')
        if not save_path:
            return
        self.tabletWidget.save(save_path)

    @pyqtSlot()
    def on_loadButton_clicked(self):
        # noinspection PyCallByClass,PyTypeChecker
        load_path, _ = QFileDialog.getOpenFileName(self, 'Сохранение иероглифа', '', 'Кана (*.kana);;Все файлы (*)')
        if not load_path:
            return
        self.tabletWidget.load(load_path)

    @pyqtSlot()
    def on_nextWordButton_clicked(self):
        repeat_count = self.repeatCount.value()
        allowed_vowels = [number for number, checkbox in enumerate(self.vowels) if checkbox.isChecked()]
        if not allowed_vowels:
            self.kanaLabel.setText('')
            return

        kana_list = make_kana_list(self.levelSlider.value(), allowed_vowels)
        self.__set_kana_letters(random.choice(kana_list) for _ in range(repeat_count))


if __name__ == '__main__':
    app = QApplication(sys.argv)

    main_window = MainWindow()
    main_window.show()

    sys.exit(app.exec())
