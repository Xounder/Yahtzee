import pygame
from settings import screen_height, screen_width
from timer import Timer
from support import blit_text_shadow

class StartWindow:
    def __init__(self, active_game):
        self.display_surface = pygame.display.get_surface()
        self.active_game = active_game
        self.qnt_ply = 1
        # image
        start_surf = pygame.image.load('img/start_window.png').convert()
        self.start_surf = pygame.transform.scale(start_surf, (start_surf.get_width(), screen_height))
        self.start_rect = self.start_surf.get_rect(center= (screen_width/2, screen_height/2))
        # colisions
        self.plus_surf = pygame.Surface((25, 25))
        self.plus_rect = self.plus_surf.get_rect(center= (screen_width/2 + 90, screen_height - 107))
        self.minus_surf = pygame.Surface((25, 25))
        self.minus_rect = self.plus_surf.get_rect(center= (screen_width/2 - 105, screen_height - 107))
        self.start_button = pygame.Surface((115, 45))
        self.start_button_rect = self.start_button.get_rect(center = (screen_width/2 - 7, screen_height - 35))
        # mouse
        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center= (0, 0))
        self.mouse_timer = Timer(0.5)
        #font
        self.font_txt = pygame.font.Font('font/Pixeltype.ttf', 40)
        
    def draw(self):
        self.display_surface.blit(self.start_surf, self.start_rect)
        pygame.draw.rect(self.display_surface, 'red', [self.start_button_rect[0], self.start_button_rect[1], 115, 45], 3)
        blit_text_shadow(f'{self.qnt_ply}', 'red', (screen_width/2 - 5, screen_height - 105), self.font_txt, back_color='black')

    def update(self):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        self.input()

    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0]:
                self.mouse_rect.center = pygame.mouse.get_pos()
                if self.mouse_rect.colliderect(self.start_button_rect):
                    self.active_game(self.qnt_ply)
                elif self.mouse_rect.colliderect(self.minus_rect):
                    self.qnt_ply -= 1 if self.qnt_ply > 0 else 0
                elif self.mouse_rect.colliderect(self.plus_rect):
                    self.qnt_ply += 1 if self.qnt_ply < 10 else 0
                self.mouse_timer.active()
