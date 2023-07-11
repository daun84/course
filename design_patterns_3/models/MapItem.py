from dataclasses import field
from dataclasses import dataclass
from models.Vector2D import Vector2D
from dataclasses_json import dataclass_json
from models.enums.EnumMapItem import EnumMapItem
import uuid
import struct

MAP_ITEM_BYTE_COUNT = 28

@dataclass_json
@dataclass
class MapItem:
    uuid: str = uuid.uuid4()
    position: Vector2D = field(default_factory=Vector2D)
    item_type: EnumMapItem = EnumMapItem.NotSet

    def to_bin(self) -> bytes:
        format_string = '16s3i'

        map_item_enum_value: Dict[int, EnumMapItem] = {
            EnumMapItem.NotSet: 0,
            EnumMapItem.Fruit: 1,
            EnumMapItem.Forrest: 2,
        }

        data = struct.pack(format_string,
                           str(self.uuid).encode('utf-8'),
                           self.position.x, self.position.y,
                           map_item_enum_value[self.item_type.value])

        return data

    def from_bin(self, data: bytes):
        format_string = '16s3i'

        map_item_enum_value: Dict[int, EnumMapItem] = {
            0: EnumMapItem.NotSet,
            1: EnumMapItem.Fruit,
            2: EnumMapItem.Forrest,
        }

        unpacked_data = struct.unpack(format_string, data)
        self.uuid = unpacked_data[0].decode('utf-8')
        self.position = Vector2D(unpacked_data[1], unpacked_data[2])
        self.item_type = map_item_enum_value[npacked_data[3]]
