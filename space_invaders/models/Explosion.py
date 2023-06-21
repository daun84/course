from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject
from models.Alien import ALIEN_HEIGHT, ALIEN_WIDTH


@dataclass_json
@dataclass(kw_only=True)
class Explosion(GameObject):
    width: int = ALIEN_WIDTH
    height: int = ALIEN_HEIGHT
    speed: int = 0
    name: str = "explosion"
    direction: Vector2D = field(default_factory=lambda: Vector2D(x=0,y=0))
    explosion_countdown: int = 5 # when it becomes zero, it ceases to exist