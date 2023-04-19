import os
from typing import Dict

import pygame
from pygame import Surface, transform

from pathlib import Path
MODULE_PATH = Path(__file__).parent.parent

def load_textures(path: str, scale: tuple):
    textures: Dict[str, Surface] = {}
    _textures_path = MODULE_PATH / "Images" / path
    if path.endswith(".png"):
        image = pygame.transform.scale(pygame.image.load(_textures_path), scale)
        return image 
    for file in os.listdir(_textures_path):
        if file.endswith(".png"):
            file_name = file.replace(".png", "").lower()

            path = os.path.join(_textures_path, file)
            image = pygame.transform.scale(pygame.image.load(path), scale)
            textures[file_name] = image
    return textures
