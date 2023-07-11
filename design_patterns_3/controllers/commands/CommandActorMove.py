from controllers.ControllerGame import ControllerGame
from controllers.commands.interfaces.ICommand import ICommand
from models.Actor import Actor
from models.Vector2D import Vector2D


class CommandActorMove(ICommand):
    def __init__(self, actor: Actor, position_target: Vector2D):
        self.actor = actor
        self.position_before = actor.position.copy()
        self.position_target = position_target

    def execute(self):
        self.actor.position_target = self.position_target

    def undo(self):
        self.actor.position_target = self.position_before
