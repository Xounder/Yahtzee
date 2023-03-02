import pygame
from random import randint
from settings import screen_height, screen_width
from timer import Timer 

class Dice:
    def __init__(self, dice_pos):
        self.display_surface = pygame.display.get_surface()
        self.choosed = randint(1, 6)
        self.store_dice = False
        self.roll = True
        # image
        self.dices_surf = [pygame.image.load(f'img/dice/dice{i+1}.png').convert_alpha() for i in range(6)]
        self.frame_choosed = self.dices_surf[self.choosed-1]
        self.dice_rect = self.frame_choosed.get_rect(center = (dice_pos))
        self.atual_frame = 0

        self.mouse_surf = pygame.Surface((5, 5))
        # timer
        self.dice_animate_timer = Timer(0.5)
        self.mouse_timer = Timer(0.6)
        
    def draw(self):
        self.display_surface.blit(self.frame_choosed, self.dice_rect)
        if self.store_dice:
            pygame.draw.rect(self.display_surface,'red', (self.dice_rect[0], self.dice_rect[1], self.dices_surf[0].get_width(), self.dices_surf[1].get_height()), 3)

    def animate(self):
        self.atual_frame += 0.15
        if self.atual_frame > len(self.dices_surf)-1:
            self.atual_frame = 0
        self.frame_choosed = self.dices_surf[int(self.atual_frame)]

    def input(self):
        if not self.mouse_timer.run:
            self.mouse_rect = self.mouse_surf.get_rect(center= (pygame.mouse.get_pos()))
            if pygame.mouse.get_pressed()[0] == True and self.dice_rect.colliderect(self.mouse_rect):    
                self.store_dice = not self.store_dice
                self.mouse_timer.active()
        
    def roll_dice(self):
        if not self.store_dice:
            self.dice_animate_timer.active()
            self.roll = True
            self.choosed = randint(1, 6)  
             
    def reset_dice(self):
        self.store_dice = False

    def update(self, try_roll):
        if self.mouse_timer.run:
            self.mouse_timer.update()

        if self.dice_animate_timer.run:
                self.animate()
                self.dice_animate_timer.update()
        else:
            if 0 < try_roll < 3:
                self.input()
            else:
                self.store_dice = False
            if self.roll:
                self.frame_choosed = self.dices_surf[self.choosed-1]
                self.roll = False
