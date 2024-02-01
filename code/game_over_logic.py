

import pygame
import os
from settings import  *
class Gameover:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.field = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.field.fill('#2F4F4F')
        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 50)
        self.score = 0

    def display_text(self, pos, text, f=None):
        if f:
            self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), f)
        text_surface = self.font.render(text, False, 'white')
        text_rect = text_surface.get_rect(center=pos)
        self.field.blit(text_surface, text_rect)
        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 50)
    def run(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_SPACE]:
            with open('../data/data.txt', 'a') as file:
                print(str(self.score) + '\n',file = file )

            return True
        self.screen.fill('#2F4F4F')
        self.display_text((GAME_WIDTH//2, 100), 'Game over!')
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT // 2 + 20), f"Your score: {self.score}", 25)
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT//2 + 170), f'Press space',25)
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT//2 + 210), f'to play again',25)
        self.screen.blit(self.field, (IDENT * 1.5, IDENT * 0.6))