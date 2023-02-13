import pygame

class Tile:
    def __init__(self, type, can_collide=True, drops = None):
        self.type = type
        self.can_collide = can_collide

        if drops is None:
            drops = []