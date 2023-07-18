import pickle
import struct
import time
import random
from typing import Dict

import pygame
from pygame import Surface, key, Rect

from controllers.ControllerGame import ControllerGame

from controllers.commands.CommandActorMove import CommandActorMove
from controllers.commands.CommandCreateActor import CommandCreateActor
from controllers.commands.ControllerInvoker import ControllerInvoker
from controllers.decorators.DecoratorFasterActor import DecoratorFasterActor
from controllers.decorators.DecoratorColoredComponent import DecoratorColoredComponent

from models.Actor import Actor
from models.Game import Game
from models.Vector2D import Vector2D
from models.enums.EnumActor import EnumActor
from models.enums.EnumBuilding import EnumBuilding
from models.enums.EnumMapTile import EnumMapTile
from models.enums.EnumTribe import EnumTribe

from utils.decorators.decorator_logging import decorator_logging
from utils.decorators.decorator_try_catch import decorator_try_catch
from utils.iterator.CollectionActorControllers import CollectionActorControllers
from utils.UtilsPyGame import UtilsPyGame

from views.components.ComponentButton import ComponentButton
from views.resources.ResourcesHoodrick import ResourcesHoodrick
from views.resources.ResourcesImperius import ResourcesImperius
from views.resources.interfaces.IResourceFactory import IResourceFactory

MAP_MOVEMENT_SPEED = 30

class WindowMain:
    __instance = None

    @staticmethod
    def instance():
        if WindowMain.__instance is None:
            WindowMain.__instance = WindowMain()
        return WindowMain.__instance

    def __init__(self):
        if WindowMain.__instance is not None:
            raise Exception("Only one instance of singleton allowed")
        WindowMain.__instance = self

        pygame.init()

        self.screen = pygame.display.set_mode(
            (550, 500)
        )
        self.is_game_running = True
        self.selected_building = None
        self.selected_actor = None
        self.collection_cont_actors = None

        self.resources_by_tribe: Dict[EnumTribe, IResourceFactory] = {
            EnumTribe.Imperius: ResourcesImperius(),
            EnumTribe.Hoodrick: ResourcesHoodrick(),
        }

        self.surfaces_by_map_tiles: Dict[EnumMapTile, Surface] = {
            EnumMapTile.Ground: pygame.image.load('./resources/Tribes/Imperius/Imperius ground.png'),
            EnumMapTile.Water: pygame.image.load('./resources/Miscellaneous/Shallow water.png')
        }

        self.ui_components = []
        self.ui_actor_buttons = []

        ui_button_new_game = ComponentButton(
            Rect(5, 5, 80, 40),
            'New'
        )
        ui_button_new_game = DecoratorColoredComponent(
                                ui_button_new_game,
                                up_color_background=(255, 0, 0))
        ui_button_new_game.add_listener_click(self.on_click_new_game)
        self.ui_components.append(ui_button_new_game)

        ui_button_save_game = ComponentButton(
            Rect(90, 5, 80, 40),
            'Save'
        )
        ui_button_save_game = DecoratorColoredComponent(
                                ui_button_save_game,
                                up_color_background=(0, 255, 0)
        )
        ui_button_save_game.add_listener_click(self.on_click_save_game)
        self.ui_components.append(ui_button_save_game)

        ui_button_load_game = ComponentButton(
            Rect(175, 5, 80, 40),
            'Load'
        )
        ui_button_load_game = DecoratorColoredComponent(
                                ui_button_load_game,
                                up_color_background=(0, 0, 255)
        )
        ui_button_load_game.add_listener_click(self.on_click_load_game)
        self.ui_components.append(ui_button_load_game)

        ui_button_end_turn = ComponentButton(
            Rect(260, 5, 110, 40),
            'End turn'
        )
        ui_button_end_turn.add_listener_click(self.on_click_end_turn)
        self.ui_components.append(ui_button_end_turn)

        ui_button_undo = ComponentButton(
            Rect(375, 5, 80, 40),
            'Undo'
        )
        ui_button_undo.add_listener_click(self.on_click_undo)
        self.ui_components.append(ui_button_undo)

        ui_button_redo = ComponentButton(
            Rect(460, 5, 80, 40),
            'Redo'
        )
        ui_button_redo.add_listener_click(self.on_click_redo)
        self.ui_components.append(ui_button_redo)

        ui_button_actor = ComponentButton(
            Rect(100, 430, 100, 40),
            'Warrior',
            linked_enum=EnumActor.Warrior,
            is_visible=False
        )
        ui_button_actor.add_listener_click(self.on_click_create_actor)
        self.ui_components.append(ui_button_actor)
        self.ui_actor_buttons.append(ui_button_actor)

        ui_button_actor = ComponentButton(
            Rect(215, 430, 80, 40),
            'Rider',
            linked_enum=EnumActor.Rider,
            is_visible=False
        )
        ui_button_actor.add_listener_click(self.on_click_create_actor)
        self.ui_components.append(ui_button_actor)
        self.ui_actor_buttons.append(ui_button_actor)

        ui_button_actor = ComponentButton(
            Rect(310, 430, 90, 40),
            'Knight',
            linked_enum=EnumActor.Knight,
            is_visible=False
        )
        ui_button_actor.add_listener_click(self.on_click_create_actor)
        self.ui_components.append(ui_button_actor)
        self.ui_actor_buttons.append(ui_button_actor)

        self.new_game()

    def new_game(self):
        self.game = ControllerGame.instance().new_game()
        self.setup_game()

    def setup_game(self):
        # remove buttons that are linked with game elements
        self.ui_components = [it for it in self.ui_components if it.linked_item is None]

    def on_click_save_game(self, button):
        state_bin = self.game.to_bin()
        with open('state.bin', 'wb') as fp:
            fp.write(state_bin)

    def on_click_load_game(self, button):
        ControllerGame.instance().load_game()
        self.setup_game()
        ControllerInvoker.instance().clear_history()

    def on_click_end_turn(self, button):
        if self.game.turn_tribe == EnumTribe.Imperius:
            self.game.turn_tribe = EnumTribe.Hoodrick
        else:
            self.game.turn_tribe = EnumTribe.Imperius

        self.game.turn += 1

    def on_click_undo(self, button):
        ControllerInvoker.instance().undo_command()

    def on_click_redo(self, button):
        ControllerInvoker.instance().redo_command()

    def on_click_new_game(self, button):
        random.seed(time.time())
        self.new_game()

    def on_click_actor(self, button):
        self.selected_actor = button.linked_item

    def on_click_building(self, button):
        self.selected_building = button.linked_item
        if self.selected_building:
            for ui_button in self.ui_actor_buttons:
                ui_button.is_visible = True

    def hide_ui_actor_buttons(self):
        self.selected_building = None
        for command_button in self.ui_components:
            command_button.is_button_toggled = False
        if self.ui_actor_buttons[0].is_visible:
            for ui_button in self.ui_actor_buttons:
                ui_button.is_visible = False

    def on_click_create_actor(self, button: ComponentButton):
        command = CommandCreateActor(self.selected_building, button.linked_enum)
        ControllerInvoker.instance().execute_command(command)
        self.hide_ui_actor_buttons()

    def show(self):
        # main game loop
        time_last = time.time()
        while self.is_game_running:
            self.screen.fill((0, 0, 0))

            # get delta seconds
            time_current = time.time()
            delta_sec = time_current - time_last
            time_last = time_current

            # update
            self.update(delta_sec)

            # draw
            self.draw()

            # update display
            pygame.display.flip()

            time.sleep(0.01)

    @UtilsPyGame.timer_decorator
    def update(self, delta_sec):

        # add ComponentButton over each building
        for building in self.game.buildings:
            if not any(it.linked_item == building for it in self.ui_components):
                ui_button_actor = ComponentButton(
                    rect=Rect(
                        0,
                        0,
                        52,
                        52
                    ),
                    is_transparent=True,
                    linked_item=building,
                    is_toggle_button=True
                )
                self.ui_components.append(ui_button_actor)
                ui_button_actor.add_listener_click(self.on_click_building)

        # add ComponentButton over each actor
        for actor in self.game.actors:
            if not any(it.linked_item == actor for it in self.ui_components):
                ui_button_actor = ComponentButton(
                    rect=Rect(
                        0,
                        20,
                        52,
                        52
                    ),
                    is_transparent=True,
                    linked_item=actor,
                    is_toggle_button=True
                )
                self.ui_components.append(ui_button_actor)
                ui_button_actor.add_listener_click(self.on_click_actor)


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.is_game_running = False

        keys_pressed = key.get_pressed()
        #if any(keys_pressed):
        #    self.hide_ui_actor_buttons()
        if keys_pressed[pygame.K_LEFT]:
            self.game.window_location.x -= MAP_MOVEMENT_SPEED * delta_sec
        if keys_pressed[pygame.K_RIGHT]:
            self.game.window_location.x += MAP_MOVEMENT_SPEED * delta_sec
        if keys_pressed[pygame.K_UP]:
            self.game.window_location.y -= MAP_MOVEMENT_SPEED * delta_sec
        if keys_pressed[pygame.K_DOWN]:
            self.game.window_location.y += MAP_MOVEMENT_SPEED * delta_sec

        self.game.window_location.x = max(0, self.game.window_location.x)
        self.game.window_location.x = min(self.game.map_size.x - self.game.window_size.x - 1,
                                          self.game.window_location.x)
        self.game.window_location.y = max(0, self.game.window_location.y)
        self.game.window_location.y = min(self.game.map_size.y - self.game.window_size.y - 1,
                                          self.game.window_location.y)

        mouse_pos = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        is_clicked = False
        for ui_component in self.ui_components:
            is_clicked = ui_component.trigger_mouse(mouse_pos, mouse_buttons)
            if is_clicked:
                break

        if mouse_buttons[0] and not is_clicked:
            if self.selected_actor:
                pos_mouse = Vector2D(mouse_pos[0] // 52, mouse_pos[1] // 15)
                des_pos = pos_mouse + self.game.window_location
                command = CommandActorMove(self.selected_actor, des_pos)
                ControllerInvoker.instance().execute_command(command)

            self.selected_building = None
            self.selected_actor = None
            self.hide_ui_actor_buttons()
        
        ControllerGame.instance().update_actors(delta_sec)

        for ui_component in self.ui_components:
            if type(ui_component.linked_item) is Actor:
                if not any(ui_component.linked_item == actor for actor in self.game.actors):
                    ui_component.remove_listener_click(self.on_click_actor)
                    self.ui_components.remove(ui_component)
                    

    def draw(self):
        view_x_start = int(self.game.window_location.x)
        view_x_end = view_x_start + self.game.window_size.x + 2
        view_y_start = int(self.game.window_location.y)
        view_y_end = view_y_start + self.game.window_size.y + 2

        # show map edges
        view_i_offset = 0
        if view_x_start > 0:
            view_x_start -= 1
            view_i_offset -= 52
        if view_x_end < self.game.map_size.x:
            view_x_end += 1

        view_j_offset = 0
        if view_y_start > 0:
            view_y_start -= 1
            view_j_offset -= 15
        if view_y_end < self.game.map_size.y:
            view_y_end += 1

        for view_j, j in enumerate(range(view_y_start, view_y_end)):
            for view_i, i in enumerate(range(view_x_start, view_x_end)):
                if j < len(self.game.map_tiles) >= 0 and i < len(self.game.map_tiles[j]) >= 0:
                    map_tile = self.game.map_tiles[j][i]
                    map_tile_type = map_tile.tile_type
                    map_tile_surface = self.surfaces_by_map_tiles[map_tile_type]
                    i_offset = 26 if j % 2 == 1 else 0
                    self.screen.blit(map_tile_surface, (
                        view_i * 52 + i_offset + view_i_offset,
                        view_j * 15 + view_j_offset
                    ))

        for item in (self.game.buildings + self.game.actors):
            if item in self.game.buildings:
                item_surface = self.resources_by_tribe[item.tribe].get_building(
                    item.building_type,
                    item.level
                )
            else:
                item_surface = self.resources_by_tribe[item.tribe].get_actor(
                    enum_actor=item.actor_type,
                )
            i = item.position.x - int(self.game.window_location.x)
            j = item.position.y - int(self.game.window_location.y)
            i_offset = 26 if item.position.y % 2 == 1 else 0
            x = i * 52 + i_offset + view_i_offset
            y = j * 15 + view_j_offset
            self.screen.blit(item_surface, (x, y))

            for ui_component in self.ui_components:
                if ui_component.linked_item == item:
                    ui_component.offset_x = x
                    ui_component.offset_y = y
                    break

        for ui_component in self.ui_components:
            ui_component.draw(self.screen)

        font = pygame.font.SysFont('arial', 16)
        img_font = font.render(f'Turn: {self.game.turn} Stars: {self.game.stars}', True, (255, 255, 255))
        self.screen.blit(img_font, (20, 50))










