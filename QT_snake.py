import sys

from random import randint as random_choice_from

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap

import time

from PIL import Image


class Game(QWidget):
    def __init__(self):
        super().__init__()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec_())
