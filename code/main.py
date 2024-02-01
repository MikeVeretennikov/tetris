import random
import os
import pygame
from settings import *
import sys
from game_logic import Game
from score_logic import Score
from preview_logic import Preview
from game_over_logic import Gameover
from start_window_logic import Startwindow
class Main:
    def __init__(self):

        pygame.init()
        pygame.display.set_caption('TETRIS')
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.preview = Preview()
        self.game = Game(self.get_preview_shape, self.update_score)
        self.score = Score()
        self.start_window = Startwindow()
        self.gameover_window = Gameover()
        self.gameover_state = False
        self.start_window_state = True
        self.preview_shape = random.choice(list(FIGURES.keys()))
        self.itog_score = 0
        self.music = pygame.mixer.Sound(os.path.join('..', 'music', 'music.wav'))
        self.music.set_volume(0.01)




    def update_score(self, score, lines, level):
        self.score.score = score
        self.score.lines = lines
        self.score.level = level

    def get_preview_shape(self):
        x = self.preview_shape
        self.preview_shape = random.choice(list(FIGURES.keys()))
        return x
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            self.screen.fill('#2F4F4F')


            # start window
            if self.start_window_state:
                if self.start_window.run():
                    self.music.play(-1)
                    self.start_window_state = False

            else:

                # gameover logic

                res = self.game.run()

                if res:
                    self.itog_score = res[0]
                    self.gameover_state = True

                if self.gameover_state:
                    self.music.stop()
                    self.gameover_window.score = self.itog_score

                    res2 = self.gameover_window.run()
                    if res2:
                        self.gameover_state = False
                        self.__init__()

                # game
                else:

                    self.preview.run(self.preview_shape)
                    self.score.run()

            pygame.display.update()
            self.clock.tick()

        pygame.quit()

if __name__ == '__main__':
    main = Main()
    main.run()