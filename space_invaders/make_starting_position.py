from models.GameData import GameData
from models.Alien import Alien
from models.Wall import Wall
from models.Vector2D import Vector2D

import pickle

def main():
    starting_position = GameData()
    for i in range(2):
        for j in range(10):
            starting_position.objects.append(
                Alien(position=Vector2D(x=j * 70, y=i * 70 + 100), name="invader1"))
    for i in range(2):
        for j in range(10):
            starting_position.objects.append(
                Alien(position=Vector2D(x=j * 70, y=i * 70 + 240), name="invader2"))
    for i in range(2):
        for j in range(10):
            starting_position.objects.append(
                Alien(position=Vector2D(x=j * 70, y=i * 70 + 380), name="invader3"))
    for i in range(2):
        for j in range(4):
            for k in range(5):
                starting_position.objects.append(
                    Wall(position=Vector2D(x=225 * j + 100 + k * 25, y=800 + i * 25)))
    for j in range(4):
        for k in range(2):
            starting_position.objects.append(
                Wall(position=Vector2D(x=225 * j + 100 + k * 100,y= 850)))
    with open("saves/starting_position.pickle", "wb") as file:
        pickle.dump(starting_position, file)

if __name__ == '__main__':
    main()