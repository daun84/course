from enum import Enum
from abc import ABC, abstractmethod
from typing import List


class Vector2D:
    def __init__(self):
        self.x = 0.0
        self.y = 0.0

    def __add__(self, vec):
        pass

    def __sub__(self, vec):
        pass


class EnumTribe(Enum):
    NONE = 0
    PLAYER = 1
    OPPONENT = 2


class EnumSeason(Enum):
    NONE = 0
    WINTER = 1
    SUMMER = 2


class Actor(ABC):
    def __init__(self):
        self.tribe = EnumTribe.NONE
        self.coins_cost = 0
        self.move_steps = 0
        self.power_attack = 0
        self.power_defense = 0
        self.experience = 0
        self.level = 0

    @abstractmethod
    def move(self, pos: Vector2D):
        pass


class Warrior(Actor):
    def move(self, pos: Vector2D):
        pass

class Horseman(Actor):
    def move(self, pos: Vector2D):
        pass


class Knight(Horseman):
    def move(self, pos: Vector2D):
        pass


class Item:
    def __init__(self):
        self.is_consumable = False
        self.coins_collect = 0


class Fruit(Item):
    def collect(self):
        pass


class Forest(Item):
    pass


class Building(Item):
    def __init__(self):
        super().__init__()
        self.level = 0


class Sawmill(Building):
    pass


class Village(Building):
    def capture(self):
        pass


class City(Village):
    pass


class MapTile:
    def __init__(self):
        self.position: Vector2D
        self.season: EnumSeason = EnumSeason.NONE
        self.tribe: EnumTribe = EnumTribe.NONE
        self.items_on_tile: List[Item] = []
        self.actor_on_tile: List[Actor] = []
        self.is_visible_for_tribe: List[EnumTribe] = []


class Land(MapTile):
    pass


class Mountain(MapTile):
    pass


class Water(MapTile):
    pass


class Game:
    def __init__(self):
        self.map_size: Vector2D
        self.turn = 0
        self.__map_tiles: List[MapTile] = []

    def get_map_tiles(self):
        return self.__map_tiles

    def update_step(self, tribe: EnumTribe, actor: Actor):
        pass




