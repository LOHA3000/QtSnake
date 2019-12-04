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
        self.n = 10  # размер поля в клеточках
        self.pixels_side_size = 20  # размер клетки в пикселях
        self.snake_size = 2  # начальная длина змейки

        self.coordinates = {'head': [0, 0], 'tail': [0, 0], 'pineapple': [0, 0]}
        self.turns = {}
        self.directions = {'head': 0}

        self.t = []  # последнее положение хвоста
        self.ps = []  # последне положение сегмента перед хвостом
        self.pt = []  # коордтната последнего поворота

        self.play = False

        self.initUI()

    def initUI(self):
        k = self.pixels_side_size * self.n  # размер поля в пикселях

        self.setFixedSize(k, k)
        self.setWindowTitle('Змейка')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec_())
