from random import randint as r


head = '■'
body = '*'
tail = '#'
turn = '@'
pineapple = '$'

field = []
n = 10  # начальная длина змейки
snake_size = 2

coordinates = {'head': [0, 0], 'tail': [0, 0], 'pineapple': [0, 0]}
turns = {}
directions = {'head': 0}

t = []  # последнее положение хвоста
ps = []  # последне положение сегмента перед хвостом
pt = []  # коордтната последнего поворота

play = False


def generate_field():
    global field
    global n
    global coordinates
    global head
    global turns
    field = [['-' for i in range(n)] for i in range(n)]
    for i in coordinates:
        if i == 'head':
            field[coordinates[i][0]][coordinates[i][1]] = head
        elif i == 'tail':
            field[coordinates[i][0]][coordinates[i][1]] = tail
        elif i == 'pineapple':
            field[coordinates[i][0]][coordinates[i][1]] = pineapple
        elif type(i) == int:
            if i not in turns:
                field[coordinates[i][0]][coordinates[i][1]] = body
            else:
                field[coordinates[i][0]][coordinates[i][1]] = turn


def generate_pineapple():
    global coordinates
    del coordinates['pineapple']
    x, y = [r(0, n - 1), r(0, n - 1)]
    while [y, x] in coordinates.values():
        [x, y] = [r(0, n - 1), r(0, n - 1)]
    coordinates['pineapple'] = [y, x]


def get_pineapple():
    global snake_size
    global coordinates
    global t
    global ps
    global pt
    snake_size += 1
    coordinates['tail'] = t
    coordinates[snake_size] = ps
    check_turns()
    print(pt)
    if pt != list():
        turns[snake_size] = pt
        pt = []
    generate_pineapple()
    generate_field()


def start():
    global directions
    global coordinates
    global snake_size
    coordinates['head'] = [r(snake_size + 2, n - snake_size - 2), r(snake_size + 2, n - snake_size - 2)]
    k = r(0, 3)
    directions['head'] = [k, k]
    for i in range(1, snake_size + 1):
        directions[i] = directions['head']
    directions['tail'] = directions['head']
    x_tail = 0
    y_tail = 0
    if directions['head'][0] == 0:
        y_tail = 1
    elif directions['head'][0] == 1:
        x_tail = -1
    elif directions['head'][0] == 2:
        y_tail = -1
    elif directions['head'][0] == 3:
        x_tail = 1
    m = coordinates['head']
    coordinates['tail'] = [m[0] + (snake_size + 1) * y_tail, m[1] + (snake_size + 1) * x_tail]
    for i in range(1, snake_size + 1):
        coordinates[i] = [m[0] + i * y_tail, m[1] + i * x_tail]
    generate_pineapple()


def move():
    global directions
    global coordinates
    global snake_size
    global n
    global t
    global ps
    t = coordinates['tail']
    ps = coordinates[snake_size]
    x_head = 0
    y_head = 0
    if directions['head'][0] == 0:
        y_head = -1
    elif directions['head'][0] == 1:
        x_head = 1
    elif directions['head'][0] == 2:
        y_head = 1
    elif directions['head'][0] == 3:
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
    check_turns()
    check_directions()


def check_turns():
    global turns
    global coordinates
    global snake_size
    global pt
    turns = {}
    for i in coordinates:
        if type(i) == int and snake_size > i > 1:
            if (coordinates[i - 1][0] != coordinates[i + 1][0]
                    and coordinates[i - 1][1] != coordinates[i + 1][1]):
                turns[i] = coordinates[i]
        elif i == 1:
            if (coordinates['head'][0] != coordinates[i + 1][0]
                    and coordinates['head'][1] != coordinates[i + 1][1]):
                turns[i] = coordinates[i]
        elif i == snake_size:
            if (coordinates[i - 1][0] != coordinates['tail'][0]
                    and coordinates[i - 1][1] != coordinates['tail'][1]):
                turns[i] = coordinates[i]
        elif snake_size in turns:
            if coordinates['tail'] == turns[snake_size]:
                pt = turns[snake_size]
                print(pt)
    generate_field()


def check_directions():
    global coordinates
    global directions
    global snake_size
    print(coordinates)
    for i in range(1, snake_size + 2):
        segment_direction = 0
        if type(i) == int and i < snake_size:
            if coordinates[i + 1][0] > coordinates[i][0]:
                segment_direction = 0
            elif coordinates[i + 1][1] < coordinates[i][1]:
                segment_direction = 1
            elif coordinates[i + 1][0] < coordinates[i][0]:
                segment_direction = 2
            elif coordinates[i + 1][1] > coordinates[i][1]:
                segment_direction = 3
            if i == 1:
                directions[i] = [directions['head'][1], segment_direction]
            else:
                directions[i] = [directions[i - 1][1], segment_direction]
        elif i == snake_size:
            if coordinates['tail'][0] > coordinates[i][0]:
                segment_direction = 0
            elif coordinates['tail'][1] < coordinates[i][1]:
                segment_direction = 1
            elif coordinates['tail'][0] < coordinates[i][0]:
                segment_direction = 2
            elif coordinates['tail'][1] > coordinates[i][1]:
                segment_direction = 3
            directions[i] = [directions[i - 1][1], segment_direction]
        elif i == snake_size + 1:
            directions['tail'] = [directions[snake_size][1], directions[snake_size][1]]
    print(directions)


def game():
    global play
    global directions
    global coordinates
    if not play:
        play = True
        start()
    generate_field()
    [print(i) for i in field]
    while True:
        command = input('u - up, r - right, d - down, l - left, p - pass, s - stop\n')
        if command == 'p':
            move()
        elif command == 's':
            break
        if command in ['u', 'r', 'd', 'l']:
            lr = False  # возможность поворота влево и вправо
            ud = False  # возможность поворота вверх и вниз
            if directions['head'][0] == 0:
                lr = True
            elif directions['head'][0] == 1:
                ud = True
            elif directions['head'][0] == 2:
                lr = True
            elif directions['head'][0] == 3:
                ud = True
            if command == 'u' and ud:
                directions['head'] = [0, 0]
                move()
            elif command == 'd' and ud:
                directions['head'] = [2, 2]
                move()
            elif command == 'r' and lr:
                directions['head'] = [1, 1]
                move()
            elif command == 'l' and lr:
                directions['head'] = [3, 3]
                move()
            else:
                print('Error')
        if coordinates['head'] == coordinates['pineapple']:
            get_pineapple()
        [print(i) for i in field]


game()
