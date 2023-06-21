from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject


@dataclass_json
@dataclass(kw_only=True)
class Wall(GameObject):
    width: int = 25
    height: int = 25
    name: str = "wall"
    speed: int = 0
    direction: Vector2D = field(default_factory=lambda: Vector2D(x=0,y=0))

