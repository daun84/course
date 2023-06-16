from abc import ABC, abstractmethod

from models.enums.EnumTribe import EnumTribe
from models.Vector2D import Vector2D

from controllers.interfaces.IControllerActor import IControllerActor


class IControllerActorFactory:
    def __init__(self):
        pass

    @abstractmethod
    def create_actor_controller(self, position: Vector2D, tribe: EnumTribe) -> IControllerActor:
        pass