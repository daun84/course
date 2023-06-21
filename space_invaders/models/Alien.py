from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject

ALIEN_HEIGHT = 25
ALIEN_WIDTH = 35

@dataclass_json
@dataclass(kw_only=True)
class Alien(GameObject):
    width: int = ALIEN_WIDTH
    height: int = ALIEN_HEIGHT
    speed: int = 1
    direction: Vector2D = field(default_factory=lambda: Vector2D(x=1,y=0))
    current_frame: int = 0 # there's two frames 