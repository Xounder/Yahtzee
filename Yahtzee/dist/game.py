import pygame, sys
from settings import *
from control import Control
from start_window import StartWindow

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption('Yahtzee')
        self.clock = pygame.time.Clock()
        bg_surf = pygame.image.load('img/bg.png').convert()
        self.bg_surf = pygame.transform.scale(bg_surf, (screen_width, screen_height))

        self.control_game = Control()
        self.start_window = StartWindow(self.control_game.active_game)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
            self.screen.blit(self.bg_surf, (0, 0))

            if self.control_game.run_game:
                self.control_game.draw()
                self.control_game.update()
            else:
                self.start_window.draw()
                self.start_window.update()

            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()