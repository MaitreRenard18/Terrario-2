from random import choice
from time import sleep

import sys
import os

import pygame
from pygame import Surface

from .button import Button
from .saving import get_saves, save, load
from .textures import background_textures, thumbnails_textures, logo_texture, button_textures, world_textures, delete_textures, x_mark_textures
from .constants import screen, MODULE_PATH


class Menu():

    def __init__(self, map) -> None:

        self.map = map

        self.displayed: bool = True
        self.main: bool = True

        self.save_number = len(get_saves()) + 1
        self.save_name = "World " + str(self.save_number)
        self.delete = False

        self.background: Surface = choice(list(background_textures.values()))
        self.logo: Surface = logo_texture

        self.play_button =  Button(button_textures["p_button"].get_rect(center = (screen.get_width() // 2, screen.get_height() // 2)),
                                    button_textures["p_button"], button_textures["button_hovered"], "Play", 48, self.play)
        
        self.quit_button = Button(x_mark_textures["x_mark"].get_rect(center = (screen.get_width() - 40, 40)),
                                    x_mark_textures["x_mark"], x_mark_textures["x_mark_hovered"], "", 0, self.quit)
        
        self.world_buttons = {"create_world_button": Button(button_textures["p_button"].get_rect(center = (screen.get_width() // 2 - 200, screen.get_height() // 2 + 400)),
                                            button_textures["p_button"], button_textures["button_hovered"], "New world", 32, self.create_new_world),
                            "cancel_button": Button(button_textures["p_button"].get_rect(center = (screen.get_width() // 2 + 200, screen.get_height() // 2 + 400)),
                                            button_textures["p_button"], button_textures["button_hovered"], "Cancel", 32, self.play),}
        
        self.saves_buttons = {}
    
    def play(self) -> None:
        self.main = not self.main
        sleep(0.1)

    def quit(self) -> None:
        if not self.displayed:
            save(self.save_name, self.map)
        pygame.quit()
        sys.exit()

    def launch_world(self, world) -> None:
        self.displayed = False
        self.save_name = world
        self.map = load(self.save_name)

    def create_new_world(self) -> None:
        if self.save_number > 3:
            return
        self.displayed = False

    def delete_save(self, world) -> None:
        delete_save = MODULE_PATH / "Saves" / world
        del self.saves_buttons[world + "_button"]
        del self.saves_buttons[world + "_delete_button"]
        os.remove(delete_save)
        self.delete = True
        sleep(0.1)

    def update(self, event) -> None:
        screen.blit(self.background, (0,0))
        screen.blit(self.logo, ((screen.get_width() - self.logo.get_width()) // 2, 100))

        self.save_number = len(get_saves()) + 1

        if not self.main:
            element = -1
            for world in get_saves():
                if str(world) + "_button" not in self.saves_buttons:
                    self.saves_buttons[str(world) + "_button"] = Button(
                        world_textures["world_button"].get_rect(center = (screen.get_width() // 2, screen.get_height() // 2 + element * 150)),
                        world_textures["world_button"], world_textures["world_button_hovered"], "    " + world, 32, self.launch_world, world)
                    self.saves_buttons[str(world) + "_delete_button"] = Button(
                        delete_textures["delete_button"].get_rect(center = (screen.get_width() // 2 + 300, screen.get_height() // 2 + element * 150)),
                        delete_textures["delete_button"], delete_textures["delete_button_hovered"], "", 0, self.delete_save, world)
            
                if len(thumbnails_textures) >= 1:
                    screen.blit(thumbnails_textures[str(world).lower()], ((screen.get_width() - thumbnails_textures[str(world).lower()].get_width()) // 2 - 156, 
                                                                               (screen.get_height() - thumbnails_textures[str(world).lower()].get_height()) // 2 + 146 * element))
                    
                    element += 1

            for save in self.saves_buttons:
                self.saves_buttons[save].check_event(event)
                if self.delete:
                    self.delete = False
                    break
                
            for button in self.world_buttons:
                self.world_buttons[button].check_event(event)

        else:
            self.play_button.check_event(event)
