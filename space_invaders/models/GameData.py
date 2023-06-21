from typing import List
from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from models.Vector2D import Vector2D
from models.GameObject import GameObject
from models.Player import Player
from models.Explosion import Explosion

MAP_WIDTH, MAP_HEIGHT = 1000, 1000
ALIEN_ANIMATION_COUNTDOWN = 20

@dataclass_json
@dataclass(kw_only=True)
class GameData:
    objects: List[GameObject] = field(default_factory=list)
    player: Player = field(default_factory=Player)
    score: int = 0
    health: int = 3
    player_shot_cooldown: int = 0
    alien_shot_cooldown: int = 0
    alien_leap_countdown: int = 0 
    explosions: List[Explosion] = field(default_factory=list)
    alien_animation_countdown: int = ALIEN_ANIMATION_COUNTDOWN # when becomes zero, aliens should change sprite

