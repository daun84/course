from controllers.interfaces.IControllerActorFactory import IControllerActorFactory
from controllers.interfaces.IControllerActor import IControllerActor
from controllers.ControllerActorKnight import ControllerActorKnight

from models.enums.EnumTribe import EnumTribe
from models.enums.EnumActor import EnumActor
from models.Vector2D import Vector2D
from models.Actor import Actor

import random
from typing import List, Tuple

class KnightControllerFactory(IControllerActorFactory):
    def __init__(self):
        super().__init__()

    def create_actor_controller(self, free_tiles: List[Tuple[int, int]], tribe: EnumTribe) -> IControllerActor:
        actor = Actor()
        actor.position = random.choice(free_tiles) 
        actor.tribe = tribe
        actor.actor_type = EnumActor.Knight
        controller = ControllerActorKnight(actor)
        return controller