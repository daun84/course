from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Callable, Tuple
from abc import ABC, abstractmethod
from constants import MAP_WIDTH, MAP_HEIGHT, EnumPlayerTurns
import pickle
import random

class DirectionVector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def inverse(self):
        self.x *= -1
        self.y *= -1


class GameObject:
    def __init__(self, x, y, width, height, name, speed, direction):
        self._x: int = x
        self._y: int = y
        self._width: int = width
        self._height: int = height
        self._name: str = name
        self._speed: int = speed
        self._direction: DirectionVector = direction
    
    def set_direction(self, direction: DirectionVector) -> None:
        self._direction = direction

    def get_cords(self) -> Tuple[int, int, int, int]:
        return self._x, self._y, self._width, self._height
    
    def move(self) -> None:
        pass


class Alien(GameObject):
    def __init__(self, x, y, name):
        super().__init__(x, y, 35, 25, name, 1, DirectionVector(1, 0))
        self._position_observer: Callable[[], None]
        self._leap_distance: int = 0 

    def set_observer(self, callback: Callable[[], None]) -> None:
        self._position_observer = callback

    def invoke_leap(self) -> None:
        self._leap_distance = self._height * 2

    def notify_observer(self) -> None:
        self._position_observer()
    
    def move(self):
        if self._leap_distance > 0:
            temp = min(self._speed * 2, self._leap_distance)
            self._y += self._speed * 2
            self._leap_distance = max(0, self._leap_distance - temp)
        else:
            self._x += self._direction.x * self._speed
            self._y += self._direction.y * self._speed

            if(self._x + self._width >= MAP_WIDTH or self._x <= 0):
                self.notify_observer()


class Player(GameObject):
    def __init__(self):
        super().__init__(450, 900, 50, 50, "player", 3, DirectionVector(0, 0))

    def move(self) -> None:
        new_pos = self._x + self._direction.x * self._speed
        if new_pos >= 0 and new_pos <= MAP_WIDTH - 50:
            self._x = new_pos


class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, 25, 25, "wall", 0, DirectionVector(0, 0))


class Rocket(GameObject):
    def __init__(self, x, y, name, direction: DirectionVector, speed):
        super().__init__(x, y, 10, 20, name, speed, direction)

    def move(self):
        self._x += self._direction.x * self._speed
        self._y += self._direction.y * self._speed 


@dataclass_json
@dataclass
class GameData:
    objects: List[GameObject] = field(default_factory=list)
    player: Player = field(default_factory=Player)
    score: int = 0
    health: int = 3
    player_cooldown: int = 0
    alien_cooldown: int = 0

class Game:
    def __init__(self):
        self._data = GameData()
        self._change_direction: bool = False
    
    def initialize_position(self, position: GameData) -> None:
        self._data = position
        for obj in self._data.objects:
            if type(obj) != Alien:
                continue
            obj.set_observer(self.set_change_direction)

    def set_change_direction(self) -> None:
        self._change_direction = True

    def change_alien_direction(self) -> None:
        for obj in self._data.objects:
            if type(obj) != Alien:
                continue
            obj._direction.inverse()
            obj.invoke_leap()

    def launch_rocket(self, x, y, name, direction: DirectionVector, speed) -> None:
        self._data.objects.append(Rocket(x, y, name, direction, speed))

    def handle_collision(self, obj: GameObject) -> None:
        if type(obj) == Player:
            self._data.health -= 1
        else:
            self._data.objects.remove(obj) 

    def are_intersected(self, obj1: GameObject, obj2: GameObject) -> bool:
        check_horiz1: bool = obj2._x < (obj1._x + obj1._width) and obj2._x >= obj1._x
        check_horiz2: bool = (obj2._x + obj2._width) > obj1._x and (obj2._x + obj2._width) <= (obj1._x + obj2._width)
        check_vert1: bool = obj2._y < (obj1._y + obj1._height) and obj2._y >= obj1._y
        check_vert2: bool = (obj2._y + obj2._height) > obj1._y and (obj2._y + obj2._height) <= (obj1._y + obj2._height)
        return (check_horiz1 or check_horiz2) and (check_vert1 or check_vert2)

    def check_collisions_for_object(self, target: GameObject) -> None:
        if type(target) == Rocket and (target._y <= 0 or target._y >= MAP_HEIGHT):
            self.handle_collision(target)
            return
        for obj in self._data.objects:
            if obj == target:
                continue
            if(self.are_intersected(target, obj)):
                self.handle_collision(obj)
                self.handle_collision(target)
                break

    def update_player(self, turn: List[EnumPlayerTurns]) -> None:
        direction: int = 0 
        if EnumPlayerTurns.LEFT in turn:
            direction -= 1
        if EnumPlayerTurns.RIGHT in turn:
            direction += 1
        self._data.player.set_direction(DirectionVector(direction, 0))
        if EnumPlayerTurns.FIRE in turn and self._data.player_cooldown == 0:
            self._data.player_cooldown = 30
            x: int = self._data.player._x + 15
            y: int = self._data.player._y - 40
            self.launch_rocket(x, y, "rocket", DirectionVector(0, -1), 12)

    def invoke_alien_attack(self) -> None:
        if self._data.alien_cooldown != 0:
            return
        self._data.alien_cooldown = 90

        aliens: List[Alien] = []
        chosen: List[Alien] = []
        
        for obj in self._data.objects:
            if type(obj) == Alien:
                aliens.append(obj)
                
        aliens.sort(key=lambda obj: (obj._x, -obj._y))

        x = -1
        for obj in aliens:
            if x != obj._x:
                x = obj._x
                chosen.append(obj)

        for obj in random.sample(chosen, min(3, len(chosen))):
            x = obj._x + 15
            y = obj._y + 50

            self.launch_rocket(x, y, "rocket", DirectionVector(0, 1), 7)
        

    def update(self, turn: List[EnumPlayerTurns]) -> None:
        self.update_player(turn)

        is_leaping: bool = False

        self._data.player.move()
        for obj in self._data.objects:
            obj.move()
        for obj in self._data.objects:
            self.check_collisions_for_object(obj)
            if type(obj) == Alien:
                is_leaping = obj._leap_distance > 0
        self.check_collisions_for_object(self._data.player)

        if not is_leaping:
            self.invoke_alien_attack()

        if self._change_direction:
            self.change_alien_direction()

        self._data.player_cooldown = max(0, self._data.player_cooldown - 1)
        self._data.alien_cooldown = max(0, self._data.alien_cooldown - 1)
        self._change_direction = False

    def get_data(self) -> GameData:
        return self._data
