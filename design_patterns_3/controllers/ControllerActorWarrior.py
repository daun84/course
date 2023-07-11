import random

from controllers.interfaces.IControllerActor import IControllerActor
from models.Actor import Actor


class ControllerActorWarrior(IControllerActor):
    def __init__(self, actor):
        super().__init__(actor)
        self._actor = actor
        self._actor.speed = 1.5

    @property
    def actor(self) -> Actor:
        return self._actor

    def do_turn(self):
        self.actor.position_target.x = self.actor.position.x + random.randint(-3, 3)
        self.actor.position_target.y = self.actor.position.y + random.randint(-3, 3)
        # TODO check positions that are free and then select randomly from free positions

    def update(self, delta_time):
        if self.actor.position.x != self.actor.position_target.x or self.actor.position.y != self.actor.position_target.y:
            self.actor.position.x += (1 if (self.actor.position_target.x - self.actor.position.x) > 0 else -1) * delta_time * self._actor.speed
            self.actor.position.y += (1 if (self.actor.position_target.y - self.actor.position.y) > 0 else -1) * delta_time * self._actor.speed

            if abs(self.actor.position.x - self.actor.position_target.x) < 1e-1:
                self.actor.position.x = self.actor.position_target.x
            if abs(self.actor.position.y - self.actor.position_target.y) < 1e-1:
                self.actor.position.y = self.actor.position_target.y
