from dataclasses import field
from dataclasses import dataclass
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumTribe import EnumTribe
from dataclasses_json import dataclass_json
import uuid
import struct

ACTOR_BYTE_COUNT = 68

@dataclass_json
@dataclass
class Actor:
    uuid: str = uuid.uuid4()
    position: Vector2D = field(default_factory=Vector2D)
    position_target: Vector2D = field(default_factory=Vector2D)

    actor_type: EnumActor = EnumActor.NotSet
    tribe: EnumTribe = EnumTribe.NotSet

    cost_stars: int = 0
    move_steps: int = 0
    power_attack: int = 0
    power_defense: int = 0
    experience: int = 0
    level: int = 0
    speed: float = 0.0

    def to_bin(self) -> bytes:
        format_string = '16s2f10if'

        actor_enum_values: Dict[EnumActor, int] = {
            EnumActor.NotSet: 0,
            EnumActor.Warrior: 1,
            EnumActor.Rider: 2,
            EnumActor.Knight: 3
        }

        tribe_enum_values: Dict[EnumTribe, int] = {
            EnumTribe.NotSet: 0,
            EnumTribe.Imperius: 1,
            EnumTribe.Hoodrick: 2
        }

        data = struct.pack(format_string,
                           str(self.uuid).encode('utf-8'),
                           self.position.x, self.position.y,
                           self.position_target.x, self.position_target.y,
                           actor_enum_values[self.actor_type],
                           tribe_enum_values[self.tribe],
                           self.cost_stars, self.move_steps,
                           self.power_attack, self.power_defense,
                           self.experience, self.level, self.speed)

        return data

    def from_bin(self, data: bytes):
        format_string = '16s2f10if'

        actor_enum_values: Dict[int, EnumActor] = {
            0: EnumActor.NotSet,
            1: EnumActor.Warrior,
            2: EnumActor.Rider,
            3: EnumActor.Knight
        }

        tribe_enum_values: Dict[int, EnumTribe] = {
            0: EnumTribe.NotSet,
            1: EnumTribe.Imperius,
            2: EnumTribe.Hoodrick
        }

        unpacked_data = struct.unpack(format_string, data)
        self.uuid = unpacked_data[0].decode('utf-8')
        self.position = Vector2D(unpacked_data[1], unpacked_data[2])
        self.position_target = Vector2D(unpacked_data[3], unpacked_data[4])
        self.actor_type = actor_enum_values[unpacked_data[5]]
        self.tribe = tribe_enum_values[unpacked_data[6]]
        self.cost_stars = unpacked_data[7]
        self.move_steps = unpacked_data[8]
        self.power_attack = unpacked_data[9]
        self.power_defense = unpacked_data[10]
        self.experience = unpacked_data[11]
        self.level = unpacked_data[12]
        self.speed = unpacked_data[13]
