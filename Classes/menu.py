from random import choice
from typing import Dict
from time import sleep

import sys

import pygame
from pygame import Surface, display

from .button import Button
from .saving import get_saves, save, load
from .textures import load_textures

background_textures = load_textures("Screenshots", (1920, 1080))
logo_texture = load_textures("UI/logo.png", (970, 116))
button_textures: Dict[str, Surface] = load_textures("Button", (360, 108))
x_mark_textures: Dict[str, Surface] = load_textures("Button", (56, 56))

class Menu():

    def __init__(self, map) -> None:

        self.map = map

        self.displayed: bool = True
        self.main: bool = True

        self.save_number = len(get_saves()) + 1
        self.save_name = "World " + str(self.save_number)

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

        self.update_world_buttons()

    def display_background(self) -> None:
        
        self.screen.blit(self.background, (0,0))
        self.screen.blit(self.logo, ((self.screen.get_width() - self.logo.get_width()) // 2, 100))

    def play(self) -> None:
        self.main = not self.main
        sleep(0.1)

    def quit(self) -> None:
        save(self.save_name, self.map)
        pygame.quit()
        sys.exit()

    def launch_world(self, world) -> None:
        self.displayed = False
        self.save_name = world
        load(world)

    def create_new_world(self) -> None:
        self.displayed = False
    
    def update_world_buttons(self) -> None:
        element = -1
        for world in get_saves():
            self.saves_buttons[str(world) + "_button"] = Button(
                button_textures["p_button"].get_rect(center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + element * 150)),
                button_textures["p_button"], button_textures["button_hovered"], world, 32, self.launch_world, world)
            element += 1
