import pygame
from settings import *
from timer import Timer
from support import blit_text

class Scoreboard:
    def __init__(self, num_ply, posx_score=354):
        self.display_surface = pygame.display.get_surface()
        self.num_ply = num_ply
        self.bonus = 0
        self.total_score = 0
        self.sum_points = 0
        self.last_value = 3
        self.next_player = False
        self.bonus_acquire = False
        self.posx_score = posx_score
        # player score
        player_section_surf = pygame.image.load('img/player_section.png').convert()
        self.player_section_surf = pygame.transform.scale(player_section_surf, (player_section_surf.get_width(), screen_height))
        self.player_section_rect = self.player_section_surf.get_rect(topleft= (posx_score, 0))
        self.possible_pts = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        # upper section
        self.upper_pts = [-1, -1, -1, -1, -1, -1]
        self.upper_section_surf = [pygame.Surface((10, 10)) for i in range(6)]
        self.upper_section_rect = [self.upper_section_surf[i].get_rect(center= (posx_score + 20,  screen_height / 10.5 + (screen_height / 15.5 * i - (screen_height/160 * i)))) for i in range(6)]
        # lower section
        self.lower_pts = [-1, -1, -1, -1,-1, -1, -1]
        self.lower_section_surf = [pygame.Surface((10, 10)) for i in range(7)]
        self.lower_section_rect = [self.lower_section_surf[i].get_rect(center= (posx_score + 20,  screen_height / 10.5 + (screen_height / 15.5 * (i + 8) - (screen_height/160 * (i + 8))))) for i in range(7)]
        # mouse
        self.mouse_surf = pygame.Surface((5, 5))
        self.mouse_rect = self.mouse_surf.get_rect(center = (0, 0))
        self.mouse_timer = Timer(0.6)
        # font
        self.font_txt = pygame.font.Font('font/Pixeltype.ttf', 25)

    def draw(self):
        self.display_surface.blit(self.player_section_surf, self.player_section_rect)
        blit_text(f'P{self.num_ply}', 'black', [self.posx_score + 20, 20], self.font_txt)
        for i in range(6):
            if self.last_value < 3:
                if self.upper_pts[i] == -1:
                    blit_text(f'{self.possible_pts[0][i]}', 'red', (self.upper_section_rect[i][0] + 5, self.upper_section_rect[i][1] + 5), self.font_txt)
            if self.upper_pts[i] != -1:
                blit_text(f'{self.upper_pts[i]}', 'black', (self.upper_section_rect[i][0] + 5, self.upper_section_rect[i][1] + 5), self.font_txt)
        for i in range(7):
            if self.last_value < 3:
                if self.lower_pts[i] == -1:
                    blit_text(f'{self.possible_pts[1][i]}', 'red', (self.lower_section_rect[i][0] + 5, self.lower_section_rect[i][1] + 5), self.font_txt)
            if self.lower_pts[i] != -1:
                blit_text(f'{self.lower_pts[i]}', 'black', (self.lower_section_rect[i][0] + 5, self.lower_section_rect[i][1] + 5), self.font_txt)
        # bonus // sum // total_score
        for i in range(2):
            tam_upper = [self.posx_score + 20,  screen_height / 10.5 + (screen_height / 15.5 * (6+i) - (screen_height/160 * (6+i)))]
            if i == 0:
                if self.upper_pts.count(-1) == 0:
                    blit_text(f'{self.sum_points}', 'black', (tam_upper), self.font_txt)
            else:
                if self.bonus_acquire:
                    blit_text(f'{self.bonus}', 'black', (tam_upper), self.font_txt)
        if self.upper_pts.count(-1) == 0 and self.lower_pts.count(-1) == 0:
            tam_lower = [self.posx_score + 20,  screen_height / 10.5 + (screen_height / 15.5 * 15 - (screen_height/160 * 15))]
            blit_text(f'{self.total_score}', 'black', (tam_lower), self.font_txt)
    
    def update(self, dices_value, try_roll):
        if self.mouse_timer.run:
            self.mouse_timer.update()
        if try_roll != self.last_value:
            self.update_possible_pts(dices_value)
            self.last_value = try_roll
        self.input()
        if self.next_player:
            self.next_player = False
            self.last_value = 3
            return True
        
    def input(self):
        if not self.mouse_timer.run:
            if pygame.mouse.get_pressed()[0] and self.last_value < 3:
                self.mouse_rect.center = pygame.mouse.get_pos()
                for i, upper_score in enumerate(self.upper_section_rect):
                    if self.mouse_rect.colliderect(upper_score):
                        if self.upper_pts[i] == -1:
                            self.upper_pts[i] = self.possible_pts[0][i]
                            if self.upper_pts.count(-1) == 0:
                                self.sum_points = sum(self.upper_pts)
                                if self.sum_points >= 63:
                                    self.bonus = 35
                                    self.bonus_acquire = True
                            self.next_player = True
                            break
                for i, lower_score in enumerate(self.lower_section_rect):
                    if self.mouse_rect.colliderect(lower_score):
                        if self.lower_pts[i] == -1:
                            self.lower_pts[i] = self.possible_pts[1][i]
                            self.next_player = True
                            break
                if self.upper_pts.count(-1) == 0 and self.lower_pts.count(-1) == 0:
                    self.total_score = self.sum_points + sum(self.lower_pts) + self.bonus
                self.mouse_timer.active()
    
    def update_possible_pts(self, dices_value):
        org_dices = dices_value[:]
        org_dices.sort()
        eliminated_dices = []
        count_dices = []
        self.possible_pts = [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]]
        #eliminar os iguais
        for num in org_dices:
            if eliminated_dices:
                if num != eliminated_dices[len(eliminated_dices)-1]:
                   eliminated_dices.append(num)
            else:
                eliminated_dices.append(num)
        #juntar em outra lista para averiguar
        for num in eliminated_dices:
            count_dices.append(org_dices.count(num)) 
        
        for i, dice_value in enumerate(eliminated_dices):
            if dice_value == 1:
                self.possible_pts[0][0] = count_dices[i]
            elif dice_value == 2:
                self.possible_pts[0][1] = count_dices[i] * 2
            elif dice_value == 3:
                self.possible_pts[0][2] = count_dices[i] * 3
            elif dice_value == 4:
                self.possible_pts[0][3] = count_dices[i] * 4
            elif dice_value == 5:
                self.possible_pts[0][4] = count_dices[i] * 5
            elif dice_value == 6:
                self.possible_pts[0][5] = count_dices[i] * 6
            if count_dices[i] >= 3: # tree of a kind
                self.possible_pts[1][0] = sum(dices_value)
            if count_dices[i] >= 4: # four of a kind
                self.possible_pts[1][1] = sum(dices_value)

        self.possible_pts[1][5] = sum(dices_value) # chance
        if len(eliminated_dices) == 2 and (count_dices[0] == 2 or count_dices[0] == 3): # full house
            self.possible_pts[1][2] = 25
        elif len(count_dices) == 1: # yathzee
                self.possible_pts[1][6] = 50
        elif len(eliminated_dices) == 4:
            if eliminated_dices == [1, 2, 3, 4] or eliminated_dices == [2, 3, 4, 5] or eliminated_dices == [3, 4, 5, 6]: # small straight
                self.possible_pts[1][3] = 30
        elif len(eliminated_dices) == 5:
            if eliminated_dices == [1, 2, 3, 4, 5] or eliminated_dices == [2, 3, 4, 5, 6]: # large straight
                self.possible_pts[1][4] = 40
            dice_check = [eliminated_dices[:4], eliminated_dices[1:5]]
            for i, dcheck in enumerate(dice_check):
                if dcheck == [1, 2, 3, 4] or dcheck == [2, 3, 4, 5] or dcheck == [3, 4, 5, 6]: # small straight
                    self.possible_pts[1][3] = 30
