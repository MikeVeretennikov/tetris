import pygame.display
import  os
from settings import *

class Preview:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.field = pygame.Surface((GAME_WIDTH // 2 - 20, IDENT + 20))
        self.rect = self.field.get_rect(topleft=(IDENT * 1.5 - 20, (IDENT * 0.5) + (IDENT * 0.5) + GAME_HEIGHT))
        self.field.fill('#2F4F4F')
        self.shape_surfaces = {shape: pygame.image.load(os.path.join('..', 'visual', f'{shape}.png')).convert_alpha() for shape in
                               FIGURES.keys()}

        self.font = pygame.font.Font(os.path.join('..', 'visual', 'Tetris.ttf'), 30)


    def run(self,next_shape):
        shape_surface = self.shape_surfaces[next_shape]
        x = self.field.get_width() / 2
        y = self.field.get_height() / 2
        rect = shape_surface.get_rect(center=(x,y))
        self.field.fill('#2F4F4F')

        self.field.blit(shape_surface, rect)
        self.screen.blit(self.field, self.rect)