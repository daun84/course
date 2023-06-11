from model import GameData, Alien, Wall
import pickle

starting_position = GameData()
for i in range(6):
    for j in range(10):
        starting_position.objects.append(Alien(j * 70, i * 70 + 100, "invader"))

for i in range(2):
    for j in range(4):
        for k in range(5):
            starting_position.objects.append(Wall(225 * j + 100 + k * 25, 800 + i * 25))
for j in range(4):
    for k in range(2):
        starting_position.objects.append(Wall(225 * j + 100 + k * 100, 850))


with open("starting_position.pickle", "wb") as file:
    pickle.dump(starting_position, file)
