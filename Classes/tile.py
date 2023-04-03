import os
from typing import Dict, Union

import pygame
from pygame import Color, Surface, Vector2

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

        self.light_level: int = 128
        self.light_emission: int = 0

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def destroy(self) -> Union[str, None]:
        if self.hardness == float("inf"):
            return

        self.texture = self._generate_mined_texture()
        self.can_collide = False
        self.hardness = float("inf")
    
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

        self.light_level = 255
        self.light_emission = 255

    def update(self, position: Vector2) -> None:
        pass

    def destroy(self) -> None:
        pass


class Cave(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        super().__init__(texture=texture, hardness=float("inf"), can_collide=False)
        self.texture = self._generate_mined_texture()


class PropTile(Tile):
    def __init__(self, texture: Union[Surface, str], background_texture: Union[Surface, str, None] = None) -> None:
        
        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)

        if background_texture is not None:
            background_texture = textures[background_texture] if isinstance(background_texture, str) else background_texture
            surface.blit(background_texture, (0, 0))

        texture = textures[texture] if isinstance(texture, str) else texture
        surface.blit(texture, (0, 0))

        super().__init__(texture=surface, hardness=float("inf"), can_collide=False)


class Scaffolding(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        texture = texture.copy().convert_alpha()
        texture.set_colorkey((0, 0, 0))

        scaffolding_texture = textures["scaffolding"]

        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(scaffolding_texture, (0, 0))

        super().__init__(texture=surface, hardness=float("inf"))

    def destroy(self) -> None:
        pass