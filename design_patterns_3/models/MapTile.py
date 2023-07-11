from dataclasses import field
from dataclasses import dataclass
from models.Vector2D import Vector2D
from models.enums.EnumMapTile import EnumMapTile
from dataclasses_json import dataclass_json
import uuid
import struct

MAP_TILE_BYTE_COUNT = 28

@dataclass_json
@dataclass
class MapTile:
    uuid: str = uuid.uuid4()
    position: Vector2D = field(default_factory=Vector2D)
    tile_type: EnumMapTile = EnumMapTile.NotSet

    def to_bin(self) -> bytes:
        format_string = '16s3i'

        map_tile_enum_type: Dict[int, EnumMapTile] = {
            EnumMapTile.NotSet: 0,
            EnumMapTile.Ground: 1,
            EnumMapTile.Water: 2,
            EnumMapTile.Mountain: 3
        }

        data = struct.pack(format_string,
                           str(self.uuid).encode('utf-8'),
                           self.position.x, self.position.y,
                           map_tile_enum_type[self.tile_type])

        return data

    def from_bin(self, data: bytes):
        format_string = '16s3i'

        map_tile_enum_type: Dict[int, EnumMapTile] = {
            0: EnumMapTile.NotSet,
            1: EnumMapTile.Ground,
            2: EnumMapTile.Water,
            3: EnumMapTile.Mountain
        }

        unpacked_data = struct.unpack(format_string, data)
        self.uuid_str = unpacked_data[0].decode('utf-8')
        self.position = Vector2D(unpacked_data[1], unpacked_data[2])
        self.tile_type = map_tile_enum_type[unpacked_data[3]]