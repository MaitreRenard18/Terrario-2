import os
from typing import Dict

import pygame
from pygame import Surface, transform

def import_textures(path: str, scale: tuple):
    textures: Dict[str, Surface] = {}
    _textures_path = os.path.join("Images", path)
    for file in os.listdir(_textures_path):
        if file.endswith(".png"):
            file_name = file.replace(".png", "").lower()

            path = os.path.join(_textures_path, file)
            image = transform.scale(pygame.image.load(path), scale)
            textures[file_name] = image
    return textures