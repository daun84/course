from models.Actor import Actor
from models.MapBuilding import MapBuilding
from models.enums.EnumTribe import EnumTribe

from views.resources.interfaces.IResourceFactory import IResourceFactory
from views.resources.ResourcesHoodrick import ResourcesHoodrick
from views.resources.ResourcesImperius import ResourcesImperius

from collections import OrderedDict
from typing import List

class CollectionObjectSurface:
    def __init__(
            self,
            actors: List[Actor],
            buildings: List[MapBuilding]
    ):
        super().__init__()
        self.actors = actors
        self.buildings = buildings
        self.objects: list = []
        self.index: int = 0
        self.resources_by_tribe: Dict[EnumTribe, IResourceFactory] = {
            EnumTribe.Imperius: ResourcesImperius(),
            EnumTribe.Hoodrick: ResourcesHoodrick(),
        }

    def __len__(self):
        return len(self.objects)

    def __iter__(self):
        self.index = 0
        self.buildings = sorted(self.buildings, key=lambda obj: (obj.position.y, obj.position.x))
        self.actors = sorted(self.actors, key=lambda obj: (obj.position.y, obj.position.x))
        self.objects = self.buildings + self.actors
        return self

    def __next__(self):
        if self.index >= len(self):
            raise StopIteration()
        item = self.objects[self.index]
        #print(type(item))
        #print(item.position.y, item.position.x)
        if type(item) is MapBuilding:
            item_surface = self.resources_by_tribe[item.tribe].get_building(
                item.building_type,
                item.level
            )
        else:
            item_surface = self.resources_by_tribe[item.tribe].get_actor(
                enum_actor=item.actor_type,
            )
        self.index += 1
        return item, item_surface