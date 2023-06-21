from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D


@dataclass_json
@dataclass(kw_only=True)
class GameObject:
    position: Vector2D 
    width: int 
    height: int 
    name: str 
    speed: int 
    direction: Vector2D

    def get_cords(self) -> Tuple[int, int, int, int]:
        return self.position.x, self.position.y, self.width, self.height