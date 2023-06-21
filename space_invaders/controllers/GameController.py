from models.GameData import GameData, MAP_HEIGHT, MAP_WIDTH, ALIEN_ANIMATION_COUNTDOWN
from models.Alien import Alien, ALIEN_HEIGHT, ALIEN_WIDTH
from models.Wall import Wall
from models.Vector2D import Vector2D
from models.GameObject import GameObject
from models.Player import Player
from models.enums.EnumPlayerTurns import EnumPlayerTurns
from models.Rocket import Rocket
from models.Explosion import Explosion

from controllers.GameObjectMovement import GameObjectMovement
from controllers.enums.EnumAlienEventType import EnumAlienEventType

import random
import pickle
import pygame
import json
import time
import os

from typing import List
from datetime import datetime


class GameController:
    __instance = None

    #
    # interface for view module
    #

    @staticmethod
    def instance():
        if GameController.__instance is None:
            GameController.__instance = GameController()
        return GameController.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance is allowed")
        self.__instance = self
        self.__data = GameData()
        self.__object_mover = GameObjectMovement.instance()
        self.__object_mover.add_listener_border_reach(self.__on_alien_border_reach)
        self.__aliens_reached_bottom: bool = False

    def load_game(self, file_name: str):
        with open(f'saves/{file_name}', "rb") as file:
            self.__data = pickle.load(file)
        
    def save_game(self):
        file_name: str = datetime.now().strftime("saves/%Y-%m-%d_%H:%M:%S.pickle")
        with open(file_name, "wb") as file:
            pickle.dump(self.__data, file)

    def load_next_round(self):

        for obj in self.__data.objects:
            if type(obj) == Rocket:
                self.__data.objects.remove(obj)

        for i in range(2):
            for j in range(10):
                self.__data.objects.append(
                    Alien(position=Vector2D(x=j * 70, y=i * 70 + 100), name="invader1"))
        for i in range(2):
            for j in range(10):
                self.__data.objects.append(
                    Alien(position=Vector2D(x=j * 70, y=i * 70 + 240), name="invader2"))
        for i in range(2):
            for j in range(10):
                self.__data.objects.append(
                    Alien(position=Vector2D(x=j * 70, y=i * 70 + 380), name="invader3"))
        self.__data.health: int = 3
        self.__data.player_shot_cooldown: int = 0
        self.__data.alien_shot_cooldown: int = 0
        self.__data.alien_leap_countdown: int = 0 

    # -1 - lose, 0 - continues, 1 - round secured
    def update_game(self, turn: List[EnumPlayerTurns]) -> int:
        self.__object_mover.move_objects(self.__data.objects, self.__data.alien_leap_countdown)

        self.__update_player(turn)
        player = self.__data.player
        player.position.x = max(0, min(MAP_WIDTH - player.width, player.position.x + player.direction.x * player.speed))

        for obj in self.__data.objects:
            self.__check_collisions_for_object(obj)
        self.__check_collisions_for_object(self.__data.player)

        if not self.__data.alien_leap_countdown:
            self.__invoke_alien_attack()

        self.__data.player_shot_cooldown = max(0, self.__data.player_shot_cooldown - 1)
        self.__data.alien_shot_cooldown = max(0, self.__data.alien_shot_cooldown - 1)
        self.__data.alien_leap_countdown = max(0, self.__data.alien_leap_countdown - 1)

        self.__data.alien_animation_countdown = max(0, self.__data.alien_animation_countdown - 1)
        if self.__data.alien_animation_countdown == 0:
            self.__data.alien_animation_countdown = ALIEN_ANIMATION_COUNTDOWN
            for obj in self.__data.objects:
                if type(obj) is not Alien:
                    continue
                obj.current_frame = 1 - obj.current_frame 

        for expl in self.__data.explosions:
            expl.explosion_countdown = max(0, expl.explosion_countdown - 1)
            if expl.explosion_countdown == 0:
                self.__data.explosions.remove(expl)

        game_status: int = 0

        has_aliens = any(isinstance(obj, Alien) for obj in self.__data.objects)

        if not has_aliens:
            game_status = 1

        if self.__data.health <= 0 or self.__aliens_reached_bottom:
            game_status = -1

        self.__aliens_reached_bottom = False

        return game_status

    def get_data(self):
        return self.__data

    # 
    # in-game logic
    #  

    def __on_alien_border_reach(self, event_type: EnumAlienEventType):
        if event_type is EnumAlienEventType.SideBorderReach:
            for obj in self.__data.objects:
                if type(obj) is not Alien:
                    continue
                obj.direction = -obj.direction
            self.__data.alien_leap_countdown = 15
        elif event_type is EnumAlienEventType.BottomBorderReach:
            self.__aliens_reached_bottom = True

    def __launch_rocket(self, x, y, name, direction: Vector2D, speed):
        self.__data.objects.append(Rocket(position=Vector2D(x,y), name=name, direction=direction, speed=speed))

    def __handle_collision(self, obj: GameObject):
        if type(obj) == Player:
            self.__data.health -= 1
        elif type(obj) == Alien: 
            self.__data.score += 50
            self.__data.explosions.append(Explosion(position=obj.position))
            self.__data.objects.remove(obj)
        else:
            self.__data.objects.remove(obj) 

    def __are_intersected(self, obj1: GameObject, obj2: GameObject) -> bool:
        check_horiz1: bool = obj2.position.x < (obj1.position.x + obj1.width) and obj2.position.x >= obj1.position.x
        check_horiz2: bool = (obj2.position.x + obj2.width) > obj1.position.x and (obj2.position.x + obj2.width) <= (obj1.position.x + obj2.width)
        check_vert1: bool = obj2.position.y < (obj1.position.y + obj1.height) and obj2.position.y >= obj1.position.y
        check_vert2: bool = (obj2.position.y + obj2.height) > obj1.position.y and (obj2.position.y + obj2.height) <= (obj1.position.y + obj2.height)
        return (check_horiz1 or check_horiz2) and (check_vert1 or check_vert2)

    def __check_collisions_for_object(self, target: GameObject):
        if type(target) == Rocket and (target.position.y <= 0 or target.position.y >= MAP_HEIGHT):
            self.__handle_collision(target)
            return
        for obj in self.__data.objects:
            if obj == target:
                continue
            if self.__are_intersected(target, obj):
                self.__handle_collision(obj)
                self.__handle_collision(target)
                break

    def __update_player(self, turn: List[EnumPlayerTurns]):
        direction: int = 0 
        if EnumPlayerTurns.Left in turn:
            direction -= 1
        if EnumPlayerTurns.Right in turn:
            direction += 1
        self.__data.player.direction = Vector2D(direction, 0)
        if EnumPlayerTurns.Fire in turn and self.__data.player_shot_cooldown == 0:
            self.__data.player_shot_cooldown = 30 
            x: int = self.__data.player.position.x + 20
            y: int = self.__data.player.position.y - 20
            self.__launch_rocket(x, y, "rocket", Vector2D(0, -1), 12)

    def __invoke_alien_attack(self):
        if self.__data.alien_shot_cooldown != 0:
            return
        self.__data.alien_shot_cooldown = 90

        aliens: List[Alien] = []
        chosen: List[Alien] = []
        
        for obj in self.__data.objects:
            if type(obj) == Alien:
                aliens.append(obj)
                
        aliens.sort(key=lambda obj: (obj.position.x, -obj.position.y))

        x = -1
        for obj in aliens:
            if x != obj.position.x:
                x = obj.position.x
                chosen.append(obj)

        for obj in random.sample(chosen, min(3, len(chosen))):
            x = obj.position.x + 15
            y = obj.position.y + 50 
            self.__launch_rocket(x, y, "rocket", Vector2D(0, 1), 7)
