from abc import ABC, abstractmethod

class BaseState(ABC):
    def __init__(self, entity):
        self.state_name = self.__class__.__name__.lower()
        self.animation_loop = True
        entity.frame_index = 0

    def state_logic(self, entity):
        pass

    def update(self, dt, entity):
        pass