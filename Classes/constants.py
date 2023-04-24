from typing import Dict, List, Union
from pathlib import Path

import pygame
from pygame import Surface


# Récupère le chemin d'accès des fichiers du jeu.
MODULE_PATH: Path = Path(__file__).parent.parent

# Récupère la taille de l'écran.
screen: Surface = pygame.display.set_mode()

# Initialise la police d'écriture utilisée pour l'inventaire et l'interface de craft.
pygame.font.init()
font: pygame.font.Font = pygame.font.Font("prstart.ttf", 27)

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

# Déclaration des ressources nécessaires pour augmenter le niveau du joueur.
requirements_upgrade: Dict[int, Dict[str, int]] = {
    1: {"rock": 5},
    2: {"iron": 10, "gold": 10, "coal": 10},
    3: {"uranium": 20, "copper": 20},
    4: {"ruby": 30},
    5: {"soul": 40},
    6: {"dark_crystal": 50},
    7: {}
}
