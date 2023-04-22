from random import choice, randint, seed
from typing import Dict, List, Union

import opensimplex
import pygame.image
from pygame import Color, Surface, display
from pygame.math import Vector2

from .player import Player
from .prop import Prop
from .tile import Air, Background, Ore, Tile, Void

# Déclaration des biomes et des décors associés à chaque biome.
biomes: Dict[Union[float, int], List[str]] = {
    816: ["hell"],
    616: ["haunted_cave"],
    416: ["crystal_cave"],
    216: ["lush_cave", "shroom_cave"],
    16: ["sand_cave", "cave", "ice_cave"],
    float("-inf"): ["desert", "forest", "snowy_forest"]
}

tile_palettes: Dict[str, Dict[str, str]] = {
    "forest": {
        "primary_tile": "dirt",
        "floor_tile": "grass",
        "ore": "rock"
    },

    "desert": {
        "primary_tile": "sand"
    },

    "snowy_forest": {
        "primary_tile": "snowy_dirt",
        "floor_tile": "snowy_grass"
    },

    "cave": {
        "primary_tile": "loess",
        "ore": "iron"
    },

    "sand_cave": {
        "primary_tile": "sandstone",
        "ore": "gold"
    },

    "ice_cave": {
        "primary_tile": "ice",
        "ore": "coal"
    },

    "lush_cave": {
        "primary_tile": "stone",
        "floor_tile": "mossy_stone",
        "ore": "uranium"
    },

    "shroom_cave": {
        "primary_tile": "dark_stone",
        "floor_tile": "mycelium",
        "ore": "copper"
    },

    "haunted_cave": {
        "primary_tile": "shale",
        "ore": "soul"
    },

    "crystal_cave": {
        "primary_tile": "calcite",
        "ore": "ruby"
    },

    "hell": {
        "primary_tile": "hellstone",
        "ore": "dark_crystal"
    }
}

biomes_scale: Dict[str, float] = {
    "shroom_cave": 0.075,
    "lush_cave": 0.075,

    "crystal_cave": 0.065,

    "haunted_cave": 0.125,

    "hell": 0.05
}

props: Dict[str, List[str]] = {
    "forest": ["oak_tree_1", "oak_tree_2", "oak_tree_3", "weed", "weed", "tulip"],
    "desert": ["cactus_1", "cactus_2", "cactus_3", "cactus_4", "dead_weed", "dead_weed", "dead_weed"],
    "snowy_forest": ["fir_1", "fir_2", "snowman", "snowy_weed"],

    "cave": ["stalagmite_1", "stalagmite_2", "stalagmite_3"],
    "sand_cave": ["cactus_1", "cactus_2", "dead_weed", "dead_weed"],
    "ice_cave": ["ice_stalagmite_1", "ice_stalagmite_2", "ice_stalagmite_3"],

    "lush_cave": ["oak_tree_1", "oak_tree_2", "oak_tree_3", "weed", "weed", "tulip"],
    "shroom_cave": [
        "red_mushroom", "brown_mushroom", "red_mushroom", "brown_mushroom", "giant_red_mushroom", "giant_brown_mushroom"
    ],

    "crystal_cave": ["crystal_1", "crystal_2", "crystal_3", "crystal_4", "amethyst"],

    "haunted_cave": ["tombstone_1", "tombstone_2", "lamp", "skull", "pile_of_skulls"],

    "hell": ["fire", "skull", "pile_of_skulls"]
}

props_density: Dict[str, int] = {
    "shroom_cave": 4,

    "haunted_cave": 6,
    "crystal_cave": 2
}


# Déclaration de la classe Map
class Map:
    """
    Class qui représente une carte 2D générée procéduralement composée de grottes
    et de différents biomes en fonction de la profondeur.
    """

    def __init__(self, world_seed: int = None) -> None:
        """
        Initialise une Map.
        """

        # Récupère la surface d'affichage
        self.display_surface: Surface = display.get_surface()

        # Initialise le joueur et le dictionnaire contenant les tuiles et le dictionnaire contenant les props.
        self.player: Player = Player(Vector2(0, -1), self)
        self._tiles: Dict[int, Dict[int, Tile]] = {}
        self.props: Dict[int, Dict[int, List[Prop]]] = {}

        # Initialise les valeurs utilisées lors de la génération de la carte.
        self.seed = randint(0, 2 ** 16) if world_seed is None else world_seed
        opensimplex.seed(self.seed)
        seed(self.seed)

        self.scale: float = 0.1
        self.cave_size: float = 0.5
        self.biome_size: float = 0.01
        self.biome_blend: int = 3

        # Récupère le nombre de tuiles qui peut être afficher en x et en y.
        self.render_distance: tuple = (self.display_surface.get_size()[0] // 32 // 2 + 4,
                                       self.display_surface.get_size()[1] // 32 // 2 + 3)

    def get_tile(self, position: Union[Vector2, tuple]) -> Tile:
        """
        Prend en paramètre un Vector2 et retourne la tuile se trouvant à cette position. 
        Si la tuile n'existe pas, en génère une nouvelle.
        """

        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])
        self._tiles[x] = self._tiles.get(x, {})

        tile = self._tiles[x].get(y, None)
        if tile is None:
            tile = self._generate_tile(Vector2(x, y))

        return tile

    def set_tile(self, tile: Union[Tile, tuple], position: Vector2) -> Tile:
        """
        Prend en paramètre une Tuile et un Vector2, et change la tuile
        se trouvant à cette position par la tuile passée en paramètre.
        Retourne la tuile passée en paramètre.
        """

        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])
        self._tiles[x] = self._tiles.get(x, {})
        self._tiles[x][y] = tile

        return tile

    def get_prop(self, position: Union[Vector2, tuple]) -> Union[List[Prop], None]:
        """
        Prend en paramètre un Vector2 et retourne les props se trouvant à cette position.
        Retourne None s'il n'y a pas de prop à cette position.
        """

        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])
        return self.props.get(x, {}).get(y, None)

    def add_prop(self, prop: Prop, position: Union[Vector2, tuple]) -> Prop:
        """
        Prend en paramètre un Prop et un Vector2, et rajoute le prop
        à la position passée un paramètre.
        Retourne la tuile passée en paramètre.
        """

        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])
        self.props[x] = self.props.get(x, {})
        self.props[x][y] = self.props[x].get(y, [])
        self.props[x][y].append(prop)

        return prop

    def remove_prop(self, prop: Prop, position: Union[Vector2, tuple]) -> Prop:
        """
        Prend en paramètre un Prop et un Vector2, et enlève le prop passé en paramètre se trouvant
        à la position passée un paramètre.
        Retourne la tuile passée en paramètre.
        """

        x, y = (int(position.x), int(position.y)) if isinstance(position, Vector2) else (position[0], position[1])
        self.props[x] = self.props.get(x, {})
        self.props[x][y] = self.props[x].get(y, [])
        self.props[x][y].pop(self.props[x][y].index(prop))

        return prop

    def _generate_tile(self, position: Vector2) -> Tile:
        """
        Prend en paramètre un Vector2 et génère une tuile à cette position.
        Retourne la tuile générée.
        """

        # Créer une entrée dans le dictionnaire.
        self._tiles[position.x] = self._tiles.get(position.x, {})

        # Récupère le biome.
        hardness = 0
        biome = "cave"
        for hardness, k in enumerate(biomes.keys()):
            if position.y + randint(0, self.biome_blend) >= k:
                number_range = 2 / len(biomes[k])
                noise_value = opensimplex.noise2((position.x + randint(0, self.biome_blend)) * self.biome_size, 0) + 1
                biome = biomes[k][int(noise_value // number_range)]
                break

        hardness = len(biomes) - hardness
        tile_palette = tile_palettes[biome] if biome in tile_palettes else tile_palettes["cave"]

        # Génération de la tuile si elle se trouve à la surface.
        random_biome_blend_value = randint(0, self.biome_blend)
        if position.y - random_biome_blend_value < 16:
            noise_value = round(opensimplex.noise2(position.x * self.scale * 0.25, 0) * 6)
            if position.y == noise_value:
                # Génération des props
                if biome in props and randint(1, 5) == 1:
                    if self.get_prop(position - (1, 0)) is None and self.get_prop(position + (1, 0)) is None:
                        self.props[position.x] = self.props.get(position.x, {})
                        self.props[position.x][position.y] = self.props[position.x].get(position.y, [])
                        self.props[position.x][position.y].append(Prop(self, position, choice(props[biome])))

                # Génération de la tuile supérieure
                if "floor_tile" in tile_palette:
                    self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], hardness)

                else:
                    self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], hardness)

            elif position.y > noise_value:
                if randint(0, 32) == 0 and "ore" in tile_palette:
                    self._tiles[position.x][position.y] = Ore(tile_palette["primary_tile"], tile_palette["ore"],
                                                              hardness)

                else:
                    self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], hardness)

            else:
                # Génération de l'arrière-plan
                noise_value = round(opensimplex.noise2(-position.x * self.scale * 0.25, 0) * 8) - 6
                if position.y == noise_value:
                    if "floor_tile" in tile_palette:
                        self._tiles[position.x][position.y] = Background(tile_palette["floor_tile"],
                                                                         Color(77, 165, 217))

                    else:
                        self._tiles[position.x][position.y] = Background(tile_palette["primary_tile"],
                                                                         Color(77, 165, 217))

                elif position.y > noise_value:
                    self._tiles[position.x][position.y] = Background(tile_palette["primary_tile"], Color(77, 165, 217))

                else:
                    self._tiles[position.x][position.y] = Air()

        # Génération de la tuile si elle se trouve sous terre.
        elif position.y - random_biome_blend_value < 1016:
            if biome in biomes_scale:
                noise_value = opensimplex.noise2(position.x * biomes_scale[biome], position.y * biomes_scale[biome])
            else:
                noise_value = opensimplex.noise2(position.x * self.scale, position.y * self.scale)

            if noise_value < (self.cave_size * 2) - 1:
                if randint(0, 32) == 0 and "ore" in tile_palette:
                    self._tiles[position.x][position.y] = Ore(tile_palette["primary_tile"], tile_palette["ore"],
                                                              hardness)

                else:
                    self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], hardness)

                if not self.get_tile(position - (0, 1)).can_collide:
                    # Génération des props
                    density = 8
                    if biome in props_density:
                        density = props_density[biome]

                    if biome in props and randint(1, density) == 1:
                        self.props[position.x] = self.props.get(position.x, {})
                        self.props[position.x][position.y] = self.props[position.x].get(position.y, [])
                        self.props[position.x][position.y].append(Prop(self, position, choice(props[biome])))

                    # Génération de la tuile supérieure
                    if "floor_tile" in tile_palette:
                        self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], hardness)

            else:
                if biome in biomes_scale:
                    depth = (1 + opensimplex.noise2(position.x * biomes_scale[biome],
                                                    position.y * biomes_scale[biome])) / 3
                else:
                    depth = (1 + opensimplex.noise2(position.x * self.scale, position.y * self.scale)) / 3

                if depth < 0.4:
                    self._tiles[position.x][position.y] = Background(tile_palette["primary_tile"], Color(0, 0, 0), 0.35)
                elif depth < 0.5:
                    self._tiles[position.x][position.y] = Background(tile_palette["primary_tile"], Color(0, 0, 0), 0.45)
                else:
                    self._tiles[position.x][position.y] = Background(tile_palette["primary_tile"], Color(0, 0, 0), 0.5)

        elif position.y - random_biome_blend_value < 1024:
            self._tiles[position.x][position.y] = Tile("bedrock", hardness + 1)

        elif position.y - random_biome_blend_value <= 2048:
            self._tiles[position.x][position.y] = Void()

        else:
            self._tiles[position.x][position.y] = Background("air", Color(77, 165, 217),
                                                             min((position.y - 2048) * 0.05, 1))

        return self._tiles[position.x][position.y]

    def update(self) -> None:
        """
        Affiche la carte sur l'écran et s'occupe de mettre à jour les différentes tuiles, ainsi que le joueur.
        """

        # Affiche le ciel.
        self.display_surface.fill(Color(77, 165, 217))

        # Permet de décaler les tuiles en fonction du joueur pour que celui-ci soit au centre de l'écran.
        offset = Vector2()
        offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        # Parcours chaques tuiles visibles à l'écran et les met à jour.
        props_to_render = []
        for x in range(round(self.player.position.x) - self.render_distance[0],
                       round(self.player.position.x) + self.render_distance[0]):
            for y in range(round(self.player.position.y) - self.render_distance[1],
                           round(self.player.position.y) + self.render_distance[1] + 10):
                offset_vec = Vector2(x, y) * 32 - offset

                tile = self.get_tile((x, y))
                tile.update(offset_vec)

                if self.get_prop((x, y)) is not None:
                    prop = self.props[x][y]
                    props_to_render.append(prop)

        # Fait le rendu des props
        for prop_list in props_to_render:
            for prop in prop_list:
                prop.update(prop.position * 32 - offset)

        # Détermine la position du joueur sur l'écran.
        offset_rect = self.player.rect.copy()
        offset_rect.center -= offset

        self.player.facing()

        # Met à jour le joueur.
        self.display_surface.blit(self.player.image, offset_rect)
        self.display_surface.blit(self.player.tip_image, (offset_rect.x + self.player.tip_position.x * 32,
                                                          offset_rect.y + self.player.tip_position.y * 32))

        self.player.update()

    def get_thumbnail(self) -> Surface:
        """Retourne une surface au format 1:1 de ce qui est actuellement affiché sur l'écran."""

        if self.display_surface.get_width() > self.display_surface.get_height():
            return self.display_surface.subsurface((
                self.display_surface.get_width() // 2 - self.display_surface.get_height() // 2, 0,
                self.display_surface.get_height(), self.display_surface.get_height()))

        else:
            return self.display_surface.subsurface((
                0, self.display_surface.get_height() // 2 - self.display_surface.get_width() // 2,
                self.display_surface.get_width(), self.display_surface.get_width()))

    def __getstate__(self):
        """
        Renvoie un dictionnaire représentant l'état de l'objet pour la sérialisation.
        Le dictionnaire renvoyé contient toutes les tuiles et les props.
        """
        state = self.__dict__.copy()
        del state["display_surface"]
        return state

    def __setstate__(self, state):
        """
        Restaure l'état de l'objet à partir du dictionnaire "state".
        """

        self.__dict__.update(state)
        self.display_surface = display.get_surface()

        opensimplex.seed(self.seed)
        seed(self.seed)
