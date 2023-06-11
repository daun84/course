import pygame
from pygame.locals import *
import os
from singleton import SingletonMeta
from controller import Controller
from typing import List
from model import GameData
from constants import MAP_WIDTH, MAP_HEIGHT, EnumPlayerTurns

class Menu:
    def __init__(self, menu_options: List[str], window: pygame.surface.Surface):
        self.options: List[str] = menu_options
        self.font = pygame.font.Font(None, 32)
        self.selected_option = 0
        self.win = window
        self.fps = 60

    def draw_menu(self) -> None:
        for i, option in enumerate(self.options):
            if i == self.selected_option:
                text = self.font.render(option, True, (255, 0, 0)) 
            else:
                text = self.font.render(option, True, (255, 255, 255)) 
            rect = text.get_rect(center=(self.win.get_width() // 2, self.win.get_height() // 2 + i * 40))
            self.win.blit(text, rect)

    def run(self) -> str:
        clock = pygame.time.Clock()

        running = True
        while running:
            clock.tick(self.fps)

            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == K_RETURN:
                        return self.options[self.selected_option]

            self.win.fill((0, 0, 0))
            self.draw_menu()
            pygame.display.flip()

class MainMenu(Menu):
    def __init__(self, window):
        super().__init__(["NEW GAME", "LOAD GAME", "QUIT"], window)
        self.headline_font = pygame.font.Font(None, 64)
        headline_text: str = "KOSMOSA OKKUPANTI VERSION 1.01"
        self.headline = self.headline_font.render(headline_text, True, (255, 255, 255))


    def draw_menu(self):
        super().draw_menu()
        headline_x = self.win.get_width() // 2 - self.headline.get_width() // 2
        headline_y = self.win.get_height() // 2 - self.headline.get_height() // 2 - 200
        self.win.blit(self.headline, (headline_x, headline_y))

class LoadMenu(Menu):
    def __init__(self, window):
        options: List[str] = []
        if not os.listdir("../saves"):
            options.append("THERE'S NOTHING TO LOAD")
        else:
            options = os.listdir("../saves")
        options.sort()
        super().__init__(options, window)

    def draw_menu(self):
        start_index = self.selected_option // 25 * 25
        end_index = min(len(self.options), start_index + 25)
        for i, option in enumerate(self.options[start_index : end_index]):
            if start_index + i == self.selected_option:
                text = self.font.render(option, True, (0, 255, 0))  
            else:
                text = self.font.render(option, True, (255, 255, 255))  
            rect = text.get_rect()
            rect.center = (self.win.get_width() // 2, 20 + i * 40)
            self.win.blit(text, rect)

class View(metaclass=SingletonMeta):
    def __init__(self, controller):
        pygame.init()
        pygame.font.init()
        self.__controller: Controller = controller
        self.__fps: int = 60
        self.__win = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("Space invaders")
        self.__save_cooldown: int = 0

    def main(self):
        running = True
        main_menu = MainMenu(self.__win)
        load_menu = LoadMenu(self.__win)
        while running:
            option: str = main_menu.run()
            if option == "QUIT":
                pygame.quit()
                running = False
            elif option == "NEW GAME":
                self.game_loop("../resources/starting_position.pickle")
            elif option == "LOAD GAME":
                self.game_loop(load_menu.run())

    def handle_input(self) -> List[EnumPlayerTurns]:
        keys: List[EnumPlayerTurns] = [EnumPlayerTurns.NONE]
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_LEFT]:
            keys.append(EnumPlayerTurns.LEFT)
        if key_input[pygame.K_RIGHT]:
            keys.append(EnumPlayerTurns.RIGHT)
        if key_input[pygame.K_SPACE]:
            keys.append(EnumPlayerTurns.FIRE)
        if key_input[pygame.K_s]:
            keys.append(EnumPlayerTurns.SAVE)
        if key_input[pygame.K_ESCAPE]:
            keys.append(EnumPlayerTurns.EXIT)
        return keys

    def game_loop(self, name: str) -> None:
        self.__controller.load_game(name)
        clock = pygame.time.Clock()
        game_is_running = True
        while game_is_running:
            print(clock.get_fps())
            clock.tick(self.__fps)
            turn: List[EnumPlayerTurns] = self.handle_input() 

            if EnumPlayerTurns.EXIT in turn:
                break

            if EnumPlayerTurns.SAVE in turn and self.__save_cooldown == 0:
                self.__save_cooldown = 5 * self.__fps
                self.__controller.save_game()
            data = self.__controller.update_model(turn)
            self.render_objects(data)
            pygame.event.pump()
            self.__save_cooldown = max(0, self.__save_cooldown - 1)
            
        

    def render_objects(self, data: GameData) -> None:
        self.__win.fill((0, 0, 0))
        for obj in data.objects:
            pygame.draw.rect(self.__win, (0, 0, 255), obj.get_cords())
        pygame.draw.rect(self.__win, (255, 0, 0), data.player.get_cords())
        
        # player stats
        pygame.draw.rect(self.__win, (150, 150, 150), (0, 0, 1000, 80))
        pygame.draw.rect(self.__win, (255, 255, 255), (0, 0, 1000, 80), 2)


        pygame.display.update()
