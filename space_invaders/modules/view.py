import pygame
from pygame.locals import *
import os
from singleton import SingletonMeta
from controller import Controller
from typing import List
from model import GameData, Alien, GameObject, Rocket, Wall
from constants import MAP_WIDTH, MAP_HEIGHT, EnumPlayerTurns

class Menu:
    def __init__(self, menu_options: List[str], window: pygame.surface.Surface):
        self.options: List[str] = menu_options
        self.font = pygame.font.Font("../resources/RetroGaming.ttf", 32)
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
        self.headline_font = pygame.font.Font("../resources/RetroGaming.ttf", 48)
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
        self.font = pygame.font.Font("../resources/RetroGaming.ttf", 36)
        # images
        self.images = {}
        self.images["invader1_1"] = pygame.image.load("../resources/invader1_1.png")
        self.images["invader1_1"] = pygame.transform.scale(self.images["invader1_1"], (35, 25))
        self.images["invader1_2"] = pygame.image.load("../resources/invader1_2.png")
        self.images["invader1_2"] = pygame.transform.scale(self.images["invader1_2"], (35, 25))
        self.images["invader2_1"] = pygame.image.load("../resources/invader2_1.png")
        self.images["invader2_1"] = pygame.transform.scale(self.images["invader2_1"], (35, 25))
        self.images["invader2_2"] = pygame.image.load("../resources/invader2_2.png")
        self.images["invader2_2"] = pygame.transform.scale(self.images["invader2_2"], (35, 25))
        self.images["invader3_1"] = pygame.image.load("../resources/invader3_1.png")
        self.images["invader3_1"] = pygame.transform.scale(self.images["invader3_1"], (35, 25))
        self.images["invader3_2"] = pygame.image.load("../resources/invader3_2.png")
        self.images["invader3_2"] = pygame.transform.scale(self.images["invader3_2"], (35, 25))

        self.player_image = pygame.image.load("../resources/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))

        self.explosion_image = pygame.image.load("../resources/explosion.png")
        self.explosion_image = pygame.transform.scale(self.explosion_image, (35, 25))
        

    def main(self):
        running = True
        main_menu = MainMenu(self.__win)
        while running:
            option: str = main_menu.run()
            if option == "QUIT":
                pygame.quit()
                running = False
            elif option == "NEW GAME":
                self.game_loop("../resources/starting_position.pickle")
            elif option == "LOAD GAME":
                load_menu = LoadMenu(self.__win)
                name = load_menu.run()
                if ".pickle" in name:
                    self.game_loop(name)

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
            #print(clock.get_fps())
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
            if data.game_status != 0:
                break
            
        

    def render_objects(self, data: GameData) -> None:
        self.__win.fill((0, 0, 0))
        for obj in data.objects:
            if type(obj) == Alien:
                self.__win.blit(self.images[f'invader2_{obj._frame + 1}'], (obj._x, obj._y))
            elif type(obj) == Rocket:
                pygame.draw.rect(self.__win, (255, 255, 255), obj.get_cords())
            elif type(obj) == Wall:
                pygame.draw.rect(self.__win, (0, 255, 0), obj.get_cords())
        self.__win.blit(self.player_image, (data.player._x, data.player._y))
        
        for expl in data.explosions:
            self.__win.blit(self.explosion_image, (expl._x, expl._y))
        
        # player stats
        pygame.draw.rect(self.__win, (0, 0, 0), (0, 0, 1000, 80))
        pygame.draw.rect(self.__win, (255, 255, 255), (0, 0, 1000, 80), 2)

        health_text = self.font.render(f'{data.health * "<3 "}', True, (255, 0, 0))  
        health_rect = health_text.get_rect()
        health_rect.center = (120, 40) 
        self.__win.blit(health_text, health_rect)
        higscore_text = self.font.render(f'SCORE: {data.score}', True, (255, 255 ,255))
        higscore_rect = higscore_text.get_rect()
        higscore_rect.center = (800, 40)
        self.__win.blit(higscore_text, higscore_rect)

        pygame.display.update()