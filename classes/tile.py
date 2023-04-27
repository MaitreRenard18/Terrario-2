from typing import Union, Any, Dict
from time import time

import pygame
from pygame import Color, Surface, Vector2
from pygame.image import tostring, fromstring

from .textures import tiles_textures, load_animated_textures
from .constants import screen


def _generate_mined_texture(texture: Union[Surface, str]) -> Surface:
    if isinstance(texture, str) and f"mined_{texture}" in tiles_textures:
        return tiles_textures[f"mined_{texture}"]

    overlay = Surface((32, 32)).convert_alpha()
    overlay.fill(Color(0, 0, 0, 64))

    surface = Surface((32, 32))
    surface.blit(tiles_textures[texture] if isinstance(texture, str) else texture, (0, 0))
    surface.blit(overlay, (0, 0))

    if isinstance(texture, str):
        tiles_textures[f"mined_{texture}"] = surface
    return surface


class Tile:
    """
    Classe qui représente une tuile dans le monde.
    """

    def __init__(self, texture: Union[Surface, str], hardness: int, can_collide: bool = True) -> None:
        """
        Initialise une tuile, avec une texture, une solidité (qui determine si la foreuse peut miner
        la tuile ou non), et un attribut qui détermine ou non si le joueur peu passé à travers.
        """

        self.texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        self._texture_key: str = texture if isinstance(texture, str) else None

        self.can_collide: bool = can_collide
        self.hardness: int = hardness

        self._mined: bool = False

    def update(self, position: Vector2) -> None:
        """
        Affiche la tuile à la position passée en paramètre.
        """

        screen.blit(self.texture, position)

    def destroy(self) -> None:
        """
        Mine la tuile, la tuile va alors afficher une texture assombrie pour signifier qu'elle est minée.
        """

        if self.hardness == 0 or self._mined:
            return

        self.texture = _generate_mined_texture(self.texture if self._texture_key is None else self._texture_key)
        self.can_collide = False
        self.hardness = 0
        self._mined = True

    def __getstate__(self) -> Dict[str, Any]:
        """
        Renvoie un dictionnaire représentant l'état de l'objet pour la sérialisation.
        """

        state = self.__dict__.copy()

        if state["_texture_key"] is None:
            state["texture"] = tostring(self.texture, "RGBA")
        else:
            del state["texture"]

        return state

    def __setstate__(self, state: Dict[str, Any]) -> None:
        """
        Restaure l'état de l'objet à partir du dictionnaire "state".
        """

        self.__dict__.update(state)

        if self._texture_key is not None:
            if not self._mined:
                self.texture = tiles_textures[self._texture_key]
            else:
                self.texture = _generate_mined_texture(self._texture_key)
        else:
            self.texture = fromstring(self.texture, (32, 32), "RGBA")


class Air(Tile):
    """
    Tuile représentant de l'air, qui est une tuile sans texture,
    sans collision, avec une hardness de 0.
    """

    def __init__(self):
        """
        Initialise de l'air.
        """

        super().__init__(texture="air", hardness=0, can_collide=False)

    def update(self, position: Vector2) -> None: pass
    def destroy(self) -> None: pass


class Void(Tile):
    """
    Tuile représentant du vide qui est une tuile avec une texture noire,
    sans collision, avec une hardness de 0.
    """

    def __init__(self):
        """
        Initialise de l'air.
        """

        super().__init__(texture="void", hardness=0, can_collide=False)

    def destroy(self) -> None: pass


class Background(Tile):
    """
    Tuile représentant du décor de fond, elle a une texture teintée d'une certaine couleur,
    et n'a aucune collision.
    """

    def __init__(self, texture: Union[Surface, str], color: Color, depth: float = 0.5) -> None:
        """
        Initialise du décor, avec une texture, une teinte, une profondeur qui détermine à quel point
        la teinte va affecter la texture.
        """

        super().__init__(texture=texture, hardness=0, can_collide=False)

        self.color: Color = color
        self.depth: float = depth

        self._base_texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        self._texture_key: str = texture if isinstance(texture, str) else None

        self._generate_texture()

    def _generate_texture(self) -> None:
        """
        Génère la texture teintée.
        """

        overlay = Surface((32, 32)).convert_alpha()
        self.color.a = int(255 * self.depth)
        overlay.fill(self.color)
        surface = Surface((32, 32))
        surface.blit(self._base_texture, (0, 0))
        surface.blit(overlay, (0, 0))
        self.texture: Surface = surface.convert()

    def __getstate__(self) -> Dict[str, Any]:
        """
        Renvoie un dictionnaire représentant l'état de l'objet pour la sérialisation.
        """

        state = self.__dict__.copy()

        del state["texture"]
        if state["_texture_key"] is None:
            state["_base_texture"] = tostring(self._base_texture, "RGBA")
        else:
            del state["_base_texture"]

        return state

    def __setstate__(self, state):
        """
        Restaure l'état de l'objet à partir du dictionnaire "state".
        """

        self.__dict__.update(state)

        if self._texture_key is not None:
            self._base_texture = tiles_textures[self._texture_key]
        else:
            self._base_texture = fromstring(state["texture"], (32, 32), "RGBA")

        self._generate_texture()


class Ore(Tile):
    """
    Tuile représentant un minerai.
    """

    def __init__(self, stone_type: str, ore_type: str, hardness: int):
        """
        Initialise un minerai, avec un type de roche (qui sera affiché une fois le minerai miné),
        et type de minerai (qui est la texture affichée avant qu'il soit miné) et une solidité.
        """

        super().__init__(texture=tiles_textures[f"{ore_type}_ore"], hardness=hardness)
        self.ore_type: str = ore_type
        self._stone_type: str = stone_type

        self.mined_texture: Surface = _generate_mined_texture(stone_type)

        self._mined = False

    def destroy(self) -> Union[str, None]:
        """
        Mine le minerai et retourne une chaine de caractère correspondant au type de minerai
        pour qu'il puisse être rajouté à l'inventaire du joueur.
        """

        if self._mined:
            return

        self._mined = True
        self.texture = self.mined_texture

        self.can_collide = False
        self.hardness = 0

        return self.ore_type

    def __getstate__(self):
        """
        Renvoie un dictionnaire représentant l'état de l'objet pour la sérialisation.
        """

        state = self.__dict__.copy()

        del state["texture"]
        del state["mined_texture"]

        return state

    def __setstate__(self, state):
        """
        Restaure l'état de l'objet à partir du dictionnaire "state".
        """

        self.__dict__.update(state)

        self.texture = tiles_textures[f"{self.ore_type}_ore"]
        self.mined_texture: Surface = _generate_mined_texture(self._stone_type)

        if self._mined:
            self.texture = self.mined_texture


class Scaffolding(Tile):
    """
    Tuile représentant un échafaudage, qui est une tuile qui évite au joueur de tomber quand il monte.
    """

    def __init__(self, texture: Union[Surface, str]) -> None:
        """
        Initialise un échafaudage avec une texture de fond.
        """

        super().__init__(texture=texture, hardness=0)

        self._base_texture: Surface = tiles_textures[texture] if isinstance(texture, str) else texture
        self._texture_key: str = texture if isinstance(texture, str) else None

        self._generate_texture()

    def _generate_texture(self) -> None:
        """
        Génère la texture de l'échafaudage.
        """

        if self._texture_key is not None and f"{self._texture_key}_scaffolding" in tiles_textures:
            return tiles_textures[f"{self._texture_key}_scaffolding"]

        texture = self._base_texture.copy().convert_alpha()
        texture.set_colorkey((0, 0, 0))

        scaffolding_texture = tiles_textures["scaffolding"]

        surface = pygame.Surface((32, 32), pygame.SRCALPHA, depth=32)
        surface.blit(tiles_textures[texture] if isinstance(texture, str) else texture, (0, 0))
        surface.blit(scaffolding_texture, (0, 0))

        if self._texture_key is not None:
            tiles_textures[f"{self._texture_key}_scaffolding"] = Surface
        self.texture = surface

    def __getstate__(self):
        """
        Renvoie un dictionnaire représentant l'état de l'objet pour la sérialisation.
        """

        state = self.__dict__.copy()

        del state["texture"]
        if state["_texture_key"] is not None:
            del state["_base_texture"]
        else:
            state["_base_texture"] = tostring(self._base_texture, "RGBA")

        return state

    def __setstate__(self, state):
        """
        Restaure l'état de l'objet à partir du dictionnaire "state".
        """

        self.__dict__.update(state)

        if self._texture_key is not None:
            state._base_texture = tiles_textures[self._texture_key]
        else:
            self._base_texture = fromstring(state["_base_texture"], (32, 32), "RGBA")

        self._generate_texture()


class AnimatedTile(Tile):
    """
    Represent une tuile animée (utilisé uniquement pour le feu).
    La classe ne contient pas de fonction pour la sérialisation, car la classe Prop (qui est la seule
    à utiliser AnimatedTile) ne sauvegarde pas les tuiles.
    """

    def __init__(self, texture_name: str, speed: float = 1) -> None:
        """
        Initialise une tuile animée, avec une texture (contentant toutes les frames de l'animation),
        et une vitesse d'animation.
        """

        self.texture_name: str = texture_name
        self.speed: float = speed

        self.frames = load_animated_textures(f"tiles/{texture_name}.png", (32, 32))
        super().__init__(self.frames[0], 0)

    def update(self, position: Vector2) -> None:
        """
        Affiche la tuile à la position passée en paramètre.
        """

        self.texture = self.frames[int((time() * self.speed) % len(self.frames))]
        screen.blit(self.texture, position)
