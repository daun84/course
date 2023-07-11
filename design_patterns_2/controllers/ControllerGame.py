from controllers.ControllerMap import ControllerMap
from controllers.interfaces.IControllerActor import IControllerActor
from controllers.factories.ControllerKnightFactory import ControllerKnightFactory
from controllers.factories.ControllerRiderFactory import ControllerRiderFactory
from controllers.factories.ControllerWarriorFactory import ControllerWarriorFactory
from controllers.factories.interfaces.IControllerActorFactory import IControllerActorFactory

from models.Actor import Actor
from models.Game import Game
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumMapTile import EnumMapTile
from models.enums.EnumTribe import EnumTribe
from models.MapBuilding import MapBuilding

from views.components.EventComponentButton import EventComponentButton

from utils.iterator.CollectionActorControllers import CollectionActorControllers

import os.path
import random
from typing import Dict

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
        self.game: Game = None
        self.controller_factories: Dict[EnumActor, IControllerActor] = {
            EnumActor.Warrior: ControllerWarriorFactory(),
            EnumActor.Rider: ControllerRiderFactory(),
            EnumActor.Knight: ControllerKnightFactory()
        }
        self.selected_building: MapBuilding = None
        self.controllers_actors: List[IControllerActor] = []

    def new_game(self):
        self.game = Game()
        self.game.window_size.x = 8
        self.game.window_size.y = 32

        self.game.playing_tribes = [EnumTribe.Imperius, EnumTribe.Hoodrick]
        self.game.turn_tribe = EnumTribe.Imperius

        self.controllers_actors = []
        self.controller_actor_collection = CollectionActorControllers(self.controllers_actors)

        ControllerMap.generate_map(self.game)
        ControllerMap.generate_initial_buildings(self.game)
        
        return self.game

    def on_click_end_turn(self, event: EventComponentButton):
        for tribe, actor_controllers in self.controller_actor_collection:
            if tribe is self.game.turn_tribe:
                for cont in actor_controllers:
                    cont.do_turn()

        self.game.turn += 1
        tribe_idx = self.game.turn % len(self.game.playing_tribes)
        self.game.turn_tribe = self.game.playing_tribes[tribe_idx]
            

    def update_actors(self, delta_sec: float):
        for cont in self.controllers_actors:
            cont.update(delta_sec)

    def on_click_create_actor(self, event: EventComponentButton):
        position: Vector2D = self.selected_building.position.copy()
        position.x += random.randint(-2, 2)
        position.y += random.randint(-2, 2)
        actor_controller = self.controller_factories[event.linked_enum].get_actor_controller(position, self.selected_building.tribe)
        self.controllers_actors.append(actor_controller)
        self.game.actors.append(actor_controller.actor)