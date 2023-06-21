from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject


@dataclass_json
@dataclass(kw_only=True)
class Player(GameObject):
    position: Vector2D = field(default_factory=lambda: Vector2D(x=450,y=930))
    width: int = 50
    height: int = 50
    name: str = "player"
    speed: int = 3
    direction: Vector2D = field(default_factory=lambda: Vector2D(x=0,y=0))