from models.GameData import GameData
from models.constants import ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_SPEED, WALL_HEIGHT, WALL_WIDTH
from models.GameObject import GameObject
from models.enums.EnumObjectType import EnumObjectType
from models.Vector2D import Vector2D

import pickle

def main():
    starting_position = GameData()
    for i in range(2):
        for j in range(10): 
            starting_position.objects.append(
                GameObject(
                    EnumObjectType.Alien,
                    Vector2D(j * 70 + 10, i * 70 + 100),
                    ALIEN_WIDTH,
                    ALIEN_HEIGHT,
                    "invader1",
                    ALIEN_SPEED,
                    Vector2D(1, 0)
                    ))
    for i in range(2):
        for j in range(10):
            starting_position.objects.append(
                GameObject(
                    EnumObjectType.Alien,
                    Vector2D(j * 70 + 10, i * 70 + 240),
                    ALIEN_WIDTH,
                    ALIEN_HEIGHT,
                    "invader2",
                    ALIEN_SPEED,
                    Vector2D(1, 0)
                    ))
    for i in range(2):
        for j in range(10):
            starting_position.objects.append(
                GameObject(
                    EnumObjectType.Alien,
                    Vector2D(j * 70 + 10, i * 70 + 380),
                    ALIEN_WIDTH,
                    ALIEN_HEIGHT,
                    "invader3",
                    ALIEN_SPEED,
                    Vector2D(1, 0)
                    ))
    for i in range(2):
        for j in range(4):
            for k in range(5):
                starting_position.objects.append(
                GameObject(
                    EnumObjectType.Wall,
                    Vector2D(225 * j + 100 + k * 25, 800 + i * 25),
                    WALL_WIDTH,
                    WALL_HEIGHT,
                    "wall",
                    0,
                    Vector2D(0, 0)
                    ))
    for j in range(4):
        for k in range(2):
            starting_position.objects.append(
                GameObject(
                    EnumObjectType.Wall,
                    Vector2D(225 * j + 100 + k * 100, 850),
                    WALL_WIDTH,
                    WALL_HEIGHT,
                    "wall",
                    0,
                    Vector2D(0, 0)
                    ))
    with open("saves/starting_position.pickle", "wb") as file:
        pickle.dump(starting_position, file)

if __name__ == '__main__':
    main()