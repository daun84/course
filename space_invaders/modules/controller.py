from singleton import SingletonMeta
from model import Game, GameData, Alien
from typing import List
from constants import EnumPlayerTurns
import pickle
import pygame
import json
import os 
from datetime import datetime

class Controller(metaclass=SingletonMeta):
    def __init__(self, model):
        self.__model: Game = model

    def save_game(self):
        data = self.__model.get_data()
        name = f'{datetime.now().strftime("%H:%M:%S")}.pickle'
        with open(os.path.join('../saves', name), "wb") as file:
            pickle.dump(data, file)

    def load_game(self, name: str):
        with open(os.path.join('../saves', name), "rb") as file:
            position = pickle.load(file)
        self.__model.initialize_position(position)

    def update_model(self, turn: List[EnumPlayerTurns]) -> GameData:
        self.__model.update(turn)
        return self.__model.get_data()
