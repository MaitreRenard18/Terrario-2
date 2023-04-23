from typing import Union
from time import time

import pygame
from pygame import Color, Surface, Vector2
from pygame.image import tostring, fromstring

from .textures import tiles_textures, load_animated_textures


_textures_names = {v: k for k, v in tiles_textures.items()}


def _generate_mined_texture(texture: Union[Surface, str]) -> Surface:
    if isinstance(texture, str) and f"mined_{texture}" in tiles_textures:
        return tiles_textures[f"mined_{texture}"]

    overlay = Surface((32, 32)).convert_alpha()
    overlay.fill(Color(0, 0, 0, 64))

    surface = Surface((32, 32))
    surface.blit(tiles_textures[texture] if isinstance(texture, str) else texture, (0, 0))
    surface.blit(overlay, (0, 0))

    return surface


class Tile:
    def __init__(self, texture: Union[Surface, str], hardness: int, can_collide: bool = True) -> None:
        self.texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        self._texture_key: str = texture if isinstance(texture, str) else None

        self.can_collide: bool = can_collide
        self.hardness: int = hardness

        self._mined: bool = False
        self._display_surface: Surface = pygame.display.get_surface()

    def update(self, position: Vector2) -> None:
        self._display_surface.blit(self.texture, position)

    def destroy(self) -> None:
        if self.hardness == 0 or self._mined:
            return

        self.texture = _generate_mined_texture(self.texture if self._texture_key is None else self._texture_key)
        self.can_collide = False
        self.hardness = 0
        self._mined = True

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_display_surface"]
        if state["_texture_key"] is None:
            state["texture"] = tostring(self.texture, "RGBA")
        else:
            del state["texture"]

        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._display_surface = pygame.display.get_surface()
        if self._texture_key is not None:
            if not self._mined:
                self.texture = tiles_textures[self._texture_key]
            else:
                self.texture = _generate_mined_texture(self._texture_key)
        else:
            self.texture = fromstring(self.texture, (32, 32), "RGBA")


class Air(Tile):
    def __init__(self):
        super().__init__(texture="air", hardness=0, can_collide=False)

    def update(self, position: Vector2) -> None: pass
    def destroy(self) -> None: pass


class Void(Tile):
    def __init__(self):
        super().__init__(texture="void", hardness=0, can_collide=False)

    def destroy(self) -> None: pass


class Background(Tile):
    def __init__(self, texture: Union[Surface, str], color: Color, depth: float = 0.5) -> None:
        super().__init__(texture=texture, hardness=0, can_collide=False)

        self.color: Color = color
        self.depth: float = depth

        self._base_texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        overlay = Surface((32, 32)).convert_alpha()
        color.a = int(255 * depth)
        overlay.fill(color)
        surface = Surface((32, 32))
        surface.blit(self._base_texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture: Surface = surface.convert()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["texture"]
        del state["_display_surface"]
        state["key"] = _textures_names.get(self._base_texture, None)
        if state["key"] is None:
            state["_base_texture"] = tostring(self._base_texture, "RGBA")
        else:
            del state["_base_texture"]

        return state

    def __setstate__(self, state):
        self._display_surface = pygame.display.get_surface()
        if state["key"] in tiles_textures:
            state["_base_texture"] = tiles_textures[state["key"]]
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
    def __init__(self, stone_type: str, ore_type: str, hardness: int):
        super().__init__(texture=tiles_textures[f"{ore_type}_ore"], hardness=hardness)
        self.ore_type: str = ore_type
        self.mined_texture: Surface = _generate_mined_texture(stone_type)

    def destroy(self) -> Union[str, None]:
        if self.hardness == 0:
            return

        self.texture = self.mined_texture

        self.can_collide = False
        self.hardness = 0

        return self.ore_type

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_display_surface"]
        state["texture"] = pygame.image.tostring(self.texture, "RGBA")
        state["mined_texture"] = tostring(self.mined_texture, "RGBA")
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._display_surface = pygame.display.get_surface()
        self.texture = pygame.image.fromstring(state["texture"], (32, 32), "RGBA")
        self.mined_texture = fromstring(state["mined_texture"], (32, 32), "RGBA")


class Scaffolding(Tile):
    def __init__(self, texture: Union[Surface, str]) -> None:
        self._base_texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        texture = self._base_texture.copy().convert_alpha()
        texture.set_colorkey((0, 0, 0))

        scaffolding_texture = tiles_textures["scaffolding"]

        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(tiles_textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(scaffolding_texture, (0, 0))

        super().__init__(texture=surface, hardness=0)

    def __getstate__(self):
        state = self.__dict__.copy()
        del state["_display_surface"]
        del state["texture"]
        state["_base_texture"] = tostring(self._base_texture, "RGBA")
        state["key"] = _textures_names.get(self._base_texture, None)
        return state

    def __setstate__(self, state):
        self._display_surface = pygame.display.get_surface()
        if state["key"] in tiles_textures:
            state["_base_texture"] = tiles_textures[state["key"]]
        else:
            state["_base_texture"] = fromstring(state["_base_texture"], (32, 32), "RGBA")
        self.__dict__.update(state)

        scaffolding_texture = tiles_textures["scaffolding"]
        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(tiles_textures[self._base_texture] if isinstance(self._base_texture, str) else self._base_texture,
                     (0, 0))
        surface.blit(scaffolding_texture, (0, 0))
        self.texture = surface


class AnimatedTile(Tile):
    def __init__(self, texture_name: str, speed: float = 1) -> None:
        self.texture_name: str = texture_name
        self.speed = speed

        self.frames = load_animated_textures(f"Tiles/{texture_name}.png", (32, 32))
        super().__init__(self.frames[0], 0)

    def update(self, position: Vector2) -> None:
        self.texture = self.frames[int((time() * self.speed) % len(self.frames))]
        display = pygame.display.get_surface()
        display.blit(self.texture, position)

    def __setstate__(self, state):
        self.__dict__.update()
        self._display_surface = pygame.display.get_surface()
        self.frames = load_animated_textures(f"Tiles/{self.texture_name}.png", (32, 32))
        self.texture = self.frames[0]
