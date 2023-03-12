from typing import Union, Dict
import os

import pygame
from pygame import Surface, Vector2, Color


textures: Dict[str, Surface] = {}
_textures_path = os.path.join("Images", "Tiles")
for file in os.listdir(_textures_path):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()

        path = os.path.join(_textures_path, file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))
        textures[file_name] = image


class Tile:
    def __init__(self, texture: Union[Surface, str], hardness: Union[int, float], can_collide: bool = True) -> None:
        self.texture: Surface = textures[texture] if isinstance(texture, str) else texture

        self.can_collide: bool = can_collide
        self.hardness: int = hardness

    def destroy(self) -> Union[str, None]:
        self.can_collide = False
        self.hardness = float("inf")
        self.texture = self._generate_mined_texture()
        self.destroy = lambda: None

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def _generate_mined_texture(self) -> Surface:
        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(0, 0, 0, 64))

        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        return surface


class Air(Tile):
    def __init__(self) -> None:
        super().__init__(texture="air", hardness=float("inf"), can_collide=False)

    def update(self, position: Vector2) -> None:
        pass


class Cave(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        super().__init__(texture=texture, hardness=float("inf"), can_collide=False)
        self.texture = self._generate_mined_texture()

    def destroy(self) -> None:
        pass


class Scaffolding(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        texture.set_colorkey((0, 0, 0))

        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(textures["scaffolding"], (0, 0))

        super().__init__(texture=surface, hardness=float("inf"))

    def destroy(self) -> None:
        pass