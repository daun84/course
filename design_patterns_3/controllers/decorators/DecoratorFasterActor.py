
from controllers.interfaces.IControllerActor import IControllerActor
from models.Actor import Actor


class DecoratorFasterActor(IControllerActor):
    def __init__(self, controller: IControllerActor):
        super().__init__(controller.actor)
        self._controller = controller
        self._controller.actor.speed += 0.5

    @property
    def actor(self) -> Actor:
        return self._controller.actor

    def do_turn(self):
        self._controller.do_turn()

    def update(self, delta_time):
        self._controller.update(delta_time)