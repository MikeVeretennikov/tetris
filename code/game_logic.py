import os.path
import random
import sys

import pygame
from timer_logic import Timer
from settings import *

class Game:
    def __init__(self, get_preview_shape, update_score):
        self.field = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.field.fill(pygame.Color('white'))
        self.screen = pygame.display.get_surface()
        self.get_preview_shape = get_preview_shape
        self.update_score = update_score
        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 50)
        self.timers = {'vertical_movement_timer': Timer(START_SPEED, True, self.move_down),
                       'horizontal_movement_timer': Timer(MOVE_WAIT_TIME),
                       'rotate_timer': Timer(ROTATE_WAIT_TIME)
                       }
        self.timers['vertical_movement_timer'].activate()
        self.now_level = 1
        self.now_score = 0
        self.now_lines = 0
        self.landing_music = pygame.mixer.Sound(os.path.join('..', 'music', 'landing.wav'))
        self.landing_music.set_volume(0.05)
        self.figures_sprites = pygame.sprite.Group()
        self.field_map = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
        self.figure = Figure(random.choice(list(FIGURES.keys())), self.figures_sprites, self.create_figure, self.field_map)
        self.speed = START_SPEED
        self.speed_fast = self.speed * 0.3
        self.speed_pressed = False
        self.gameover = False

    def end_the_game(self):
        for block in self.figure.blocks:
            if block.position.y < 0:
                self.gameover = True
                return
    def count_score(self, n):
        self.now_lines += n
        self.now_score += SCORE[n] * self.now_level
        if self.now_lines / 10 > self.now_level:
            self.speed = self.speed * 0.75
            self.speed_fast = self.speed * 0.3
            self.timers['vertical_movement_timer'].duration = self.speed
            self.now_level += 1

        self.update_score(self.now_score, self.now_lines, self.now_level)

    def update_timers(self):
        for timer in self.timers.values():
            timer.update()
    def move_down(self):
        self.figure.move_down()

    def display_text(self, pos, text):
        text_surface = self.font.render(text, False, 'white')
        text_rect = text_surface.get_rect(center = pos)
        self.screen.blit(text_surface, text_rect)

    def process_user_input(self):
        pressed = pygame.key.get_pressed()
        # горизонтальное движение
        if self.timers['horizontal_movement_timer'].active is False:
            if pressed[pygame.K_LEFT]:
                self.figure.move_horizontal(-1)
                self.timers['horizontal_movement_timer'].activate()
            if pressed[pygame.K_RIGHT]:
                self.figure.move_horizontal(1)
                self.timers['horizontal_movement_timer'].activate()
        # поворот
        if self.timers['rotate_timer'].active is False:
            if pressed[pygame.K_UP]:
                self.figure.rotate()
                self.timers['rotate_timer'].activate()
        if self.speed_pressed is False and pressed[pygame.K_DOWN]:
            self.timers['vertical_movement_timer'].duration = self.speed_fast
            self.speed_pressed = True
        if self.speed_pressed and not pressed[pygame.K_DOWN]:
            self.timers['vertical_movement_timer'].duration = self.speed
            self.speed_pressed = False
    def draw_field_lines(self):

        for row in range(1, ROWS):
            pygame.draw.line(
                self.field, '#2F4F4F',
                (0, row * CELL_SIZE), (self.field.get_width(), row * CELL_SIZE), 1
            )

        for col in range(1, COLUMNS):
            pygame.draw.line(
                self.field, '#2F4F4F',
                (col * CELL_SIZE, 0), (col * CELL_SIZE, self.field.get_height()), 1
            )


    def create_figure(self):
        self.end_the_game()
        self.clear_field()
        self.landing_music.play()
        self.figure = Figure(self.get_preview_shape(), self.figures_sprites, self.create_figure,
                             self.field_map)

    def clear_field(self):

        rows_to_delete = []
        for i in range(len(self.field_map)):
            if all(self.field_map[i]):
                rows_to_delete.append(i)
        if rows_to_delete:
            for delete_row in rows_to_delete:
                for block in self.field_map[delete_row]:
                    block.kill()

                for row in self.field_map:
                    for block in row:
                        if block and block.position.y < delete_row:
                            block.position.y += 1
            self.field_map = [[0 for i in range(COLUMNS)] for j in range(ROWS)]
            for sprite in self.figures_sprites:
                self.field_map[int(sprite.position.y)][int(sprite.position.x)] = sprite

            self.count_score(len(rows_to_delete))
    def run(self):
        if self.gameover:
            return (self.now_score, True)
        self.process_user_input()
        self.update_timers()
        self.figures_sprites.update()

        self.field.fill('white')
        self.figures_sprites.draw(self.field)
        self.draw_field_lines()
        self.display_text((WINDOW_WIDTH // 2, IDENT * 0.3), 'Tetris')
        self.screen.blit(self.field, (IDENT * 1.5, IDENT * 0.6))

class Block(pygame.sprite.Sprite):
    def __init__(self, sprite_group, position, color):
        super().__init__(sprite_group)
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(color)

        self.position = pygame.Vector2(position) + SPAWN_POINT
        self.rect = self.image.get_rect(
            topleft = (self.position.x * CELL_SIZE, self.position.y * CELL_SIZE)
        )



    def horizontal_collision(self, x, field_map):
        if not (x in range(0, COLUMNS)):
            return True

        if field_map[int(self.position.y)][x]:
            return True

    def rotate(self, center_dot):
        new_pos = center_dot + (self.position - center_dot).rotate(90)
        return new_pos
    def vertical_collision(self, y, field_map):
        if y >= ROWS:
            return True

        if y > 0 and field_map[y][int(self.position.x)]:
            return True

    def update(self):
        self.rect.topleft = self.position * CELL_SIZE


class Figure:
    def __init__(self, shape, group, create_figure, field_map):
        self.shape = shape
        self.block_positions = FIGURES[shape]['shape']
        self.color = FIGURES[shape]['color']
        self.field_map = field_map
        self.blocks = [Block(group, position, self.color) for position in self.block_positions]
        self.create_figure = create_figure
    def is_there_horizontal_collision(self, blocks, direction):
        next_move_figure = []
        for block in self.blocks:
            next_move_figure.append(block.horizontal_collision(int(block.position.x) + direction,self.field_map))

        if any(next_move_figure):
            return True
        else:
            return False

    def is_there_vertical_collision(self, blocks):
        next_move_figure = []
        for block in self.blocks:
            next_move_figure.append(block.vertical_collision(int(block.position.y) + 1,self.field_map))

        if any(next_move_figure):
            return True
        else:
            return False
    def move_horizontal(self, direction):
        if not self.is_there_horizontal_collision(self.blocks, direction):
            for block in self.blocks:
                block.position.x += direction

    def rotate(self):
        if self.shape == 'O':
            return

        center_dot = self.blocks[0].position
        rotated = [block.rotate(center_dot) for block in self.blocks]

        for position in rotated:
            if position.y > ROWS:
                return
            if not position.x in range(0, COLUMNS):
                return
            if self.field_map[int(position.y)][int(position.x)]:
                return


        for i in range(len(self.blocks)):
            self.blocks[i].position = rotated[i]
    def move_down(self):
        if not self.is_there_vertical_collision(self.blocks):
            for block in self.blocks:
                block.position.y += 1
        else:
            for block in self.blocks:
                self.field_map[int(block.position.y)][int(block.position.x)] = block

            self.create_figure()
