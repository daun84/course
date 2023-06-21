from models.Vector2D import Vector2D
from models.Actor import Actor
from models.enums.EnumActor import EnumActor
from models.enums.EnumTribe import EnumTribe

from controllers.actor_factories.IActorFactory import IActorFactory

class KnightFactory(IActorFactory):
    def __init__(self):
        pass

    def get_actor(self, position: Vector2D, tribe: EnumTribe):
        pass