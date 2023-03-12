from typing import Union, Dict, List, Callable

from pygame import Vector2, Surface, Color, display
import opensimplex
import pygame

from Classes.player import Player
from Classes.tile import Tile, Cave, Air

class Map:
    """
    Class qui réprésente une carte 2D générée procéduralement composée de grottes et de différents biomes en fonction de la profondeur.
    """

    def __init__(self) -> None:
        """
        Initialise une Map.
        """

        # Récupère la surface d'affichage
        self.display_surface: Surface = display.get_surface()

        # Initialise le joueur et le dictionnaire contenant les tuiles.
        self.player: Player = Player((0, -1), self)
        self._tiles: Dict[int, Dict[int, Tile]] = {}

        # Initialise les valeurs utilisées lors de la génération de le carte.
        opensimplex.seed = randint(0, 2**16)

        self.scale: float = 0.1
        self.cave_size: float = 0.5
        self.biome_size: float = 0.0075
        self.biome_blend: int = 3

        # Récupère le nombre de tuiles qui peut être afficher en x et en y.
        self.render_distance: tuple = (self.display_surface.get_size()[0] // 32 // 2 + 4, self.display_surface.get_size()[1] // 32 // 2 + 4)

    def get_tile(self, position: Vector2) -> Tile:
        """
        Prend en paramètre un Vector2 et retourne la tuile se trouvant à cette position. 
        Si la tuile n'existe pas, en génère une nouvelle.
        """

        # Vérifie si la tuile existe dans self._tiles, et la génère si se n'est pas le cas.
        if not position.x in self._tiles or not position.y in self._tiles[position.x]:
            self._generate_tile(position.copy())

        # Récupère la tuile et la retourne.
        return self._tiles[position.x][position.y]

    def set_tile(self, tile: Tile, position: Vector2) -> Tile:
        """
        Prend en paramètre une Tuile et un Vector2, et change la tuile se trouvant à cette position par la tuile passée en paramètre. 
        Retourne la tuile passée en paramètre.
        """

        # Vérifie si la tuile existe dans self._tiles, et la génère si se n'est pas le cas.
        position.x, position.y = int(position.x), int(position.y)
        if not position.x in self._tiles or not position.y in self._tiles[position.x]:
            self._generate_tile(position.copy())

        # Change la tuile et la retourne.
        self._tiles[position.x][position.y] = tile
        return tile

    def _generate_tile(self, position: Vector2) -> Tile:
        """
        Prend en paramètre un Vector2 et génère une tuile à cette position.
        Retourne la tuile générée.
        """

        # Créer une entrée dans le dictionnaire.
        if not position.x in self._tiles:
            self._tiles[position.x] = {}

        # Récupère le biome.
        for k in biomes.keys():
            if position.y + randint(0, self.biome_blend) >= k:
                number_range = 2 / len(biomes[k])
                noise_value = opensimplex.noise2((position.x + randint(0, self.biome_blend)) * self.biome_size, 0) + 1
                biome = biomes[k][int(noise_value // number_range)]
                break

        tile_palette = tile_palettes[biome] if biome in tile_palettes else tile_palettes["cave"] # TODO à enlever quand tout les biomes seront implémentés. 
        
        # Génération de la tuile si elle se trouve à la surface.
        if position.y - randint(0, self.biome_blend) < 16:
            noise_value = int(opensimplex.noise2(position.x * self.scale * 0.25, 0) * 8)
            if position.y == noise_value:
                if "floor_tile" in tile_palette:
                    self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], 0)

                else:
                    self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], 0)
            
            elif position.y > noise_value:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], 0)

            else:
                self._tiles[position.x][position.y] = Air()

        # Génération de la tuile si elle se trouve sous terre.
        else:
            if opensimplex.noise2(position.x * self.scale, position.y * self.scale) < (self.cave_size * 2) - 1:
                self._tiles[position.x][position.y] = Tile(tile_palette["primary_tile"], 0) # TODO à changer quand le niveau du drill sera implémenté.
                
                if "floor_tile" in tile_palette and not self.get_tile(position - Vector2(0, 1)).can_collide:
                    self._tiles[position.x][position.y] = Tile(tile_palette["floor_tile"], 0 ) # TODO à changer quand le niveau du drill sera implémenté.
                
                if "ceiling_tile" in tile_palette and not self.get_tile(position + Vector2(0, 1)).can_collide:
                    self._tiles[position.x][position.y] = Tile(tile_palette["ceiling_tile"], 0) # TODO à changer quand le niveau du drill sera implémenté.

            else:
                self._tiles[position.x][position.y] = Cave(tile_palette["primary_tile"])

        # Génération des props.
        """
        if self._tiles[position.x][position.y].can_collide and not self.get_tile(position - Vector2(0, 1)).can_collide and biome in props:
            if randint(1, 4) == 1:
                choice(props[biome])(self, position - (0, 1))
        """ #TODO Fix les props

        return self._tiles[position.x][position.y]

    def update(self) -> None:
        """
        Affiche la carte sur l'écran et s'occupe de mettre à jour les différentes tuiles, ainsi que le joueur. 
        """

        # Affiche le ciel.
        self.display_surface.fill(Color(77, 165, 217))
        
        offset = Vector2()
        offset.x = self.player.rect.centerx - self.display_surface.get_width() / 2
        offset.y = self.player.rect.centery - self.display_surface.get_height() / 2

        for x in range(int(self.player.position.x) - self.render_distance[0], int(self.player.position.x) + self.render_distance[0]):
            for y in range(int(self.player.position.y) - self.render_distance[1], int(self.player.position.y) + self.render_distance[1]):
                offset_rect = Vector2(x, y) * 32 - offset
                self.get_tile(Vector2(x, y)).update(offset_rect)

        offset_rect = self.player.rect.copy()
        offset_rect.center -= offset

        self.player.facing(self.player.going["direction"])

        self.display_surface.blit(self.player.image, offset_rect)
        self.display_surface.blit(self.player.tip, (offset_rect.x + self.player.going["tip_tile"][0] * 32, offset_rect.y + self.player.going["tip_tile"][1] * 32))

        if self.player.going["direction"] == "up":
            self.player.climb()

        self.player.update()


from Classes.props import *
biomes: Dict[Union[float, int], List[str]] = {
    #512: ["hell"],
    #256: ["crystal_cave", "haunted_cave"],
    #128: ["lush_cave"],
    16: ["sand_cave", "cave", "ice_cave"],
    float("-inf"): ["desert", "forest", "snowy_forest"]
}

tile_palettes: Dict[str, Dict[str, str]] = {
    "forest": {
        "primary_tile": "dirt",
        "floor_tile": "grass"
    },

    "desert": {
        "primary_tile": "sand"
    },

    "snowy_forest": {
        "primary_tile": "snowy_dirt",
        "floor_tile": "snowy_grass"
    },

    "cave": {
        "primary_tile": "stone",
    },

    "sand_cave": {
        "primary_tile": "sandstone",
    },

    "ice_cave": {
        "primary_tile": "ice",
    },

    "lush_cave": {
        "primary_tile": "tuff",
        "floor_tile": "mossy_tuff",
        "ceiling_tile": "tuff"
    },
}

props: Dict[str, List[Callable[[map, Vector2], None]]] = {
    "forest": [generate_oak_tree, generate_plants, generate_plants], 
    "desert": [generate_cactus, generate_dead_weed, generate_dead_weed],
    "snowy_forest": [generate_fir, generate_fir, generate_snowy_weed, generate_snowy_weed, generate_snowman],

    "cave": [generate_stalagmite]
}

ores: Dict[str, List[str]] = {
    "forest": [],
    "desert": [],
    "snowy_forest": []
}
