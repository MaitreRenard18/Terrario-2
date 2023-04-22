from random import choice
from typing import Dict
from time import sleep

import sys
import os

from pathlib import Path

import pygame
from pygame import Surface, display

from .button import Button
from .saving import get_saves, save, load
from .textures import load_textures

MODULE_PATH = Path(__file__).parent.parent

background_textures: Dict[str, Surface] = load_textures("Screenshots", (1920, 1080))
thumbnails_textures: Dict[str, Surface] = load_textures("Thumbnails", (125, 125))
logo_texture: Surface = load_textures("UI/logo.png", (970, 116))
button_textures: Dict[str, Surface] = {"p_button": load_textures("Button/p_button.png", (360, 108)), 
                                       "button_hovered": load_textures("Button/button_hovered.png", (360, 108))}
world_textures: Dict[str, Surface] = {"world_button": load_textures("Button/world_button.png", (450, 135)),
                                      "world_button_hovered": load_textures("Button/world_button_hovered.png", (450, 135))}
delete_textures: Dict[str, Surface] = {"delete_button": load_textures("Button/delete_button.png", (135, 135)),
                                      "delete_button_hovered": load_textures("Button/delete_button_hovered.png", (135, 135))}
x_mark_textures: Dict[str, Surface] = {"x_mark": load_textures("Button/x_mark.png", (56, 56)),
                                      "x_mark_hovered": load_textures("Button/x_mark_hovered.png", (56, 56))}


class Menu():

    def __init__(self, map) -> None:

        self.map = map

        self.displayed: bool = True
        self.main: bool = True

        self.save_number = len(get_saves()) + 1
        self.save_name = "World " + str(self.save_number)
        self.delete = False

        self.screen: Surface = display.get_surface()
        self.background: Surface = choice(list(background_textures.values()))
        self.logo: Surface = logo_texture

        self.play_button =  Button(button_textures["p_button"].get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2)),
                                    button_textures["p_button"], button_textures["button_hovered"], "Play", 48, self.play)
        
        self.quit_button = Button(x_mark_textures["x_mark"].get_rect(center = (self.screen.get_width() - 40, 40)),
                                    x_mark_textures["x_mark"], x_mark_textures["x_mark_hovered"], "", 0, self.quit)
        
        self.world_buttons = {"create_world_button": Button(button_textures["p_button"].get_rect(center = (self.screen.get_width() // 2 - 200, self.screen.get_height() // 2 + 400)),
                                            button_textures["p_button"], button_textures["button_hovered"], "New world", 32, self.create_new_world),
                            "cancel_button": Button(button_textures["p_button"].get_rect(center = (self.screen.get_width() // 2 + 200, self.screen.get_height() // 2 + 400)),
                                            button_textures["p_button"], button_textures["button_hovered"], "Cancel", 32, self.play),}
        
        self.saves_buttons = {}
        self.update()
    
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

    def update(self) -> None:
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.logo, ((self.screen.get_width() - self.logo.get_width()) // 2, 100))

        self.save_number = len(get_saves()) + 1
        if not self.main:
            element = -1
            for world in get_saves():
                self.saves_buttons[str(world) + "_button"] = Button(
                    world_textures["world_button"].get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + element * 150)),
                    world_textures["world_button"], world_textures["world_button_hovered"], "    " + world, 32, self.launch_world, world)
                self.saves_buttons[str(world) + "_delete_button"] = Button(
                    delete_textures["delete_button"].get_rect(center = (self.screen.get_width() // 2 + 300, self.screen.get_height() // 2 + element * 150)),
                    delete_textures["delete_button"], delete_textures["delete_button_hovered"], "", 0, self.delete_save, world)
            
                if len(thumbnails_textures) >= 1:
                    self.screen.blit(thumbnails_textures[str(world).lower()], ((self.screen.get_width() - thumbnails_textures[str(world).lower()].get_width()) // 2 - 156, 
                                                                               (self.screen.get_height() - thumbnails_textures[str(world).lower()].get_height()) // 2 + 146 * element))
                    element += 1
 
