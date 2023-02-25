from random import choice
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
        texture = self.texture.copy()
        surface = pygame.Surface((32, 32))
        surface.blit(texture, (0, 0))
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