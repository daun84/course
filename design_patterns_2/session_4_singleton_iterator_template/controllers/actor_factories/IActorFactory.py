from models.Vector2D import Vector2D
from models.Actor import Actor
from models.enums.EnumActor import EnumActor
from models.enums.EnumTribe import EnumTribe

from abc import ABC, abstractmethod
from typing import List

class IActorFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_actor(self, position: Vector2D, tribe: EnumTribe, free_tiles: List[Vector2D]) -> Actor:
        pass