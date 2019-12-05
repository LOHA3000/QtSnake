import sys

from random import randint as r

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

        if not self.play:
            self.play = True
            self.start()
        self.generate_field()

    def generate_field(self):
        pass

    def generate_pineapple(self):
        del self.coordinates['pineapple']
        x, y = [r(0, self.n - 1), r(0, self.n - 1)]
        while [y, x] in self.coordinates.values():
            [x, y] = [r(0, self.n - 1), r(0, self.n - 1)]
        self.coordinates['pineapple'] = [y, x]

    def get_pineapple(self):
        self.snake_size += 1
        self.coordinates['tail'] = self.t
        self.coordinates[self.snake_size] = self.ps
        self.check_turns()
        if self.pt != list():
            self.turns[self.snake_size] = self.pt
            self.pt = []
        self.generate_pineapple()
        self.generate_field()

    def start(self):
        self.coordinates['head'] = [r(self.snake_size + 2, self.n - self.snake_size - 2),
                                    r(self.snake_size + 2, self.n - self.snake_size - 2)]
        k = r(0, 3)
        self.directions['head'] = [k, k]
        for i in range(1, self.snake_size + 1):
            self.directions[i] = self.directions['head']
        self.directions['tail'] = self.directions['head']
        x_tail = 0
        y_tail = 0
        if self.directions['head'][0] == 0:
            y_tail = 1
        elif self.directions['head'][0] == 1:
            x_tail = -1
        elif self.directions['head'][0] == 2:
            y_tail = -1
        elif self.directions['head'][0] == 3:
            x_tail = 1
        m = self.coordinates['head']
        self.coordinates['tail'] = [m[0] + (self.snake_size + 1) * y_tail, m[1] + (self.snake_size + 1) * x_tail]
        for i in range(1, self.snake_size + 1):
            self.coordinates[i] = [m[0] + i * y_tail, m[1] + i * x_tail]
        self.generate_pineapple()

    def move(self):
        x_head = 0
        y_head = 0
        if self.directions['head'][0] == 0:
            y_head = -1
        elif self.directions['head'][0] == 1:
            x_head = 1
        elif self.directions['head'][0] == 2:
            y_head = 1
        elif self.directions['head'][0] == 3:
            x_head = -1
        m = self.coordinates['head']
        new_head_coordinates = [m[0] + y_head, m[1] + x_head]
        self.coordinates['tail'] = self.coordinates[self.snake_size]
        for i in range(self.snake_size, 0, -1):
            if i == 1:
                self.coordinates[i] = self.coordinates['head']
            else:
                self.coordinates[i] = self.coordinates[i - 1]
        self.coordinates['head'] = new_head_coordinates
        for i in self.coordinates:
            if self.coordinates[i][0] == self.n:
                self.coordinates[i][0] = 0
            elif self.coordinates[i][0] == -1:
                self.coordinates[i][0] = self.n - 1
            elif self.coordinates[i][1] == self.n:
                self.coordinates[i][1] = 0
            elif self.coordinates[i][1] == -1:
                self.coordinates[i][1] = self.n - 1
        self.check_turns()
        self.check_directions()

    def check_turns(self):
        self.turns = {}
        for i in self.coordinates:
            if type(i) == int and self.snake_size > i > 1:
                if (self.coordinates[i - 1][0] != self.coordinates[i + 1][0]
                        and self.coordinates[i - 1][1] != self.coordinates[i + 1][1]):
                    self.turns[i] = self.coordinates[i]
            elif i == 1:
                if (self.coordinates['head'][0] != self.coordinates[i + 1][0]
                        and self.coordinates['head'][1] != self.coordinates[i + 1][1]):
                    self.turns[i] = self.coordinates[i]
            elif i == self.snake_size:
                if (self.coordinates[i - 1][0] != self.coordinates['tail'][0]
                        and self.coordinates[i - 1][1] != self.coordinates['tail'][1]):
                    self.turns[i] = self.coordinates[i]
            elif self.snake_size in self.turns:
                if self.coordinates['tail'] == self.turns[self.snake_size]:
                    self.pt = self.turns[self.snake_size]
        self.generate_field()

    def check_directions(self):
        for i in range(1, self.snake_size + 2):
            segment_direction = 0
            if type(i) == int and i < self.snake_size:
                if self.coordinates[i + 1][0] > self.coordinates[i][0]:
                    segment_direction = 0
                elif self.coordinates[i + 1][1] < self.coordinates[i][1]:
                    segment_direction = 1
                elif self.coordinates[i + 1][0] < self.coordinates[i][0]:
                    segment_direction = 2
                elif self.coordinates[i + 1][1] > self.coordinates[i][1]:
                    segment_direction = 3
                if i == 1:
                    self.directions[i] = [self.directions['head'][1], segment_direction]
                else:
                    self.directions[i] = [self.directions[i - 1][1], segment_direction]
            elif i == self.snake_size:
                if self.coordinates['tail'][0] > self.coordinates[i][0]:
                    segment_direction = 0
                elif self.coordinates['tail'][1] < self.coordinates[i][1]:
                    segment_direction = 1
                elif self.coordinates['tail'][0] < self.coordinates[i][0]:
                    segment_direction = 2
                elif self.coordinates['tail'][1] > self.coordinates[i][1]:
                    segment_direction = 3
                self.directions[i] = [self.directions[i - 1][1], segment_direction]
            elif i == self.snake_size + 1:
                self.directions['tail'] = [self.directions[self.snake_size][1], self.directions[self.snake_size][1]]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec_())
