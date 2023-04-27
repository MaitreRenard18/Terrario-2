from random import choice
from time import sleep
from typing import Dict

import sys
import os

import pygame
from pygame import Surface

from .button import Button
from .saving import get_saves, save, load
from .textures import background_textures, thumbnails_textures, logo_texture, button_textures, world_textures, \
    delete_textures, x_mark_textures
from .constants import screen, MODULE_PATH


# Déclaration de la classe Menu
class Menu:
    """
    Class qui représente le menu
    """

    def __init__(self, map):
        """
        Initialise le menu
        Prend en paramètre une map, qui correspond au monde chargé
        """

        self.map = map

        self.displayed: bool = True
        self.main: bool = True

        self.save_number: int = len(get_saves()) + 1
        self.save_name: str = "world_" + str(self.save_number)
        self.delete: bool = False

        self.background: Surface = choice(list(background_textures.values()))
        self.logo: Surface = logo_texture

        self.play_button: Button = Button(button_textures["p_button"].get_rect(center=(screen.get_width() // 2,
                                                                                       screen.get_height() // 2)),
                                          button_textures["p_button"], button_textures["button_hovered"], "Play", 48,
                                          self.play)

        self.quit_button: Button = Button(x_mark_textures["x_mark"].get_rect(center=(screen.get_width() - 40, 40)),
                                          x_mark_textures["x_mark"], x_mark_textures["x_mark_hovered"], "", 0,
                                          self.quit)

        self.world_buttons: Dict[str, Button] = {
            "create_world_button": Button(button_textures["p_button"].get_rect(center=(screen.get_width() // 2 - 200,
                                                                                       screen.get_height() // 2 + screen.get_height() // 3)),
                                          button_textures["p_button"], button_textures["button_hovered"], "New world",
                                          32, self.create_new_world),
            "cancel_button": Button(button_textures["p_button"].get_rect(center=(screen.get_width() // 2 + 200,
                                                                                 screen.get_height() // 2 + screen.get_height() // 3)),
                                    button_textures["p_button"], button_textures["button_hovered"], "Cancel", 32,
                                    self.play), }

        self.saves_buttons: Dict[str, Button] = {}

    def play(self) -> None:
        """
        Lance le menu pour charger un monde
        """

        self.main = not self.main
        sleep(0.1)

    def quit(self) -> None:
        """
        Ferme le jeu, et sauvegarde la progression du joueur et l'état de la map
        """

        if not self.displayed:
            save(self.save_name, self.map)
        pygame.quit()
        sys.exit()

    def launch_world(self, world: str) -> None:
        """
        Charge un monde et l'affiche
        """

        self.displayed = False
        self.save_name = world
        self.map = load(self.save_name)

    def create_new_world(self) -> None:
        """
        Ferme le menu et charge le monde crée par défaut
        S'il y a déjà 3 sauvegardes, aucun monde ne sera crée
        """

        if self.save_number > 3:
            return
        self.displayed = False

    def delete_save(self, world) -> None:
        """
        Supprime une sauvegarde
        """

        delete_save: str = MODULE_PATH / "saves" / world
        del self.saves_buttons[world + "_button"]
        del self.saves_buttons[world + "_delete_button"]
        os.remove(delete_save)
        self.delete = True
        sleep(0.1)

    def update(self, event: pygame.event) -> None:
        """
        Affiche l'arrière-plan et le logo du jeu
        Affiche les différents boutons se trouvant dans le menu
        Vérifie que les boutons soient cliqués ou pointés
        """

        screen.blit(self.background, (0, 0))
        screen.blit(self.logo, ((screen.get_width() - self.logo.get_width()) // 2, 100))

        self.save_number = len(get_saves()) + 1

        if not self.main:
            element: int = -1
            for world in get_saves():
                if str(world) + "_button" not in self.saves_buttons:
                    self.saves_buttons[str(world) + "_button"] = Button(
                        world_textures["world_button"].get_rect(
                            center=(screen.get_width() // 2, screen.get_height() // 2 + element * 150)),
                        world_textures["world_button"], world_textures["world_button_hovered"],
                        "    " + world.replace("_", " "), 32, self.launch_world, world)
                    self.saves_buttons[str(world) + "_delete_button"] = Button(
                        delete_textures["delete_button"].get_rect(
                            center=(screen.get_width() // 2 + 300, screen.get_height() // 2 + element * 150)),
                        delete_textures["delete_button"], delete_textures["delete_button_hovered"], "", 0,
                        self.delete_save, world)

                if len(thumbnails_textures) >= 1:
                    screen.blit(thumbnails_textures[str(world).lower()],
                                ((screen.get_width() - thumbnails_textures[str(world).lower()].get_width()) // 2 - 156,
                                 (screen.get_height() - thumbnails_textures[
                                     str(world).lower()].get_height()) // 2 + 148 * element))

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
