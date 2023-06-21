from typing import List, Callable, Tuple
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject


@dataclass_json
@dataclass(kw_only=True)
class Rocket(GameObject):
    width: int = 5
    height: int = 15