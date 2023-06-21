from models.enums.EnumTribe import EnumTribe

from typing import List


class CollectionTribes:
    def __init__(self, data: List[EnumTribe]):
        self.data: List[EnumTribe] = data
        self.index = 0

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index >= len(self.data):
            self.index = 0
        value = self.data[self.index]
        self.index += 1
        return value





