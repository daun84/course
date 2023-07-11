from controllers.factories.interfaces.IControllerActorFactory import IControllerActorFactory
from controllers.interfaces.IControllerActor import IControllerActor
from controllers.ControllerActorRider import ControllerActorRider

from models.Actor import Actor
from models.Vector2D import Vector2D
from models.enums.EnumTribe import EnumTribe
from models.enums.EnumActor import EnumActor

class ControllerRiderFactory(IControllerActorFactory):
    def __init__(self):
        pass

    def get_actor_controller(self, position: Vector2D, tribe: EnumTribe) -> IControllerActor:
        actor = Actor()
        actor.position = position.copy()
        actor.tribe = tribe
        actor.actor_type = EnumActor.Rider
        controller = ControllerActorRider(actor)
        return controller