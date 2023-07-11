from collections import OrderedDict
from typing import List
from controllers.interfaces.IControllerActor import IControllerActor

class CollectionActorControllers:
    def __init__(
            self,
            actor_controllers: List[IControllerActor],
    ):
        super().__init__()
        self.actor_controllers = actor_controllers
        self.actor_groups = OrderedDict()
        self.actor_groups_keys = []
        self.idx = 0

    def __len__(self): # len(inst)
        return len(self.actor_groups_keys)

    def __iter__(self): # enter for loop
        self.idx = 0
        self.actor_groups.clear()
        for actor_cont in self.actor_controllers:
            tribe = actor_cont.actor.tribe
            if tribe not in self.actor_groups:
                self.actor_groups[tribe] = []
            self.actor_groups[tribe].append(actor_cont)
        self.actor_groups_keys = list(self.actor_groups.keys()) # iter => list
        return self

    def __next__(self): # on each for loop
        if self.idx >= len(self.actor_groups_keys):
            raise StopIteration()
        tribe = self.actor_groups_keys[self.idx]
        actors = self.actor_groups[tribe]
        self.idx += 1
        return tribe, actors