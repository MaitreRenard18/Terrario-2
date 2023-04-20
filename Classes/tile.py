from typing import Union
from time import time

import pygame
from pygame import Color, Surface, Vector2
from pygame.image import tostring, fromstring

from .textures import import_textures, import_animated_textures


textures = import_textures("Tiles", (32, 32))
_textures_names = {v: k for k, v in textures.items()}


class Tile:
    def __init__(self, texture: Union[Surface, str], hardness: Union[int, float], can_collide: bool = True) -> None:
        self.texture: Surface = textures[texture] if isinstance(texture, str) else texture

        self.can_collide: bool = can_collide
        self.hardness: int = hardness

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def destroy(self) -> Union[str, None]:
        if self.hardness == float("-inf"):
            return

        self.texture = self._generate_mined_texture()
        self.can_collide = False
        self.hardness = float("-inf")
    
    def _generate_mined_texture(self) -> Surface:
        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(0, 0, 0, 64))

        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        return surface

    def __getstate__(self):
        state = self.__dict__.copy()
        state["key"] = _textures_names.get(self.texture, None)
        if state["key"] is None:
            state["texture"] = tostring(self.texture, "RGBA")
        else:
            del state["texture"]

        return state

    def __setstate__(self, state):
        if state["key"] in textures:
            state["texture"] = textures[state["key"]]
        else:
            state["texture"] = fromstring(state["texture"], (32, 32), "RGBA")

        self.__dict__.update(state)


class Air(Tile):
    def __init__(self) -> None:
        super().__init__(texture="air", hardness=float("-inf"), can_collide=False)

    def update(self, position: Vector2) -> None:
        pass

    def destroy(self) -> None:
        pass


class Background(Air):
    def __init__(self, texture: Union[Surface, str], color: Color, depth: float = 0.5) -> None:
        super().__init__()

        self.color: Color = color
        self.depth: float = depth

        self._base_texture: Surface = textures[texture] if isinstance(texture, str) else texture
        overlay = Surface((32, 32)).convert_alpha()
        color.a = int(255 * depth)
        overlay.fill(color)
        surface = Surface((32, 32))
        surface.blit(self._base_texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture: Surface = surface.convert()

    def update(self, position: Vector2) -> None:
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["texture"]
        state["key"] = _textures_names.get(self._base_texture, None)
        if state["key"] is None:
            state["_base_texture"] = tostring(self._base_texture, "RGBA")
        else:
            del state["_base_texture"]

        return state

    def __setstate__(self, state):
        if state["key"] in textures:
            state["_base_texture"] = textures[state["key"]]
        else:
            state["_base_texture"] = fromstring(state["texture"], (32, 32), "RGBA")
        self.__dict__.update(state)

        overlay = Surface((32, 32)).convert_alpha()
        self.color.a = int(255 * self.depth)
        overlay.fill(self.color)
        surface = Surface((32, 32))
        surface.blit(self._base_texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture: Surface = surface.convert()


class Ore(Tile):
    def __init__(self, stone_type: str, ore_type: str, hardness: float):
        super().__init__(texture=textures[f"{ore_type}_ore"], hardness=hardness)
        self.ore_type: str = ore_type
        self.mined_texture: Surface = textures[stone_type]

    def destroy(self) -> Union[str, None]:
        if self.hardness == float("-inf"):
            return

        self.texture = self.mined_texture
        self.texture = self._generate_mined_texture()

        self.can_collide = False
        self.hardness = float("-inf")

        return self.ore_type

    def __getstate__(self):
        state = self.__dict__.copy()
        state["texture"] = pygame.image.tostring(self.texture, "RGBA")
        state["mined_texture"] = tostring(self.mined_texture, "RGBA")
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.texture = pygame.image.fromstring(state["texture"], (32, 32), "RGBA")
        self.mined_texture = fromstring(state["mined_texture"], (32, 32), "RGBA")


class Scaffolding(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        self._base_texture: Surface = textures[texture] if isinstance(texture, str) else texture
        texture = self._base_texture.copy().convert_alpha()
        texture.set_colorkey((0, 0, 0))

        scaffolding_texture = textures["scaffolding"]

        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(scaffolding_texture, (0, 0))

        super().__init__(texture=surface, hardness=float("-inf"))

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["texture"]
        state["_base_texture"] = tostring(self._base_texture, "RGBA")
        state["key"] = _textures_names.get(self._base_texture, None)
        return state

    def __setstate__(self, state):
        if state["key"] in textures:
            state["_base_texture"] = textures[state["key"]]
        else:
            state["_base_texture"] = fromstring(state["_base_texture"], (32, 32), "RGBA")
        self.__dict__.update(state)

        scaffolding_texture = textures["scaffolding"]
        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(textures[self._base_texture] if isinstance(self._base_texture, str) else self._base_texture, (0, 0))
        surface.blit(scaffolding_texture, (0, 0))
        self.texture = surface


class AnimatedTile(Tile):
    def __init__(self, texture_name: str, speed: float = 1) -> None:
        self.texture_name: str = texture_name
        self.speed = speed

        self.frames = import_animated_textures(f"Tiles/{texture_name}.png", (32, 32))
        super().__init__(self.frames[0], 0)

    def update(self, position: Vector2) -> None:
        self.texture = self.frames[int((time() * self.speed) % len(self.frames))]
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def __setstate__(self, state):
        self.__dict__.update()
        self.frames = import_animated_textures(f"Tiles/{self.texture_name}.png", (32, 32))
        self.texture = self.frames[0]
