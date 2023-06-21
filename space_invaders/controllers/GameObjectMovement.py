from models.GameObject import GameObject
from models.Alien import Alien, ALIEN_HEIGHT
from models.GameData import MAP_HEIGHT, MAP_WIDTH

from controllers.enums.EnumAlienEventType import EnumAlienEventType

from typing import List

LAST_RESORT_LINE = 850

class GameObjectMovement:
    __instance = None

    @staticmethod
    def instance():
        if GameObjectMovement.__instance is None:
            GameObjectMovement.__instance = GameObjectMovement()
        return GameObjectMovement.__instance

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Only one instance is allowed")
        self.__instance = self
        self.__listeners_border_reach: List[callable] = []

    def move_objects(self, objects: List[GameObject], alien_leap_countdown: int):
        event_type: EnumAlienEventType = EnumAlienEventType.NotSet
        for obj in objects:
            if type(obj) == Alien and alien_leap_countdown > 0:
                obj.position.y += 5
            else:
                obj.position.x = max(0, min(MAP_WIDTH - obj.width, obj.position.x + obj.direction.x * obj.speed))
                obj.position.y = max(0, min(MAP_HEIGHT, obj.position.y + obj.direction.y * obj.speed))
                if type(obj) == Alien and (obj.position.x == 0 or obj.position.x == MAP_WIDTH - obj.width):
                    event_type = EnumAlienEventType.SideBorderReach
            if type(obj) == Alien and (obj.position.y >= LAST_RESORT_LINE):
                event_type = EnumAlienEventType.BottomBorderReach
                break
        self.notify_listeners(event_type)

    def notify_listeners(self, event_type: EnumAlienEventType):
        for listener in self.__listeners_border_reach:
            listener(event_type)

    def add_listener_border_reach(self, func_on_border_reach):
        if func_on_border_reach not in self.__listeners_border_reach:
            self.__listeners_border_reach.append(func_on_border_reach)

    def remove_listener_border_reach(self, func_on_border_reach):
        if func_on_border_reach in self.__listeners_border_reach:
            self.__listeners_border_reach.remove(func_on_border_reach)

