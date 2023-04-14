import pygame
from pygame import Rect, Surface, Vector2, display, key, sprite

from Classes.tile import Scaffolding, Tile, Ore
from Classes.textures import import_textures

textures = import_textures("Player", (32, 32))
ores_textures = import_textures("Ores", (96, 96))
ui_textures = import_textures("UI", (942, 642))
font = pygame.font.Font('prstart.ttf', 27)


class Player(sprite.Sprite):

    def __init__(self, position: Vector2, map) -> None:
        super().__init__()
        """
        Initialise un Joueur. 
        Prend en paramètre un Vector2 qui correspond à la position du joueur.
        """

        # Initialise la position visible du joueur et sa position dans la map.
        self.position: Vector2 = Vector2(position)
        self.tile_pos: Vector2 = Vector2(position)
        self.tile_below: Tile = None

        # Initialise la vitesse du joueur et un booléen qui détermine si le joueur tombe.
        self.speed: float = 0.2
        self.falling: bool = False

        # Initialise la direction du joueur, et la position du la pointe.
        self.direction: str = "right"
        self.tip_tile: Vector2 = Vector2(1, 0)

        # Initialise l'image du joueur et de la pointe.
        self.image: Surface = textures[f"drill_{self.direction}"]
        self.tip: Surface = textures[f"drilltip_{self.direction}"]

        self.rect: Rect = self.image.get_rect()
        self.rect.topleft: tuple = self.position * 32

        # Initialise l'inventaire du joueur et un booléon qui détermine si il est affiché.
        self.inventory = {}
        for c in ores_textures:
            self.inventory[c] = 0
        self.displayed: bool = False
        self.display_surface = display.get_surface()

        self.map = map

    def mine(self) -> None:
        tile = self.map.get_tile(self.tile_pos)
        ore = tile.destroy()

        if ore is None:
            return
        if ore in self.inventory:
            self.inventory[ore] += 1
        else:
            self.inventory[ore] = 1

    def facing(self) -> None:
        self.image = textures[f"drill_{self.direction}"]
        self.tip = textures[f"drilltip_{self.direction}"]

    def climb(self) -> None:
        self.tile_below = self.map.get_tile(self.tile_pos + (0, 1))
        self.map._tiles[self.tile_pos.x][self.tile_pos.y + 1] = Scaffolding(self.tile_below.texture)

    def fall(self) -> None:
        self.tile_below = self.map.get_tile(self.tile_pos + (0, 1))
        if not self.tile_below.can_collide:
            if not self.falling:
                self.falling = True
                self.speed = 0
                return

            self.speed += 0.1
            self.speed = round(self.speed, 1)
            self.position.y += self.speed
            self.position.y = round(self.position.y, 1)

            if self.position.y >= self.tile_pos.y + 1:
                self.tile_pos.y += 1
                self.position.y = self.tile_pos.y
        else:
            self.falling = False
            self.speed = 0.2

    def display_inventory(self):
        self.display_surface.blit(ui_textures["inventory"], ((self.display_surface.get_width() - ui_textures["inventory"].get_width()) // 2, 0))
        return

    def update(self) -> None:

        self.rect.topleft = self.position * 32

        if self.displayed:
            self.display_inventory()
        
        if self.position == self.tile_pos and not self.falling:
            self.fall()
        
        if not self.falling:

            self.mine()

            if self.position != self.tile_pos:
                self.position += self.tip_tile * self.speed
                self.position.x = round(self.position.x, 1)
                self.position.y = round(self.position.y, 1)
                return
            
            keys = key.get_pressed()
            if keys[pygame.K_e]:
                self.displayed = True
                return
            else:
                self.displayed = False

            if keys[pygame.K_UP]:
                self.tip_tile.x, self.tip_tile.y =  0, -1
                self.direction = "up"
                self.tile_pos.y -= 1
                return

            if keys[pygame.K_DOWN]:
                self.tip_tile.x, self.tip_tile.y =  0, 1
                self.direction = "down"
                self.tile_pos.y += 1
                return

            if keys[pygame.K_RIGHT]:
                self.tip_tile.x, self.tip_tile.y = 1, 0
                self.direction = "right"
                self.tile_pos.x += 1
                return

            if keys[pygame.K_LEFT]:
                self.tip_tile.x, self.tip_tile.y = -1, 0
                self.direction = "left"
                self.tile_pos.x -= 1
                return
            
        self.fall()
