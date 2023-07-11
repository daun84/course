import os.path
import random
from typing import Tuple, Dict

from controllers.ControllerMap import ControllerMap
from controllers.commands.interfaces.ICommand import ICommand
from controllers.factories.ControllerKnightFactory import ControllerKnightFactory
from controllers.factories.ControllerRiderFactory import ControllerRiderFactory
from controllers.factories.ControllerWarriorFactory import ControllerWarriorFactory
from controllers.factories.interfaces.IControllerActorFactory import IControllerActorFactory
from controllers.decorators.DecoratorFasterActor import DecoratorFasterActor


from models.Actor import Actor
from models.Game import Game
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumMapTile import EnumMapTile
from models.MapBuilding import MapBuilding
from models.enums.EnumTribe import EnumTribe


class ControllerGame:
    __instance = None

    @staticmethod
    def instance():
        if ControllerGame.__instance is None:
            ControllerGame.__instance = ControllerGame()
        return ControllerGame.__instance

    def __init__(self):
        if ControllerGame.__instance is not None:
            raise Exception("Only one instance of ControllerGame allowed")
        ControllerGame.__instance = self
        self.game = None
        self.controllers_actors = []
        self.controller_factories: Dict[EnumActor, IControllerActor] = {
            EnumActor.Warrior: ControllerWarriorFactory(),
            EnumActor.Rider: ControllerRiderFactory(),
            EnumActor.Knight: ControllerKnightFactory()
        }


    def new_game(self):
        game = Game()
        self.game = game
        self.controllers_actors = []

        game.window_size.x = 8
        game.window_size.y = 32

        ControllerMap.generate_map(game)
        ControllerMap.generate_initial_buildings(game)
        return game

    def create_actor_controller(self, actor_type: EnumActor, tribe: EnumTribe, position: Vector2D, actor: Actor = None):
        if actor is None:
            actor = Actor()
        cont = self.controller_factories[actor_type].get_actor_controller(position, tribe, actor)
        if actor_type is EnumActor.Rider:
            cont = DecoratorFasterActor(cont)
        return cont

    def update_actors(self, delta_sec: float):
        for cont in self.controllers_actors:
            cont.update(delta_sec)

    def load_game(self):
        self.game.from_bin_file('state.bin')

        self.controllers_actors = []

        for actor in self.game.actors:
            cont = self.create_actor_controller(actor.actor_type, actor.tribe, actor.position.copy(), actor)
            self.controllers_actors.append(cont)