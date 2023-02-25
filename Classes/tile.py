from random import choice
from typing import Union
import pygame, os

textures = {}
for file in os.listdir("{}\Images\Tiles".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Images\Tiles\{}".format(os.getcwd(), file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))
        
        textures[file_name] = image

class Tile:
    def __init__(self, type: str, texture: Union[pygame.Surface, str], can_collide: bool = True, drops: list = None) -> None:
        self.type = type
        self.texture = textures[texture] if isinstance(texture, str) else texture
        self.can_collide = can_collide

        if drops is None:
            self.drops = []

    def mine(self) -> Union[str, None]:
        return choice(self.drops) if len(self.drops) > 0 else None

class Scaffolding(Tile):
    def __init__(self, type: str, texture: Union[pygame.Surface, str]) -> None:
        surface = pygame.surface.Surface((32, 32))
        surface.fill(pygame.Color(77, 165, 217))
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(textures["scaffolding"], (0, 0))

        super().__init__(type, surface)