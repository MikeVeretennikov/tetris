from pygame import Color, Vector2

# фигуры
FIGURES = {
    'Z': {'shape': [(0, 0), (1, 0), (0, -1), (-1, -1)], 'color': Color('#e51b20')},
    'S': {'shape': [(0, 0), (-1, 0), (0, -1), (1, -1)], 'color': Color('#65b32e')},
    'I': {'shape': [(0, 0), (0, -1), (0, -2), (0, 1)], 'color': Color('#6cc6d9')},
    'O': {'shape': [(0, 0), (0, -1), (1, 0), (1, -1)], 'color': Color('#f1e60d')},
    'T': {'shape': [(0, 0), (-1, 0), (1, 0), (0, -1)], 'color': Color('#7b217f')},
    'J': {'shape': [(0, 0), (0, -1), (0, 1), (-1, 1)], 'color': Color('#204b9b')},
    'L': {'shape': [(0, 0), (0, -1), (0, 1), (1, 1)], 'color': Color('#f07e13')},
}

# подсчет очков
# ключ - количество заполненных линий
# значение - количество полученных очков
SCORE = {
    1: 40,
    2: 100,
    3: 300,
    4: 1200
}

# размеры поля
ROWS = 20
COLUMNS = 10
CELL_SIZE = 30
GAME_WIDTH = COLUMNS * CELL_SIZE
GAME_HEIGHT = ROWS * CELL_SIZE



# константы для поведения игры
ROTATE_WAIT_TIME = 200
MOVE_WAIT_TIME = 200
START_SPEED = 300
SPAWN_POINT = Vector2(COLUMNS // 2, -1)

# размеры полей с информацией
INFO_FIELD_WIDTH = 200
NEXT_FIGURE_FIELD_FRACTION = INFO_FIELD_WIDTH * 0.5
SCORE_FIELD_FRACTION = INFO_FIELD_WIDTH - NEXT_FIGURE_FIELD_FRACTION

# размеры окна
IDENT = 100
WINDOW_HEIGHT = (IDENT * 2.5) + GAME_HEIGHT
WINDOW_WIDTH =  (IDENT * 3)  + GAME_WIDTH


