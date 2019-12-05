# змейка
import sys

from random import randint as random_choice_from

from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap

import time

from PIL import Image

from tkinter import Tk
from tkinter import messagebox as mb


''' начало игры '''

class Game(QWidget):
    def __init__(self):
        self.c = 0
        
        super().__init__()

        ''''''
        # размер змейки
        self.snake_size = 4
        # количество сегментов с одной стороны
        self.field_side_size = 20
        # возможные положения головы вначале
        self.head_directions = ['up', 'right', 'down', 'left']
        # начальное направление головы
        self.direction = random_choice_from(0, 3)
        print(self.head_directions[self.direction])
        # координата головы, отдалена от краёв на 4 клетки
        k = self.field_side_size - 4
        self.head_position = [random_choice_from(3, k), random_choice_from(3, k)]
        # игровое поле
        self.game_field = [['-' for i in range(self.field_side_size)] for i in range(self.field_side_size)]
        # размер сегментов в пикелях
        self.n = 20
        # символ головы змейки в коде
        self.symbol = '■'
        # появление змейки на поле
        self.game_field[self.head_position[0]][self.head_position[1]] = self.symbol
        ''''''
        self.initUI()
        ''''''
        # скорость змейки
        self.snake_speed = 500
        # цикл игры
        self.timer = QTimer()
        self.timer.timeout.connect(self.play)
        self.timer.start(self.snake_speed)
        ''''''
        # голова змейки
        self.image = QLabel(self)
        self.image.resize(self.n, self.n)
        

    def initUI(self):
        # размер поля в пикселях
        k = self.field_side_size * self.n
        
        self.setFixedSize(k, k)
        self.setWindowTitle('Змейка')

    def generate_image(self, name, direction):
        ''''''
        # поворот в нужную сторону
        im = Image.open(name)
        if direction == 1:
            im = im.rotate(270, expand=1)
        elif direction == 2:
            im = im.rotate(180, expand=1)
        elif direction == 3:
            im = im.rotate(90, expand=1)
        im.save(name)
        # ''' изображение на поле ''' #
        self.pixmap = QPixmap(name) 
        self.image.setPixmap(self.pixmap)
        # поворот обратно
        im = Image.open(name)
        if direction == 1:
            im = im.rotate(90, expand=1)
        elif direction == 2:
            im = im.rotate(180, expand=1)
        elif direction == 3:
            im = im.rotate(270, expand=1)
        im.save(name)
        ''''''
        
    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_field(qp, self.n)
        qp.end()

    def draw_field(self, qp, n):
        for i in range(self.field_side_size):
            for o in range(self.field_side_size):
                qp.setBrush(QColor(34, 177, 76))
                qp.drawRect(0, 0, self.field_side_size * n, self.field_side_size * n)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            self.direction = 0
            print('вверх')
        elif event.key() == Qt.Key_Right:
            self.direction = 1
            print('вправо')
        elif event.key() == Qt.Key_Down:
            self.direction = 2
            print('вниз')
        elif event.key() == Qt.Key_Left:
            self.direction = 3
            print('влево')
        elif event.key() == Qt.Key_P:
            self.timer.stop()
        elif event.key() == Qt.Key_S:
            self.timer.start(self.snake_speed)
        self.c = 0
        # print(self.direction)

    def play(self):
        # print(self.direction)
        if self.direction == 0:
            self.head_position[0] -= 1
            if self.head_position[0] < 0:
                self.head_position[0] = self.field_side_size - 1       
                self.c += 1
        elif self.direction == 2:
            self.head_position[0] += 1
            if self.head_position[0] > self.field_side_size - 1:
                self.head_position[0] = 0
                self.c += 1
        elif self.direction == 1:
            self.head_position[1] += 1
            if self.head_position[1] > self.field_side_size - 1:
                self.head_position[1] = 0
                self.c += 1
        elif self.direction == 3:
            self.head_position[1] -= 1
            if self.head_position[1] < 0:
                self.head_position[1] = self.field_side_size - 1
                self.c += 1
        self.game_field = [['-' for i in range(self.field_side_size)] for i in range(self.field_side_size)]
        self.game_field[self.head_position[0]][self.head_position[1]] = self.symbol
        # [print(i) for i in self.game_field]
        # print()
        self.generate_image('head.png', self.direction)
        self.image.move(self.n * self.head_position[1], self.n * self.head_position[0])
        if self.c == 3:
            p = Tk()
            answer = mb.askyesno(title="Вопрос", message="Продолжить игру?")
            self.timer.stop()
            if answer == True:
                self.timer.start(self.snake_speed)
                self.c = 0
            else:
                self.close()
                з.destroy()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec_())

