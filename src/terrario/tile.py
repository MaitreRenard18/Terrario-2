import os
from typing import Dict, Union

import pygame
from pygame import Color, Surface, Vector2

from pathlib import Path
MODULE_PATH = Path(__file__).parent

textures: Dict[str, Surface] = {}
_textures_path = MODULE_PATH / "Images" / "Tiles"
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

    def update(self, position: Vector2) -> None:
        pass

    def destroy(self) -> None:
        pass


class Background(Air):
    def __init__(self, texture: Union[Surface, str], depth: float = 0.5) -> None:
        super().__init__()

        self.depth: float = depth

        self.texture: Surface = textures[texture] if isinstance(texture, str) else texture
        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(77, 165, 217, int(255 * depth)))
        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture = surface.convert()

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        display.blit(self.texture, position)


class Cave(Tile):
    def __init__(self, texture: Union[Surface, str], depth: float = 0.5) -> None:
        super().__init__(texture=texture, hardness=float("inf"), can_collide=False)
        self.depth: float = depth

        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(0, 0, 0, int(255 * depth)))

        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture = surface


class Ore(Tile):
    def __init__(self, stone_type: str, ore_type: str, hardness: float):
        super().__init__(texture=textures[f"{ore_type}_ore"], hardness=hardness)
        self.ore_type: str = ore_type
        self.mined_texture: Surface = textures[stone_type]

    def destroy(self) -> Union[str, None]:
        if self.hardness == float("inf"):
            return

        self.texture = self.mined_texture
        self.texture = self._generate_mined_texture()

        self.can_collide = False
        self.hardness = float("inf")

        return self.ore_type


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
