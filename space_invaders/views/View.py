from controllers.GameController import GameController

from models.GameData import GameData
from models.Alien import Alien
from models.GameObject import GameObject
from models.Rocket import Rocket
from models.Wall import Wall
from models.GameData import MAP_WIDTH, MAP_HEIGHT
from models.enums.EnumPlayerTurns import EnumPlayerTurns

from views.menus.MainMenu import MainMenu
from views.menus.LoadMenu import LoadMenu

from time import sleep
import pygame
from pygame.locals import *
import os
from typing import List


class View:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.__controller: GameController = GameController.instance()
        self.__fps: int = 60
        self.__win = pygame.display.set_mode((MAP_WIDTH, MAP_HEIGHT))
        pygame.display.set_caption("Space invaders")
        self.__save_cooldown: int = 0
        self.font = pygame.font.Font("resources/fonts/RetroGaming.ttf", 36)
        # images
        self.images = {}
        self.images["invader1_1"] = pygame.image.load("resources/sprites/invader1_1.png")
        self.images["invader1_1"] = pygame.transform.scale(self.images["invader1_1"], (35, 25))
        self.images["invader1_2"] = pygame.image.load("resources/sprites/invader1_2.png")
        self.images["invader1_2"] = pygame.transform.scale(self.images["invader1_2"], (35, 25))
        self.images["invader2_1"] = pygame.image.load("resources/sprites/invader2_1.png")
        self.images["invader2_1"] = pygame.transform.scale(self.images["invader2_1"], (35, 25))
        self.images["invader2_2"] = pygame.image.load("resources/sprites/invader2_2.png")
        self.images["invader2_2"] = pygame.transform.scale(self.images["invader2_2"], (35, 25))
        self.images["invader3_1"] = pygame.image.load("resources/sprites/invader3_1.png")
        self.images["invader3_1"] = pygame.transform.scale(self.images["invader3_1"], (35, 25))
        self.images["invader3_2"] = pygame.image.load("resources/sprites/invader3_2.png")
        self.images["invader3_2"] = pygame.transform.scale(self.images["invader3_2"], (35, 25))

        self.player_image = pygame.image.load("resources/sprites/player.png")
        self.player_image = pygame.transform.scale(self.player_image, (50, 50))

        self.explosion_image = pygame.image.load("resources/sprites/explosion.png")
        self.explosion_image = pygame.transform.scale(self.explosion_image, (35, 25))

    def main(self):
        running = True
        main_menu = MainMenu(self.__win)
        while running:
            game_was_chosen: bool = False
            option: str = main_menu.run()
            if option == "QUIT":
                pygame.quit()
                running = False
            elif option == "NEW GAME":
                self.__controller.load_game("starting_position.pickle")
                game_was_chosen = True
            elif option == "LOAD GAME":
                load_menu = LoadMenu(self.__win)
                chosen_game: str = load_menu.run()
                self.__controller.load_game(chosen_game)
                game_was_chosen = True
            
            if game_was_chosen:
                    self.game_loop()


    def handle_input(self) -> List[EnumPlayerTurns]:
        keys: List[EnumPlayerTurns] = [EnumPlayerTurns.NotSet]
        key_input = pygame.key.get_pressed()
        if key_input[pygame.K_LEFT]:
            keys.append(EnumPlayerTurns.Left)
        if key_input[pygame.K_RIGHT]:
            keys.append(EnumPlayerTurns.Right)
        if key_input[pygame.K_SPACE]:
            keys.append(EnumPlayerTurns.Fire)
        if key_input[pygame.K_s]:
            keys.append(EnumPlayerTurns.Save)
        if key_input[pygame.K_ESCAPE]:
            keys.append(EnumPlayerTurns.Exit)
        return keys

    def print_to_center(self, message: str) -> None:
        self.__win.fill((0, 0, 0))
        text = self.font.render(message, True, (255, 255 ,255))
        rect = text.get_rect()
        rect.center = (MAP_WIDTH // 2, MAP_HEIGHT // 2)
        self.__win.blit(text, rect)
        pygame.display.update()
        sleep(1)

    def game_loop(self) -> None:
        clock = pygame.time.Clock()
        game_is_running = True
        while game_is_running:
            clock.tick(self.__fps)
            turn: List[EnumPlayerTurns] = self.handle_input() 

            if EnumPlayerTurns.Exit in turn:
                break

            if EnumPlayerTurns.Save in turn and self.__save_cooldown == 0:
                self.__save_cooldown = 5 * self.__fps
                self.__controller.save_game()

            game_status = self.__controller.update_game(turn)
            data = self.__controller.get_data() 
            self.render_objects(data)
            pygame.event.pump()
            self.__save_cooldown = max(0, self.__save_cooldown - 1)
            
            if game_status == 1:
                self.print_to_center("YOU SECURED THIS ROUND")
                self.print_to_center("PREPARE FOR NEXT ONE...")
                self.__controller.load_next_round()
            elif game_status == -1:
                self.print_to_center(f'YOU GOT {data.score} POINTS')
                break
        

    def render_objects(self, data: GameData) -> None:
        self.__win.fill((0, 0, 0))
        for obj in data.objects:
            if type(obj) == Alien:
                self.__win.blit(self.images[f'{obj.name}_{obj.current_frame + 1}'], (obj.position.x, obj.position.y))
            elif type(obj) == Rocket:
                pygame.draw.rect(self.__win, (255, 255, 255), obj.get_cords())
            elif type(obj) == Wall:
                pygame.draw.rect(self.__win, (0, 255, 0), obj.get_cords())
        self.__win.blit(self.player_image, (data.player.position.x, data.player.position.y))

        for expl in data.explosions:
            self.__win.blit(self.explosion_image, (expl.position.x, expl.position.y))
        
        
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