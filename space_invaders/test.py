from models.enums.EnumObjectType import EnumObjectType
from models.GameObject import GameObject
from models.Vector2D import Vector2D

from controllers.GameSerializationController import GameSerializationController


test = GameSerializationController.instance()

data = test.create_new_game()

test.transfer_data_to_bin("starting_position.bin", data)
