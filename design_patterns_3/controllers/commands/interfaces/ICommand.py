import abc
from abc import abstractmethod
from models.Actor import Actor


class ICommand(abc.ABC):

    @abstractmethod
    def execute(self):
        pass

    @abstractmethod
    def undo(self):
        pass