import os
from typing import Dict, Union

import pygame
from pygame import Surface, transform, Vector2

from pathlib import Path
MODULE_PATH = Path(__file__).parent.parent


def import_textures(path: str, size: Union[Vector2, tuple]):
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


def import_animated_textures(path: str, size: Union[Vector2, tuple]):
    _textures_path = MODULE_PATH / "Images" / path

    x, y = (size.x, size.y) if isinstance(size, Vector2) else (size[0], size[1])
    if path.endswith(".png"):
        image = pygame.image.load(_textures_path)
        image = pygame.transform.scale(image, (image.get_width() * (size[0] // image.get_width()),
                                               image.get_height() * (size[0] // image.get_width())))

        return [image.subsurface((0, i * y, 32, 32)) for i in range(image.get_height() // y)]
