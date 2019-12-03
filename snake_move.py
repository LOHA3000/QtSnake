from random import randint as r

from time import sleep as s


head = '■'
body = '*'
tail = '#'
turn = '@'
pineapple = '$'

field = []
n = 10
snake_size = 2

coordinates = {'head': [0, 0], 'tail': [0, 0], 'pineapple': [0, 0]}

head_direction = 0
t = []  # последнее положение хвоста
ps = []  # последне положение сегмента перед хвостом

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
        elif i == 'pineapple':
            field[coordinates[i][0]][coordinates[i][1]] = pineapple
        elif type(i) == int:
            field[coordinates[i][0]][coordinates[i][1]] = body


def generate_pineapple():
    global coordinates
    coordinates['pineapple'] = [r(0, n - 1), r(0, n - 1)]

def get_pineapple():
    global snake_size
    global coordinates
    global t
    global ps
    snake_size += 1
    coordinates['tail'] = t
    coordinates[snake_size] = ps
    generate_pineapple()
    generate_field()


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
    generate_pineapple()


def move():
    global head_direction
    global coordinates
    global snake_size
    global n
    global t
    global ps
    t = coordinates['tail']
    ps = coordinates[snake_size]
    x_head = 0
    y_head = 0
    if head_direction == 0:
        y_head = -1
    elif head_direction == 1:
        x_head = 1
    elif head_direction == 2:
        y_head = 1
    elif head_direction == 3:
        x_head = -1
    m = coordinates['head']
    new_head_coordinates = [m[0] + y_head, m[1] + x_head]
    coordinates['tail'] = coordinates[snake_size]
    for i in range(snake_size, 0, -1):
        if i == 1:
            coordinates[i] = coordinates['head']
        else:
            coordinates[i] = coordinates[i - 1]
    coordinates['head'] = new_head_coordinates
    for i in coordinates:
        if coordinates[i][0] == n:
            coordinates[i][0] = 0
        elif coordinates[i][0] == -1:
            coordinates[i][0] = n - 1
        elif coordinates[i][1] == n:
            coordinates[i][1] = 0
        elif coordinates[i][1] == -1:
            coordinates[i][1] = n - 1
    generate_field()


def game():
    global play
    global head_direction
    global coordinates
    if not play:
        play == True
        start()
    generate_field()
    [print(i) for i in field]
    while True:
        command = input('u - up, r - right, d - down, l - left, p - pass, s - stop\n')
        if command == 'p':
            move()
        elif command == 's':
            break
        elif command == 'u':
            head_direction = 0
            move()
        elif command == 'r':
            head_direction = 1
            move()
        elif command == 'd':
            head_direction = 2
            move()
        elif command == 'l':
            head_direction = 3
            move()
        if coordinates['head'] == coordinates['pineapple']:
            get_pineapple()
        [print(i) for i in field]


game()