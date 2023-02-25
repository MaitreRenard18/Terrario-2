import pygame
from Classes.tile import Tile

def generate_cactus(map, x, y, height):
    if height == 0:
        map.tiles[x][y] = Tile("cactus_top", "cactus_top", minable=False, can_collide=False)
        return
    
    map.tiles[x][y] = Tile("cactus", "cactus", minable=False, can_collide=False)
    generate_cactus(map, x, y-1, height-1)

def generate_tree(map, x, y, height):
    pass

def generate_snowy_tree(map, x, y, height):
    pass