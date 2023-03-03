from random import choice
from typing import Union, Dict, List
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
    def __init__(self, type: str, texture: Union[Surface, str], mined_texture: Union[Surface, str] = None, can_collide: bool = True, minable: bool = True, drops: List[str] = None) -> None:
        self.type: str = type

        self.texture: Surface = textures[texture] if isinstance(texture, str) else texture
        self.mined_texture: Surface = textures[mined_texture] if isinstance(mined_texture, str) else mined_texture if isinstance(mined_texture, Surface) else self.generate_mined_texture()
        
        self.can_collide: bool = can_collide
        self.minable: bool = minable

        if drops is None:
            self.drops: List[str] = []

    def generate_mined_texture(self) -> Surface:
        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(0, 0, 0, 64))

        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        return surface

    def destroy(self) -> Union[str, None]:
        if not self.minable:
            return None

        self.can_collide = False
        self.texture = self.mined_texture
        return choice(self.drops) if len(self.drops) > 0 else None
    
    def update(self, position: Vector2) -> None:
        pygame.display.get_surface().blit(self.texture, position)


class Cave(Tile):
    def __init__(self, type: str, texture: Union[Surface, str]) -> None:
        super().__init__(type, texture, texture, minable=False, can_collide=False)
        self.texture = self.generate_mined_texture()


class Air(Tile):
    def __init__(self) -> None:
        super().__init__("air", "air", can_collide=False, minable=False)

    def update(self, position: Vector2) -> None:
        pass


class Scaffolding(Tile):
    def __init__(self, type: str, texture: Union[Surface, str]) -> None:
        surface = pygame.surface.Surface((32, 32))
        surface.fill(pygame.Color(77, 165, 217))
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(textures["scaffolding"], (0, 0))
        
        super().__init__(type, surface, minable=False)