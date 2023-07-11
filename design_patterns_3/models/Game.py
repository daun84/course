from dataclasses import field
from dataclasses import dataclass
from typing import List

from dataclasses_json import dataclass_json

from models.Actor import Actor, ACTOR_BYTE_COUNT
from models.MapBuilding import MapBuilding, MAP_BUILDING_BYTE_COUNT
from models.MapItem import MapItem, MAP_ITEM_BYTE_COUNT
from models.MapTile import MapTile, MAP_TILE_BYTE_COUNT
from models.Vector2D import Vector2D 
from models.enums.EnumTribe import EnumTribe

import struct


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

    turn: int = 1
    stars: int = 0

    player_tribe = EnumTribe.Imperius
    turn_tribe = EnumTribe.Imperius

    def to_bin(self):
        data: bytes = b''
        game_variables_format_string = "4i2f4i"

        tribe_enum_values: Dict[EnumTribe, int] = {
            EnumTribe.NotSet: 0,
            EnumTribe.Imperius: 1,
            EnumTribe.Hoodrick: 2
        }

        data += struct.pack('i', 1) # game_variables

        data += struct.pack(game_variables_format_string,
                            self.map_size.x, self.map_size.y,
                            self.window_size.x, self.window_size.y,
                            self.window_location.x, self.window_location.y,
                            self.turn, self.stars, 
                            tribe_enum_values[self.player_tribe],
                            tribe_enum_values[self.turn_tribe])

        data += struct.pack('i', 2) # map_tiles
        column_length = len(self.map_tiles)
        row_length = len(self.map_tiles[0])
        data += struct.pack('2i', column_length, row_length)
        for map_tiles in self.map_tiles:
            for map_tile in map_tiles:
                data += map_tile.to_bin()

        data += struct.pack('i', 3) # items
        length = len(self.items)
        data += struct.pack('i', length)
        for item in self.items:
            data += item.to_bin()

        data += struct.pack('i', 4) # buildings
        length = len(self.buildings)
        data += struct.pack('i', length)
        for building in self.buildings:
            data += building.to_bin()

        data += struct.pack('i', 5) # actors
        length = len(self.actors)
        data += struct.pack('i', length)
        for actor in self.actors:
            data += actor.to_bin()

        return data    


    def from_bin_file(self, file_name: str):
        with open(file_name, 'rb') as f:
            game_variables_format_string = "4i2f4i"

            tribe_enum_values: Dict[int, EnumTribe] = {
                0: EnumTribe.NotSet,
                1: EnumTribe.Imperius,
                2: EnumTribe.Hoodrick
            }

            # clearing containers

            self.map_tiles = [[]]
            self.items = []
            self.buildings = []
            self.actors = []

            id_raw = f.read(4) # game_variables
            
            unpacked_data_raw = f.read(40)
            unpacked_data = struct.unpack(game_variables_format_string, unpacked_data_raw)
            self.map_size = Vector2D(unpacked_data[0], unpacked_data[1])
            self.window_size = Vector2D(unpacked_data[2], unpacked_data[3])
            self.window_location = Vector2D(unpacked_data[4], unpacked_data[5])
            self.turn = unpacked_data[6]
            self.stars = unpacked_data[7]
            self.player_tribe = tribe_enum_values[unpacked_data[8]]
            self.turn_tribe = tribe_enum_values[unpacked_data[9]]

            id_raw = f.read(4) # map_tiles
            lengths_raw = f.read(8)
            column_length, row_length = struct.unpack('2i', lengths_raw)
            for i in range(column_length):
                self.map_tiles.append([])
                for j in range(row_length):
                    map_tile_data_raw = f.read(MAP_TILE_BYTE_COUNT)
                    map_tile = MapTile()
                    map_tile.from_bin(map_tile_data_raw)
                    self.map_tiles[i].append(map_tile)

            id_raw = f.read(4) # items
            lengths_raw = f.read(4)
            length, = struct.unpack('i', lengths_raw)
            for i in range(length):
                map_item_raw = f.read(MAP_ITEM_BYTE_COUNT)
                map_item = MapItem()
                map_item.from_bin(map_item_raw)
                self.items.append(map_item)

            
            id_raw = f.read(4) # buildings
            lengths_raw = f.read(4)
            length, = struct.unpack('i', lengths_raw)
            for i in range(length):
                map_building_raw = f.read(MAP_BUILDING_BYTE_COUNT)
                map_building = MapBuilding() 
                map_building.from_bin(map_building_raw)
                self.buildings.append(map_building)

            id_raw = f.read(4) # actors
            lengths_raw = f.read(4)
            length, = struct.unpack('i', lengths_raw)
            for i in range(length):
                actor_raw = f.read(ACTOR_BYTE_COUNT)
                actor = Actor()
                actor.from_bin(actor_raw)
                self.actors.append(actor)