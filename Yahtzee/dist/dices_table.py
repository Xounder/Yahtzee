import pygame
from dice import Dice
from settings import *
from timer import Timer
from support import blit_text_shadow

class DicesTable:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.dices = [Dice(dices_pos[i]) for i in range(5)]
        self.dices_value = [dice.choosed for dice in self.dices]
        self.try_roll = 3
        # roll button
        roll_surf = pygame.image.load('img/roll.png').convert()
        self.roll_surf = pygame.transform.scale(roll_surf, (160, 30))
        self.roll_rect = self.roll_surf.get_rect(topleft= (50, screen_height - 100))
        # mouse
        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center = (0, 0))
        self.mouse_timer = Timer(0.9)
        # font
        self.font_txt = pygame.font.Font('font/Pixeltype.ttf', 35)

    def reset_try_roll(self):
        self.try_roll = 3
        for dice in self.dices:
            dice.reset_dice()

    def draw(self):
        self.display_surface.blit(self.roll_surf, self.roll_rect)
        pos = [self.roll_rect[0] + 150, self.roll_rect[1] + 18]
        color = 'white' if self.try_roll > 0 else 'red'
        blit_text_shadow(f'{self.try_roll}', color, pos, self.font_txt, back_color='black')
        for dice in self.dices:
            dice.draw()
    
    def update(self):
        self.input()
        if self.mouse_timer.run:
            self.mouse_timer.update()
        for i, dice in enumerate(self.dices):
            dice.update(self.try_roll)
            self.dices_value[i] = dice.choosed
            
    def roll_dices(self):
        for dice in self.dices:
            dice.roll_dice()

    def can_roll(self):
        for dice in self.dices:
            if not dice.store_dice:
                return True
        return False

    def input(self):
        if not self.mouse_timer.run:
            if self.try_roll > 0:
                if pygame.mouse.get_pressed()[0]:
                    self.mouse_rect.center = pygame.mouse.get_pos()
                    if self.mouse_rect.colliderect(self.roll_rect) and self.can_roll():
                        self.roll_dices()
                        self.try_roll -= 1
                        self.mouse_timer.active()
