import pygame

class Tile:
    def __init__(self, type, can_collide=True):
        self.type = type
        self.can_collide = can_collide