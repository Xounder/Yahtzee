import pygame
from dices_table import DicesTable
from scoreboard import Scoreboard
from timer import Timer
from settings import screen_height, screen_width
from support import blit_text_shadow

class Control:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.run_game = False
        self.winner = 0
        self.win = False
        self.atual_player = 0

        self.dices_table = DicesTable()
        # scoreboard
        scoreboard_surf = pygame.image.load('img/scoreboard.png').convert()
        self.scoreboard_surf = pygame.transform.scale(scoreboard_surf, (scoreboard_surf.get_width(), screen_height))
        self.scoreboard_rect = self.scoreboard_surf.get_rect(topleft= (250, 0))
        # win window
        win_surf = pygame.image.load('img/win.png').convert()
        self.win_surf = pygame.transform.scale(win_surf, (win_surf.get_width()*2, win_surf.get_height()*2))
        self.win_rect = self.win_surf.get_rect(center= (screen_width/2, screen_height/2))
        # timer
        self.win_timer = Timer(2)
        # font
        self.font_win = pygame.font.Font('font/Pixeltype.ttf', 40)
        self.ply_win_surf = None
        self.ply_win_rect = None
        
    def active_game(self, num_players):
        self.create_players(num_players)
        self.run_game = True
        self.win = False
        self.winner = 0
        self.atual_player = 0

    def create_players(self, num_players):
        self.scoreboard = [Scoreboard((i + 1), (354 + i*40)) for i in range(num_players)]

    def draw(self):
        self.display_surface.blit(self.scoreboard_surf, self.scoreboard_rect)
        self.dices_table.draw()
        for ply_scoreboard in self.scoreboard:
            ply_scoreboard.draw()
        if self.win:
            if self.win_timer.run:
                self.display_surface.blit(self.win_surf, self.win_rect)
                blit_text_shadow(f'{self.winner+1}', 'red', (screen_width/2, screen_height/2), self.font_win, back_color='black')
            else:
                self.run_game = False    

    def update(self):
        if not self.win:
            self.dices_table.update()
            if self.scoreboard[self.atual_player].update(self.dices_table.dices_value, self.dices_table.try_roll):
                self.dices_table.reset_try_roll()
                if self.atual_player < len(self.scoreboard)-1:  
                    self.atual_player += 1
                else:
                    self.check_win()
                    self.atual_player = 0
        else:
            if self.win_timer.run:
                self.win_timer.update()

    def check_win(self):
        if self.scoreboard[self.atual_player].total_score != 0:
            m_score = 0
            for i, ply_scoreboard in enumerate(self.scoreboard):
                if ply_scoreboard.total_score > m_score:
                    m_score = ply_scoreboard.total_score
                    self.winner = i
                    self.win = True
            self.win_timer.active()
