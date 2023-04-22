import os
from typing import Dict, Union

import pygame
from pygame import Surface, transform, Vector2

from pathlib import Path
MODULE_PATH = Path(__file__).parent.parent


def load_textures(path: str, size: Union[Vector2, tuple]):
    _textures_path = MODULE_PATH / "Images" / path

    if path.endswith(".png"):
        image = pygame.transform.scale(pygame.image.load(_textures_path), size)
        return image

    textures: Dict[str, Surface] = {}
    for file in os.listdir(_textures_path):
        if file.endswith(".png"):
            file_name = file.replace(".png", "").lower()

            path = os.path.join(_textures_path, file)
            image = pygame.transform.scale(pygame.image.load(path), size)
            textures[file_name] = image

    return textures


def load_animated_textures(path: str, size: Union[Vector2, tuple]):
    _textures_path = MODULE_PATH / "Images" / path

    x, y = (size.x, size.y) if isinstance(size, Vector2) else (size[0], size[1])
    if path.endswith(".png"):
        image = pygame.image.load(_textures_path)
        image = pygame.transform.scale(image, (image.get_width() * (size[0] // image.get_width()),
                                               image.get_height() * (size[0] // image.get_width())))

        return [image.subsurface((0, i * y, 32, 32)) for i in range(image.get_height() // y)]
    
    
# Charge les textures concernant le menu et les différents boutons.
logo_texture: Surface = load_textures("UI/logo.png", (970, 116))
background_textures: Dict[str, Surface] = load_textures("Screenshots", (1920, 1080))
thumbnails_textures: Dict[str, Surface] = load_textures("Thumbnails", (125, 125))
button_textures: Dict[str, Surface] = {"p_button": load_textures("Button/p_button.png", (360, 108)),
                                       "up_button": load_textures("Button/up_button.png", (360, 108)),
                                       "button_hovered": load_textures("Button/button_hovered.png", (360, 108)),}
world_textures: Dict[str, Surface] = {"world_button": load_textures("Button/world_button.png", (450, 135)),
                                      "world_button_hovered": load_textures("Button/world_button_hovered.png", (450, 135))}
delete_textures: Dict[str, Surface] = {"delete_button": load_textures("Button/delete_button.png", (135, 135)),
                                      "delete_button_hovered": load_textures("Button/delete_button_hovered.png", (135, 135))}
x_mark_textures: Dict[str, Surface] = {"x_mark": load_textures("Button/x_mark.png", (56, 56)),
                                      "x_mark_hovered": load_textures("Button/x_mark_hovered.png", (56, 56))}

# Charge les textures concernant le joueur, les minerais, l'inventaire et l'interface de craft.
player_textures: Dict[str, Surface] = load_textures("Player", (32, 32))
ores_textures: Dict[str, Surface] = load_textures("Ores", (96, 96))
inventory_texture: Surface = load_textures("UI/inventory.png", (942, 462))
craft_interface_texture: Surface = load_textures("UI/craft_interface.png", (840, 390))
drilltip_textures: Dict[str, Surface] = {}
for level in range(1, 9):
    drilltip_textures["drilltip_right_" + str(level)] = load_textures("Player/drilltip_right_" + str(level) + ".png", (192, 192))
    
# Charge les textures concernant les tiles qui composent la map.
tiles_textures = load_textures("Tiles", (32, 32))
