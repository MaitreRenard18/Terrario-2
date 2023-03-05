from random import choice, randint
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

class Fluid(Tile):
    def __init__(self, map, position: pygame.Vector2, type: str, texture: Union[pygame.Surface, str], level: float = 1) -> None:
        self.map = map
        self.position = position
        self.fluid_level = level

        super().__init__(type, texture, minable=False, can_collide=False)

    def update(self, screen_position: pygame.Vector2) -> None:
        if self.check_empty():
            return
        
        texture = pygame.Surface((32, 32))
        texture.blit(self.texture, (0, 0))
        texture.fill(pygame.Color(0, 0, 128), pygame.Rect(0, 32 - 32 * self.fluid_level, 32, 32))
        pygame.display.get_surface().blit(texture, screen_position)

        """font = pygame.font.SysFont("Arial", 16)
        img = font.render(str(self.fluid_level), True, pygame.Color(255, 0, 0))
        pygame.display.get_surface().blit(img, screen_position)"""

        tile_underneath = self.map.get_tile(self.position + (0, 1))
        if type(tile_underneath) is Fluid:
            if tile_underneath.fluid_level < 1:
                self.fluid_level -= 0.1
                tile_underneath.fluid_level += 0.1

        elif not (tile_underneath.can_collide):
            self.map.set_tile(Tile("error", self.texture, minable=False, can_collide=False), self.position)
            self.position = self.position + pygame.Vector2(0, 1)
            self.map.set_tile(self, self.position)
            return

        if self.check_empty():
            return

        def _check_tile(x, y):
            if self.check_empty():
                return
        
            tile = self.map.get_tile(Vector2(x, y))
            if type(tile) is Fluid:
                tile.fluid_level += 0.1
                self.fluid_level -= 0.1

            elif not (tile.can_collide):
                self.fluid_level -= 0.1
                self.map.set_tile(Fluid(self.map, pygame.Vector2(x, y), self.type, tile.texture, 0.1), Vector2(x, y))

        tile_left = self.map.get_tile(self.position - (1, 0))
        tile_right = self.map.get_tile(self.position + (1, 0))
        if type(tile_right) is Fluid and type(tile_left) is Fluid:
            if tile_left.fluid_level > tile_right.fluid_level:
                _check_tile(self.position.x+1, self.position.y)
                _check_tile(self.position.x-1, self.position.y)
            else:
                _check_tile(self.position.x-1, self.position.y)
                _check_tile(self.position.x+1, self.position.y)

        elif type(tile_left) is Fluid:
            _check_tile(self.position.x+1, self.position.y)
            _check_tile(self.position.x-1, self.position.y)

        elif type(tile_right) is Fluid:
            _check_tile(self.position.x-1, self.position.y)
            _check_tile(self.position.x+1, self.position.y)

        elif randint(0, 1) == 0:
            _check_tile(self.position.x+1, self.position.y)
            _check_tile(self.position.x-1, self.position.y)
        
        else:
            _check_tile(self.position.x-1, self.position.y)
            _check_tile(self.position.x+1, self.position.y)

    def check_empty(self):
        if self.fluid_level <= 0:
            self.map.set_tile(Tile("error", self.texture, minable=False, can_collide=False), self.position)
            return True
        
        return False