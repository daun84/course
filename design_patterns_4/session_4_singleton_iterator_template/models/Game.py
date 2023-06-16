from dataclasses import field
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from models.Actor import Actor
from models.MapBuilding import MapBuilding
from models.MapItem import MapItem
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumTribe import EnumTribe


@dataclass_json
@dataclass
class Game:
    map_size: Vector2D = field(default_factory=Vector2D)

    window_size: Vector2D = field(default_factory=Vector2D)
    window_location: Vector2D = field(default_factory=Vector2D)

    map_tiles: List[List[MapTile]] = field(default_factory=list)
    items: List[MapItem] = field(default_factory=list)
    buildings: List[MapBuilding] = field(default_factory=list)
    actors: List[Actor] = field(default_factory=list)

    tribes: List[EnumTribe] = field(default_factory=[EnumTribe.Imperius, EnumTribe.Hoodrick])

    turn: int = 0
    stars: int = 0

