from models.Actor import Actor
from models.Game import Game
from models.MapTile import MapTile
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumMapTile import EnumMapTile
from models.MapBuilding import MapBuilding

class ControllerSerialization:
    def __init__(self):
        pass

    @staticmethod
    def write_data_to_bin_file(file_name: str, data: Game):
        pass

    @staticmethod 
    def read_data_from_bin_file(file_name: str) -> Game:
        pass