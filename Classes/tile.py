from random import choice, randint
from typing import Union
import pygame, os


textures: dict = {}
_textures_path = os.path.join("Images", "Tiles")
for file in os.listdir(_textures_path):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = os.path.join(_textures_path, file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))
        
        textures[file_name] = image


class Tile:
    def __init__(self, type: str, texture: Union[pygame.Surface, str], mined_texture: Union[pygame.Surface, str] = None, minable: bool = True, can_collide: bool = True, drops: list = None) -> None:
        self.type: str = type
        self.texture: pygame.Surface = textures[texture] if isinstance(texture, str) else texture
        if minable:
            match mined_texture:
                case pygame.Surface():
                    self.mined_texture: pygame.Surface = mined_texture
                
                case str():
                    self.mined_texture: pygame.Surface = textures[mined_texture]

                case _:
                    self.mined_texture: pygame.Surface = self.generate_mined_texture()
        
        self.minable: bool = minable
        self.can_collide: bool = can_collide
        if drops is None:
            self.drops: list = []

    def generate_mined_texture(self) -> pygame.Surface:
        overlay = pygame.Surface((32, 32)).convert_alpha()
        overlay.fill(pygame.Color(0, 0, 0, 64))
        surface = pygame.Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        return surface

    def mine(self) -> Union[str, None]:
        if not self.minable:
            return None

        self.can_collide = False
        self.texture = self.mined_texture
        return choice(self.drops) if len(self.drops) > 0 else None
    
    def update(self, position: pygame.Vector2) -> None:
        pygame.display.get_surface().blit(self.texture, position)


class Cave(Tile):
    def __init__(self, type: str, texture: Union[pygame.Surface, str]):
        self.texture: pygame.Surface = textures[texture] if isinstance(texture, str) else texture
        self.texture = self.generate_mined_texture()

        super().__init__(type, self.texture, minable=False, can_collide=False)


class Scaffolding(Tile):
    def __init__(self, type: str, texture: Union[pygame.Surface, str]) -> None:
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

        tile_underneath = self.map.get_tile(self.position.x, self.position.y+1)
        if type(tile_underneath) is Fluid:
            if tile_underneath.fluid_level < 1:
                self.fluid_level -= 0.1
                tile_underneath.fluid_level += 0.1

        elif not (tile_underneath.can_collide):
            self.map.set_tile(Tile("error", self.texture, minable=False, can_collide=False), self.position.x, self.position.y)
            self.position = self.position + pygame.Vector2(0, 1)
            self.map.set_tile(self, self.position.x, self.position.y)
            return

        if self.check_empty():
            return

        def _check_tile(x, y):
            if self.check_empty():
                return
        
            tile = self.map.get_tile(x, y)
            if type(tile) is Fluid:
                if int(tile.fluid_level) < 1:
                    tile.fluid_level += 0.1
                    self.fluid_level -= 0.1

            elif not (tile.can_collide):
                self.fluid_level -= 0.1
                self.map.set_tile(Fluid(self.map, pygame.Vector2(x, y), self.type, tile.texture, 0.1), x, y)


        if randint(0, 1):
            _check_tile(self.position.x+1, self.position.y)   
            _check_tile(self.position.x-1, self.position.y)
        else:
            _check_tile(self.position.x-1, self.position.y)
            _check_tile(self.position.x+1, self.position.y)

    def check_empty(self):
        if self.fluid_level <= 0:
            self.map.set_tile(Tile("error", self.texture, minable=False, can_collide=False), self.position.x, self.position.y)
            return True
        
        return False