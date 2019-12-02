from random import randint as r

from time import sleep as s


head = '■'
body = '*'
tail = '#'
turn = '@'

field = []
n = 20
snake_size = 5

coordinates = {'head': [0, 0], 'tail': [0, 0]}

head_direction = 0

play = False


def generate_field():
    global field
    global n
    global coordinates
    global head
    field = [['-' for i in range(n)] for i in range(n)]
    for i in coordinates:
        if i == 'head':
            field[coordinates[i][0]][coordinates[i][1]] = head
        elif i == 'tail':
            field[coordinates[i][0]][coordinates[i][1]] = tail
        elif type(i) == int:
            field[coordinates[i][0]][coordinates[i][1]] = body


def start():
    global head_direction
    global coordinates
    global snake_size
    coordinates['head'] = [r(snake_size + 2, n - snake_size - 2), r(snake_size + 2, n - snake_size - 2)]
    head_direction = r(0, 3)
    x_tail = 0
    y_tail = 0
    if head_direction == 0:
        y_tail = 1
    elif head_direction == 1:
        x_tail = -1
    elif head_direction == 2:
        y_tail = -1
    elif head_direction == 3:
        x_tail = 1
    m = coordinates['head']
    coordinates['tail'] = [m[0] + (snake_size + 1) * y_tail, m[1] + (snake_size + 1) * x_tail]
    for i in range(1, snake_size + 1):
        coordinates[i] = [m[0] + i * y_tail, m[1] + i * x_tail]
    generate_field()


def game():
    global play
    if not play:
        start()
        play = True
    while True:
        s(0.5)
        print('k')


game()
[print(i) for i in field]
