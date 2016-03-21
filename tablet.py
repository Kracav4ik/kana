# encoding: utf-8
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


class TabletWidget(QWidget):
    def __init__(self, *args):
        super().__init__(*args)
        print('tablet!')

    def paintEvent(self, event):
        # Makes stylesheets work for custom children of QWidget
        # (see http://www.qtcentre.org/threads/37976-Q_OBJECT-and-CSS-background-image)
        # Yes, this is what kind of shit we have to deal with
        o = QStyleOption()
        o.initFrom(self)
        p = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, o, p, self)

    def tabletEvent(self, event):
        print('Tablet!', event.posF(), event.pressure())
        event.accept()
