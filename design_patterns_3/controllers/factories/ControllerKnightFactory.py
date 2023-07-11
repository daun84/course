from controllers.factories.interfaces.IControllerActorFactory import IControllerActorFactory
from controllers.interfaces.IControllerActor import IControllerActor
from controllers.ControllerActorKnight import ControllerActorKnight

from models.Actor import Actor
from models.Vector2D import Vector2D
from models.enums.EnumTribe import EnumTribe
from models.enums.EnumActor import EnumActor

class ControllerKnightFactory(IControllerActorFactory):
    def __init__(self):
        pass

    def get_actor_controller(self, position: Vector2D, tribe: EnumTribe, actor: Actor) -> IControllerActor:
        actor.position = position.copy()
        actor.position_target = position.copy()
        actor.tribe = tribe
        actor.actor_type = EnumActor.Knight
        controller = ControllerActorKnight(actor)
        return controller