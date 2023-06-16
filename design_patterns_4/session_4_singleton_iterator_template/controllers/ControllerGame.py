import os.path
import random

from controllers.ControllerMap import ControllerMap
from models.Actor import Actor
from models.Game import Game
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumMapTile import EnumMapTile
from models.enums.EnumTribe import EnumTribe
from controllers.ControllerMap import MAP_HEIGHT, MAP_WIDTH

from typing import Dict, Tuple, List
from collections import defaultdict


class ControllerGame:

    __instance = None

    @staticmethod
    def instance():
        if ControllerGame.__instance is None:
            ControllerGame.__instance = ControllerGame()
        return ControllerGame.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance is allowed")
        self.__instance = self
        self.game: Game = None
        self.actors: Dict[Tuple[int, int], actor] = {}


    def init_actor(self, actor: Actor):
        self.actors[(actor.position.x, actor.position.y)] = actor

    def new_game(self):
        self.actors.clear()
        self.game = Game()
        self.game.window_size.x = 8
        self.game.window_size.y = 32

        ControllerMap.generate_map(self.game)
        ControllerMap.generate_initial_buildings(self.game)
        return self.game

    def make_a_move(self):
        for actor in self.game.actors:
            free_tiles = self.get_free_pos_near_target(actor.position.copy(), Vector2D(x=2, y=2))
            if free_tiles:
                actor.position = random.choice(free_tiles)

        print(self.game.turn)

    # position - tile near which we need to find free tiles
    def get_free_pos_near_target(self, position: Vector2D, radius: Vector2D) -> List[Vector2D]:
        free_positions: List[Vector2D] = []
        for i in range(max(0, position.y - radius.y), min(MAP_HEIGHT, position.y + radius.y)):
            for j in range(max(0, position.x - radius.x), min(MAP_WIDTH, position.x + radius.x)):
                temp = self.actors.get((j, i), Actor(tribe=EnumTribe.NotSet))
                if self.game.map_tiles[i][j].tile_type is EnumMapTile.Ground and temp.tribe == EnumTribe.NotSet:
                    free_positions.append(Vector2D(y=i, x=j))
        return free_positions


    


class MoveIterator:
    pass
