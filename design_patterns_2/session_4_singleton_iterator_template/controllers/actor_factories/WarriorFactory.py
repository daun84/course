from models.Vector2D import Vector2D
from models.Actor import Actor
from models.enums.EnumActor import EnumActor
from models.enums.EnumTribe import EnumTribe

from controllers.actor_factories.IActorFactory import IActorFactory

import random

class WarriorFactory(IActorFactory):
    def __init__(self):
        pass

    def get_actor(self, tribe: EnumTribe, free_tiles: List[Vector2D]) -> Actor:
        pos = random.choice(free_tiles)
        a = Actor()
        a.actor_type = EnumActor.Warrior
        a.tribe = tribe
        a.position = pos
        return a 

