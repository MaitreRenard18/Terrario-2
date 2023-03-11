"""A module that provides a set of classes to represent game tiles.

This module provides the following classes:
- Tile: A class to represent a game tile with a texture, a hardness value and a collision property.
- Cave: A class to represent a cave tile that cannot be mined or collided with. 
- Air: A class to represent an empty space tile that cannot be mined or collided with.
- Scaffolding: A class to represent a tile that can be placed by the player allowing him to climb up.

Author:
    Lucas THOMAS (MaitreRenard18)
"""
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
        image = pygame.transform.scale(
            pygame.image.load(path), (32, 32)
        ).convert_alpha()

        textures[file_name] = image


class Tile:
    """A class to represent a game tile."""
    def __init__(self, texture: Union[Surface, str], hardness: Union[int, float], can_collide: bool = True) -> None:
        """
        Initializes a Tile object with given texture, hardness and collision property.

        Args:
            texture (Union[Surface, str]): The texture of the Tile. Can be a Surface object or a string representing
                                            a key in a dictionary of texture objects.
            hardness (Union[int, float]): The hardness of the Tile. Determines if the player can mine the tile depending of the drill level.
            can_collide (bool, optional): A flag indicating if the Tile can be collided with. Defaults to True.
        """
        self.texture: Surface = textures[texture] if isinstance(texture, str) else texture

        self.can_collide: bool = can_collide
        self.hardness: int = hardness

    def destroy(self) -> Union[str, None]:
        """
        Destroys the Tile object by setting its collision property to False and generating a new texture.

        Returns:
            Union[str, None]: If the Tile can be dropped as an item, returns a string representing the item. Otherwise,
                              returns None.
        """
        self.can_collide = False
        self.texture = self._generate_mined_texture()

    def update(self, position: Vector2) -> None:
        """
        Updates the Tile object by blitting its texture to the display surface.

        Args:
            position (Vector2): A Vector2 object representing the position of the Tile on the screen.
        """
        display = pygame.display.get_surface()
        if -32 <= position.x <= display.get_size()[0] and -32 <= position.y <= display.get_size()[0]:
            display.blit(self.texture, position)

    def _generate_mined_texture(self) -> Surface:
        """
        Generates a new texture for the Tile object to represent it being mined.

        Returns:
            Surface: A Surface object representing the new texture.
        """
        overlay = Surface((32, 32)).convert_alpha()
        overlay.fill(Color(0, 0, 0, 64))

        surface = Surface((32, 32))
        surface.blit(self.texture, (0, 0))
        surface.blit(overlay, (0, 0))
        return surface


class Cave(Tile):
    """A class to represent a cave tile that cannot be mined or collided with."""
    def __init__(self, texture: Union[Surface, str]) -> None:
        """Initializes a Cave object.

        Args:
            texture (Union[Surface, str]): The texture of the Tile. Can be a Surface object or a string representing
                                            a key in a dictionary of texture objects. The texture will be darken to
                                            differencate it from solid tiles.
        """
        super().__init__(texture=texture, hardness=float("inf"), can_collide=False)
        self.texture = self._generate_mined_texture()


class Air(Tile):
    """A class to represent an air tile, which is not visible and cannot be collided with."""
    def __init__(self) -> None:
        """Initializes an Air object."""
        super().__init__(texture="air", hardness=float("inf"), can_collide=False)

    def update(self, position: Vector2) -> None:
        """Updates the Air object by doing nothing."""
        pass


class Scaffolding(Tile):
    """A class to represent a scaffolding tile, which is a Tile that can be walked through but not mined allowing the player to climb up."""
    def __init__(self, texture: Union[Surface, str]) -> None:
        """
        Initializes a Scaffolding object.

        Args:
            texture (Union[Surface, str]): The texture of the Tile. Can be a Surface object or a string representing
                                            a key in a dictionary of texture objects. The scaffolding texture is 
                                            added as an overlay to this texture.
        """
        surface = pygame.Surface((32, 32))
        surface.fill(pygame.Color(77, 165, 217))
        surface.blit(textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(textures["scaffolding"], (0, 0))

        super().__init__(texture=surface, hardness=float("inf"), minable=False)
