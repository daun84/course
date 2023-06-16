from controllers.interfaces.IControllerActorFactory import IControllerActorFactory
from controllers.interfaces.IControllerActor import IControllerActor
from controllers.ControllerActorRider import ControllerActorRider

from models.enums.EnumTribe import EnumTribe
from models.enums.EnumActor import EnumActor
from models.Vector2D import Vector2D
from models.Actor import Actor

import random
from typing import List, Tuple

class RiderControllerFactory(IControllerActorFactory):
    def __init__(self):
        super().__init__()

    def create_actor_controller(self, free_tiles: List[Tuple[int, int]], tribe: EnumTribe) -> IControllerActor:
        actor = Actor()
        actor.position = random.choice(free_tiles) 
        actor.tribe = tribe
        actor.actor_type = EnumActor.Rider
        controller = ControllerActorRider(actor)
        return controller