import pygame
from pygame import Rect, Surface, Vector2, display, key, sprite

from Classes.tile import Scaffolding, Tile, Ore
from Classes.textures import import_textures

textures = import_textures("Player", (32, 32))
ores_textures = import_textures("Ores", (96, 96))
ui_textures = import_textures("UI", (942, 642))


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
        self.displayed: bool = False
        self.display_surface = display.get_surface()

        self.map = map

    def mine(self) -> None:
        tile = self.map.get_tile(self.tile_pos)
        ore = tile.destroy()

        if ore is None:
            return
        if ore not in self.inventory:
            self.inventory[ore] = 1
        else:
            self.inventory[ore] += 1

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
        inv_pos = (self.display_surface.get_width() - ui_textures["inventory"].get_width()) // 2
        self.display_surface.blit(ui_textures["inventory"], (inv_pos, 0))

        element, ligne = 0, 0
        for c in self.inventory:
            if element == 5:
                element = 0
                ligne += 1

            element_gap = element * 180
            ligne_gap = ligne * 180
            self.display_surface.blit(ores_textures[c], (inv_pos + 48 + element_gap, 107 + ligne_gap))

            text = font.render(str(self.inventory[c]), 1, (0,0,0))
            text_pos = (inv_pos + 153 + element_gap, 214 + ligne_gap)
            text_rect = text.get_rect(center = (text_pos))
            self.display_surface.blit(text, text_rect)
            element += 1

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

            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.tip_tile.x, self.tip_tile.y =  0, -1
                self.direction = "up"
                self.tile_pos.y -= 1
                return

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.tip_tile.x, self.tip_tile.y =  0, 1
                self.direction = "down"
                self.tile_pos.y += 1
                return

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.tip_tile.x, self.tip_tile.y = 1, 0
                self.direction = "right"
                self.tile_pos.x += 1
                return

            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.tip_tile.x, self.tip_tile.y = -1, 0
                self.direction = "left"
                self.tile_pos.x -= 1
                return
            
    def __getstate__(self):
        state = self.__dict__.copy()
        state["position"] = Vector2(round(self.position.x), round(self.position.y))
        del state["image"]
        del state["tip"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image: Surface = transform.scale(image.load(MODULE_PATH / "Images" / "Player" / "Drill_right.png"), (32, 32)).convert_alpha()
        self.tip: Surface = transform.scale(image.load(MODULE_PATH / "Images" / "Player" / "DrillTip_right.png"), (32, 32)).convert_alpha()