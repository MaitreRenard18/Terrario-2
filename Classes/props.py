import pygame
from Classes.tile import Tile

def generate_cactus(map, x, y, height):
    if height == 0:
        map.tiles[x][y] = Tile("cactus_top", False)
        return
    
    map.tiles[x][y] = Tile("cactus", False)
    generate_cactus(map, x, y-1, height-1)