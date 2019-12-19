import sys
from random import randint as r
from tkinter import Tk, messagebox, Spinbox, Button

from PIL import Image
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPainter, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QPushButton


class Game(QWidget):
    def __init__(self):
        super().__init__()

        self.field_size = 8

        self.n = 8  # размер поля в клеточках
        self.pixels_side_size = 20  # размер клетки в пикселях
        self.snake_size = 2  # начальная длина змейки

        self.coordinates = {'head': [0, 0], 'tail': [0, 0], 'pineapple': [0, 0]}
        self.turns = {}
        self.directions = {'head': 0}

        self.t = []  # последнее положение хвоста
        self.ps = []  # последне положение сегмента перед хвостом
        self.pt = []  # коордтната последнего поворота

        self.play = False

        self.is_playing = True

        self.body_labels = []
        for i in range(self.snake_size):
            self.generate_bodies()

        self.head = QLabel(self)
        self.head.resize(self.pixels_side_size, self.pixels_side_size)
        self.tail = QLabel(self)
        self.tail.resize(self.pixels_side_size, self.pixels_side_size)
        self.pineapple = QLabel(self)
        self.pineapple.resize(self.pixels_side_size, self.pixels_side_size)

        # скорость змейки
        self.snake_speed = 170
        # цикл игры
        self.timer = QTimer()
        self.timer.timeout.connect(self.move)
        self.timer.start(self.snake_speed)

        self.initUI()

    def initUI(self):
        k = self.pixels_side_size * self.n  # размер поля в пикселях

        self.setFixedSize(k, k + 20)
        self.setWindowTitle('Змейка')

        if not self.play:
            self.play = True
            self.start()
        self.generate_field()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.draw_field(qp, self.n, self.pixels_side_size)
        qp.end()

    def draw_field(self, qp, n, p):
        qp.setBrush(QColor(34, 177, 76))
        qp.drawRect(-1, -1, p * n + 1, p * n + 1)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Up:
            if self.directions['head'] == [1, 1] or self.directions['head'] == [3, 3]:
                self.directions['head'] = [0, 0]
        elif event.key() == Qt.Key_Right:
            if self.directions['head'] == [0, 0] or self.directions['head'] == [2, 2]:
                self.directions['head'] = [1, 1]
        elif event.key() == Qt.Key_Down:
            if self.directions['head'] == [1, 1] or self.directions['head'] == [3, 3]:
                self.directions['head'] = [2, 2]
        elif event.key() == Qt.Key_Left:
            if self.directions['head'] == [0, 0] or self.directions['head'] == [2, 2]:
                self.directions['head'] = [3, 3]
        elif event.key() == Qt.Key_P:
            self.timer.stop()
        elif event.key() == Qt.Key_C:
            if self.play:
                self.timer.start(self.snake_speed)
            else:
                p = Tk()
                messagebox.showerror('Вы проиграли', 'начните новую игру, нажав R')
                p.destroy()
        elif event.key() == Qt.Key_R:
            # print('restart')
            self.restart()
        elif event.key() == Qt.Key_S:
            # print('settings')
            self.timer.stop()
            self.p = Tk()
            self.p.title('Размер поля')
            self.p.geometry('300x100+100+100')
            self.p.resizable(False, False)
            self.txt = Spinbox(self.p, from_=8, to=40, textvariable=self.field_size)
            self.txt.place(x=0, y=0, relwidth=1, relheight=1 / 2)
            button_save = Button(self.p, text='Save', command=self.save_settings,
                                 font=('Cooper Black', 20))
            button_save.place(x=0, y=51, relwidth=1, relheight=1 / 2)
            self.p.mainloop()

    def save_settings(self):
            self.field_size = int(self.txt.get())
            k = self.pixels_side_size * self.field_size  # размер поля в пикселях

            self.setFixedSize(k, k)
            self.p.destroy()
            self.restart()

    def check_game(self):
        if len(set([str(i[0]) + ',' + str(i[1]) for i in list(self.coordinates.values())])) < self.snake_size + 3:
            self.timer.stop()
            self.is_playing = False
        else:
            self.is_playing = True

    def generate_field(self):
        self.check_game()
        if self.is_playing:
            self.check_directions()
            self.check_turns()
            for i in self.coordinates:
                if i == 'pineapple':
                    self.generate_image('p', self.coordinates[i])
                elif i == 'head':
                    self.generate_image('h', self.coordinates[i])
                elif i == 'tail':
                    self.generate_image('t', self.coordinates[i])
                elif type(i) == int:
                    self.generate_image('b', self.coordinates[i], i - 1)

    def generate_image(self, object, coords, i=0):
        if object == 'p':
            pixmap = QPixmap('snake_segments/pineapple.png')
            self.pineapple.move(self.pixels_side_size * coords[1],
                                self.pixels_side_size * coords[0])
            self.pineapple.setPixmap(pixmap)
        elif object == 'h':
            im = Image.open('snake_segments/head.png')
            if self.directions['head'][0] == 3:
                im = im.rotate(90, expand=1)
                im.save('snake_segments/res/res_head.png')
            elif self.directions['head'][0] == 2:
                im = im.rotate(180, expand=1)
                im.save('snake_segments/res/res_head.png')
            elif self.directions['head'][0] == 1:
                im = im.rotate(270, expand=1)
                im.save('snake_segments/res/res_head.png')
            if self.directions['head'][0] != 0:
                pixmap = QPixmap('snake_segments/res/res_head.png')
            else:
                pixmap = QPixmap('snake_segments/head.png')
            self.head.setPixmap(pixmap)
            self.head.move(self.pixels_side_size * coords[1],
                           self.pixels_side_size * coords[0])
        elif object == 't':
            im = Image.open('snake_segments/tail.png')
            if self.directions['tail'][0] == 3:
                im = im.rotate(90, expand=1)
                im.save('snake_segments/res/res_tail.png')
            elif self.directions['tail'][0] == 2:
                im = im.rotate(180, expand=1)
                im.save('snake_segments/res/res_tail.png')
            elif self.directions['tail'][0] == 1:
                im = im.rotate(270, expand=1)
                im.save('snake_segments/res/res_tail.png')
            if self.directions['tail'][0] != 0:
                pixmap = QPixmap('snake_segments/res/res_tail.png')
            else:
                pixmap = QPixmap('snake_segments/tail.png')
            self.tail.setPixmap(pixmap)
            self.tail.move(self.pixels_side_size * coords[1],
                           self.pixels_side_size * coords[0])
        elif object == 'b':
            try:
                im = Image.open('snake_segments/res/res_body.png')
                im .save('snake_segments/res/res_body.png')
            except:
                im = Image.open('snake_segments/body.png')
                im = im.rotate(90, expand=1)
                im.save('snake_segments/res/res_body.png')
            if self.directions[i + 1] == [0, 0] or self.directions[i + 1] == [2, 2]:
                pixmap = QPixmap('snake_segments/body.png')
            elif self.directions[i + 1][0] != self.directions[i + 1][1]:
                if self.directions[i + 1] == [0, 3] or self.directions[i + 1] == [1, 2]:
                    pixmap = QPixmap('snake_segments/turn.png')
                else:
                    im = Image.open('snake_segments/turn.png')
                    if self.directions[i + 1] == [3, 2] or self.directions[i + 1] == [0, 1]:
                        im = im.rotate(90, expand=1)
                    elif self.directions[i + 1] == [3, 0] or self.directions[i + 1] == [2, 1]:
                        im = im.rotate(180, expand=1)
                    elif self.directions[i + 1] == [1, 0] or self.directions[i + 1] == [2, 3]:
                        im = im.rotate(270, expand=1)
                    im.save('snake_segments/res/res_turn.png')
                    pixmap = QPixmap('snake_segments/res/res_turn.png')
            else:
                pixmap = QPixmap('snake_segments/res/res_body.png')
            self.body_labels[i].move(self.pixels_side_size * coords[1],
                                     self.pixels_side_size * coords[0])
            self.body_labels[i].setPixmap(pixmap)
            self.body_labels[i].show()
    
    def generate_bodies(self):
        p = QLabel(self)
        p.resize(self.pixels_side_size, self.pixels_side_size)
        self.body_labels.append(p)

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
        if self.pt != []:
            self.turns[self.snake_size] = self.pt
            self.pt = []
        self.generate_bodies()
        self.generate_pineapple()
        try:
            self.generate_field()
            # print('field ready')
        except:
            # print('Error')
            # print(self.snake_size)
            # print(self.coordinates)
            # print(self.directions)
            # print(self.turns)
            # print(self.body_labels)
            self.restart()
        self.setWindowTitle(str(self.snake_size))

    def start(self):
        # print(type(self.n))
        # print([i for i in range(self.snake_size + 2, self.n - self.snake_size - 2 + 1)])
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

    def restart(self):
        self.n = self.field_size

        self.snake_size = 2

        self.setWindowTitle(self.snake_size)

        self.coordinates = {'head': [0, 0], 'tail': [0, 0], 'pineapple': [0, 0]}
        self.turns = {}
        self.directions = {'head': 0}

        self.t = []
        self.ps = []
        self.pt = []

        self.play = False
        for i in self.body_labels:
            i.hide()
        self.body_labels = []
        for i in range(self.snake_size):
            self.generate_bodies()

        self.timer.start(self.snake_speed)

        if not self.play:
            self.play = True
            self.start()
        self.generate_field()

    def move(self):
        self.t = self.coordinates['tail']
        self.ps = self.coordinates[self.snake_size]
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
        if self.coordinates['head'] == self.coordinates['pineapple']:
            self.get_pineapple()
        self.check_turns()
        self.check_directions()
        k = []
        for i in self.coordinates.values():
            if i not in k:
                k.append(i)
        # print(k, self.coordinates.keys(), self.snake_size)
        if len(k) == self.snake_size + 3:
            self.generate_field()
        else:
            self.timer.stop()
            print('snake died')
            self.play = False

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
                    if abs(segment_direction - self.directions['head'][1]) == 2:
                        segment_direction = self.directions[i + 1][1]
                    self.directions[i] = [self.directions['head'][1], segment_direction]
                else:
                    if abs(segment_direction - self.directions[i - 1][1]) == 2:
                        segment_direction = self.directions[i + 1][1]
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
                if abs(segment_direction - self.directions[i - 1][1]) == 2:
                    segment_direction = self.directions['tail'][1]
                self.directions[i] = [self.directions[i - 1][1], segment_direction]
            elif i == self.snake_size + 1:
                self.directions['tail'] = [self.directions[self.snake_size][1], self.directions[self.snake_size][1]]


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec_())
