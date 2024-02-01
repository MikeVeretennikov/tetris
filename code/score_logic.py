import pygame.display
import os
import pygame
from settings import *

class Score:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.field = pygame.Surface((GAME_WIDTH // 2 + 40, IDENT + 20))
        self.rect = self.field.get_rect(topleft=(IDENT * 1.5 + GAME_WIDTH // 2 + 20, (IDENT * 0.5) + (IDENT * 0.5) + GAME_HEIGHT))
        self.field.fill('#2F4F4F')
        self.lines = 0
        self.score = 0
        self.level = 1
        self.increment = self.field.get_height() / 3
        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 30)

    def display_text(self, pos, text):
        text_surface = self.font.render(f'{text[0]}: {text[1]}', False, 'white')
        text_rect = text_surface.get_rect(center=pos)
        self.field.blit(text_surface, text_rect)

    def run(self):
        self.field.fill('#2F4F4F')
        for i, text in enumerate([('Score', self.score), ('Level', self.level), ('Lines', self.lines)]):
            self.display_text((self.field.get_width() / 2-15, self.increment / 2 + i * self.increment), text)
        self.screen.blit(self.field, self.rect)