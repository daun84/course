import pygame
from pygame.locals import *
import os
from typing import List

from views.menus.Menu import Menu


class MainMenu(Menu):
    def __init__(self, window: pygame.surface.Surface):
        super().__init__(["NEW GAME", "LOAD GAME", "QUIT"], window)
        self.headline_font = pygame.font.Font("resources/fonts/RetroGaming.ttf", 48)
        headline_text: str = "KOSMOSA OKKUPANTI VERSION 1.01"
        self.headline = self.headline_font.render(headline_text, True, (255, 255, 255))


    def draw_menu(self):
        super().draw_menu()
        headline_x = self.win.get_width() // 2 - self.headline.get_width() // 2
        headline_y = self.win.get_height() // 2 - self.headline.get_height() // 2 - 200
        self.win.blit(self.headline, (headline_x, headline_y))