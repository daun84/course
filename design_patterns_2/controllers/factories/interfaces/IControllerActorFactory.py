from abc import ABC, abstractmethod

from controllers.interfaces.IControllerActor import IControllerActor

from models.Vector2D import Vector2D
from models.enums.EnumTribe import EnumTribe

class IControllerActorFactory(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_actor_controller(self, position: Vector2D, tribe: EnumTribe) -> IControllerActor:
        pass
