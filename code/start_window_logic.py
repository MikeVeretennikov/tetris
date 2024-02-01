import pygame
import os
from settings import *
class Startwindow:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.field = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
        self.field.fill('#2F4F4F')
        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 50)
        f = open('../data/data.txt', 'r')
        data = []
        for i in f:
            i = i.strip()
            if i:
                data.append(int(i))
        f.close()
        if data:
            self.best_score = max(data)
        else:
            self.best_score = 0


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
            return True
        self.screen.fill('#2F4F4F')
        self.display_text((GAME_WIDTH//2, 100), 'Tetris')
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT // 2 + 20), f"Best score: {self.best_score}", 25)
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT//2 + 170), f'Press space',25)
        self.display_text((GAME_WIDTH // 2, GAME_HEIGHT//2 + 210), f'to start',25)
        self.screen.blit(self.field, (IDENT * 1.5, IDENT * 0.6))
