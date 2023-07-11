from abc import ABC, abstractmethod

class IComponent(ABC):
    @abstractmethod
    def generate_transparent_button_surface():
        pass

    @abstractmethod
    def generate_button_surface():
        pass

    @abstractmethod
    def draw():
        pass

    @abstractmethod
    def trigger_mouse() -> bool:
        pass

    @abstractmethod
    def add_listener_click():
        pass

    @abstractmethod
    def remove_listener_click():
        pass