from dataclasses import field
from dataclasses import dataclass
from models.Vector2D import Vector2D
from dataclasses_json import dataclass_json

from models.enums.EnumBuilding import EnumBuilding
from models.enums.EnumTribe import EnumTribe
import uuid
import struct

MAP_BUILDING_BYTE_COUNT = 36

@dataclass_json
@dataclass
class MapBuilding:
    uuid: str = uuid.uuid4()
    position: Vector2D = field(default_factory=Vector2D)
    building_type: EnumBuilding = EnumBuilding.NotSet
    tribe: EnumTribe = EnumTribe.NotSet
    level = 1

    def to_bin(self) -> bytes:
        format_string = '16s5i' 

        tribe_enum_values: Dict[EnumTribe, int] = {
            EnumTribe.NotSet: 0,
            EnumTribe.Imperius: 1,
            EnumTribe.Hoodrick: 2
        }

        building_enum_values: Dict[EnumBuilding, int] = {
            EnumBuilding.NotSet: 0,
            EnumBuilding.City: 1,
            EnumBuilding.Sawmill: 2 
        }

        data = struct.pack(format_string,
                           str(self.uuid).encode('utf-8'),
                           self.position.x, self.position.y,
                           building_enum_values[self.building_type], 
                           tribe_enum_values[self.tribe],
                           self.level)

        return data

    def from_bin(self, data: bytes):
        format_string = '16s5i'

        tribe_enum_values: Dict[int, EnumTribe] = {
            0: EnumTribe.NotSet,
            1: EnumTribe.Imperius,
            2: EnumTribe.Hoodrick
        }

        building_enum_values: Dict[int, EnumBuilding] = {
            0: EnumBuilding.NotSet,
            1: EnumBuilding.City,
            2: EnumBuilding.Sawmill 
        }

        unpacked_data = struct.unpack(format_string, data)
        self.uuid = unpacked_data[0].decode('utf-8')
        self.position = Vector2D(unpacked_data[1], unpacked_data[2])
        self.building_type = building_enum_values[unpacked_data[3]]
        self.tribe = tribe_enum_values[unpacked_data[4]]
        self.level = unpacked_data[5]