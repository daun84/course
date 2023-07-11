from controllers.ControllerGame import ControllerGame
from controllers.commands.interfaces.ICommand import ICommand
from controllers.interfaces.IControllerActor import IControllerActor

from models.Actor import Actor
from models.Vector2D import Vector2D
from models.MapBuilding import MapBuilding
from models.enums.EnumActor import EnumActor

import random


class CommandCreateActor(ICommand):
    def __init__(self, selected_building: MapBuilding, actor_type: EnumActor):
        self.controller_actor: IControllerActor = None
        self.controller_game: ControllerGame = ControllerGame.instance()
        self.selected_building = selected_building
        self.actor_type = actor_type
        self.position = selected_building.position.copy()
        self.actor = Actor()
        self.position.x += random.randint(-2, 2)
        self.position.y += random.randint(-2, 2)
        self.controller_actor = self.controller_game.create_actor_controller(self.actor_type,
                                                                             self.selected_building.tribe, 
                                                                             self.position,
                                                                             self.actor)

    def execute(self):
        self.controller_game.controllers_actors.append(self.controller_actor)
        self.controller_game.game.actors.append(self.controller_actor.actor)

    def undo(self):
        if self.controller_actor in self.controller_game.controllers_actors:
            self.controller_game.game.actors.remove(self.controller_actor.actor)
            self.controller_game.controllers_actors.remove(self.controller_actor)
        self.controller_actor = self.controller_game.create_actor_controller(self.actor_type,
                                                                             self.selected_building.tribe, 
                                                                             self.position,
                                                                             self.actor)
