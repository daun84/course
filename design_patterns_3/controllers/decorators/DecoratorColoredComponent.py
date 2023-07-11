from views.components.interfaces.IComponent import IComponent

from typing import Tuple
import pygame

class DecoratorColoredComponent(IComponent):
    def __init__(
                self,
                component_button: IComponent, 
                up_color_background: Tuple[int, int, int] = None,
                up_color_font: Tuple[int, int, int] = None,
                over_color_background: Tuple[int, int, int] = None,
                over_color_font: Tuple[int, int, int] = None,
                down_color_background: Tuple[int, int, int] = None,
                down_color_font: Tuple[int, int, int] = None,
                trans_over_background: Tuple[int, int, int, int] = None,
                trans_over_border: Tuple[int, int, int, int] = None,
                trans_down_background: Tuple[int, int, int, int] = None,
                trans_down_border: Tuple[int, int, int, int] = None):
        self.__component_button = component_button
        self.linked_enum = component_button.linked_enum
        self.linked_item = component_button.linked_item

        if up_color_background is not None:
            self.__component_button.up_color_background = up_color_background
        if up_color_font is not None:
            self.__component_button.up_color_font = up_color_font
            
        if over_color_background is not None:
            self.__component_button.over_color_background = over_color_background
        if over_color_font is not None:
            self.__component_button.over_color_font = over_color_font
        
        if down_color_background is not None:
            self.__component_button.down_color_background = down_color_background
        if down_color_font is not None:
            self.__component_button.down_color_font = down_color_font

        if trans_over_background is not None:
            self.__component_button.trans_over_background = trans_over_background
        if trans_over_border is not None:
            self.__component_button.trans_over_border = trans_over_border

        if trans_down_background is not None:
            self.__component_button.trans_down_background = trans_down_background
        if trans_over_border is not None:
            self.__component_button.trans_down_border = trans_down_border

        if not self.__component_button.is_transparent:
            self.__component_button.button_up = self.generate_button_surface(
                color_background=self.__component_button.up_color_background,
                color_font=self.__component_button.up_color_font
            )
            self.__component_button.button_over = self.generate_button_surface(
                color_background=self.__component_button.over_color_background,
                color_font=self.__component_button.over_color_font
            )
            self.__component_button.button_down = self.generate_button_surface(
                color_background=self.__component_button.down_color_background,
                color_font=self.__component_button.down_color_font
            )
        else:
            self.__component_button.button_up = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            self.__component_button.button_over = self.generate_transparent_button_surface(
                color_background=self.__component_button.trans_over_background,
                color_border=self.__component_button.trans_over_border
            )
            self.__component_button.button_down = self.generate_transparent_button_surface(
                color_background=self.__component_button.trans_down_background,
                color_border=self.__component_button.trans_down_border
            )
        
    def generate_button_surface(self, color_background, color_font):
        return self.__component_button.generate_button_surface(color_background, color_font)
        
    def generate_transparent_button_surface(self, color_background, color_font):
        return self.__component_button.generate_transparent_button_surface(color_background, color_font)

    def draw(self, surface: pygame.Surface):
        self.__component_button.draw(surface)

    def trigger_mouse(self, mouse_position, mouse_buttons) -> bool:
        return self.__component_button.trigger_mouse(mouse_position, mouse_buttons)

    def add_listener_click(self, func_on_click):
        self.__component_button.add_listener_click(func_on_click)

    def remove_listener_click(self, func_on_click):
        self.__component_button.remove_listener_click(func_on_click)