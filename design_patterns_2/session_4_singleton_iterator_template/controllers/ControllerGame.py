import os.path
import random

from controllers.ControllerMap import ControllerMap
from controllers.iterators.CollectionTribes import CollectionTribes
from controllers.actor_factories.KnightFactory import KnightFactory
from controllers.actor_factories.WarriorFactory import WarriorFactory
from controllers.actor_factories.RiderFactory import RiderFactory
from controllers.actor_factories.IActorFactory import IActorFactory

from models.Actor import Actor
from models.Game import Game
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumMapTile import EnumMapTile
from models.enums.EnumTribe import EnumTribe

from typing import Dict, Tuple

class ControllerGame:
    __instance = None

    @staticmethod
    def instance():
        if ControllerGame.__instance is None:
            ControllerGame.__instance = ControllerGame()
        return ControllerGame.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance of ControllerGame is allowed")
        self.__instance = self
        self.__map_controller = ControllerMap.instance()
        self.__tribe_iter = CollectionTribes([EnumTribe.Imperius, EnumTribe.Hoodrick])
        self.__actors_position = Dict[Tuple[int, int], EnumTribe]
        self.game: Game = None

        self.__actor_factories: Dict[EnumActor, IActorFactory] = {
            EnumActor.Warrior: WarriorFactory(),
            EnumActor.Rider: RiderFactory(),
            EnumActor.Knight: KnightFactory()
        }

    def new_game(self):
        self.game = Game()
        self.game.window_size.x = 8
        self.game.window_size.y = 32

        self.__tribe_iter = CollectionTribes([EnumTribe.Imperius, EnumTribe.Hoodrick]) 

        self.__map_controller.generate_map(self.game)
        self.__map_controller.generate_initial_buildings(self.game)

    def make_tribe_move(self):
        current_tribe = next(self.__tribe_iter)
        count: int = 0
        for actor in self.game.actors:
            if actor.tribe is not current_tribe:
                continue
            count += 1


    def create_actor(self, position: Vector2D, tribe: EnumTribe, actor_type: EnumActor):
        free_tiles: List[Vector2D] = self.get_free_tiles_in_radius(position, Vector2D(2, 2), tribe)
        if free_tiles:
            actor = self.__actor_factories[actor_type].get_actor(position, tribe)   
            self.game.actors.append(actor)
            self.__actors_position[(actor.position.x, actor.position.y)] = tribe

    def get_free_tiles_in_radius(self, position: Vector2D, radius: Vector2D, tribe: EnumTribe) -> List[Vector2D]:
        free_tiles: List[Vector2D] = []
        for i in range(position.x - radius.x, position.x + radius.x):
            for j in range(position.y - radius.y, position.y + radius.y):
                if self.game.map_tiles[i][j] is EnumMapTile.Ground and self.__actors_position.get((i, j), EnumTribe.NotSet) is not tribe:
                    free_tiles.append(Vector2D(i,j))
        return free_tiles

    
