from typing import Tuple

import pygame
from pygame import Surface
import time


class UtilsPyGame:
    @staticmethod
    def load_image_and_resize(path: str, size: Tuple[int, int]) -> Surface:
        return pygame.transform.scale(pygame.image.load(path), size)

    @staticmethod
    def timer_decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            end_time = time.time()
            execution_time = end_time - start_time
            print(f"Execution time of '{func.__name__}': {execution_time:.6f} seconds")
            return result
        return wrapper