from enum import Enum
import pygame

MAP_WIDTH, MAP_HEIGHT = 1000, 1000

class EnumPlayerTurns(Enum):
    NONE = 'none'
    LEFT = 'left'
    RIGHT = 'right'
    FIRE = 'fire'
    SAVE = 'save'
    EXIT = 'exit'
    
# valid