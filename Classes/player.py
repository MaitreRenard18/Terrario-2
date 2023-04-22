from time import sleep
from typing import Dict

import pygame
from pygame import Rect, Surface, Vector2, display, key, sprite

from .tile import Scaffolding, Tile
from .button import Button
from .textures import load_textures

# Charge les textures concernant le joueur, les minerais, l'inventaire et l'interface de craft.
player_textures: Dict[str, Surface] = load_textures("Player", (32, 32))
ores_textures: Dict[str, Surface] = load_textures("Ores", (96, 96))
button_textures: Dict[str, Surface] = load_textures("Button", (300, 90))
inventory_texture: Surface = load_textures("UI/inventory.png", (942, 642))
craft_interface_texture: Surface = load_textures("UI/craft_interface.png", (840, 390))

# Initialise la police d'écriture utilisée pour l'inventaire et l'interface de craft.
pygame.font.init()
font = pygame.font.Font("prstart.ttf", 27)

# Déclaration des ressources requises pour augmenter le niveau du joueur.
requirements_upgrade: Dict[int, Dict[str, int]] = {
    1: {"rock": 5},
    2: {"iron": 10, "gold": 10, "coal": 10},
    3: {"uranium": 20, "copper": 20},
    4: {"ruby": 30},
    5: {"soul": 40},
    6: {"dark_crystal": 50},
    7: {}
}


# Déclaration de la classe Player.
class Player:
    """
    Class qui représente un joueur qui se situe au milieu de l'écran.
    """

    def __init__(self, position: Vector2, map) -> None:
        """
        Initialise un Joueur. 
        Prends en paramètres un Vector2, qui correspond à la position du joueur
        et une map, qui correspond à la carte dans laquelle il se déplace.
        """

        # Initialise la position du joueur et sa direction.
        self.position: Vector2 = Vector2(position)
        self.relative_position: Vector2 = Vector2(position)
        self.tip_position: Vector2 = Vector2(1, 0)
        self.direction: str = "right"

        # Initialise le niveau, la vitesse du joueur et un booléen qui détermine si le joueur tombe.
        self.level: int = 1
        self.speed: float = 0.2
        self.falling: bool = False

        # Initialise l'inventaire du joueur, un bouton et un booléen qui déterminent si il est affiché.
        self.inventory: Dict[str, int] = {}
        self.upgrade_button: Button = Button(button_textures["up_button"].get_rect(center=(1080,383)), button_textures["up_button"], 
                                             button_textures["button_hovered"], "Upgrade", 32, self.upgrade)
        self.display_button: bool = False

        # Récupère l'image du joueur et de la pointe.
        self.image: Surface = player_textures[f"drill_{self.direction}"]
        self.tip_image: Surface = player_textures[f"drilltip_{self.direction}_{str(self.level)}"]

        # Récupère le rectangle où l'image du joueur va être affichée et la taille de l'écran.
        self.rect: Rect = self.image.get_rect()
        self.rect.topleft: tuple = self.position * 32
        self.display_surface: Surface = display.get_surface()

        # Récupère la map dans laquelle le joueur se trouve.
        self.map = map

    def mine(self) -> None:
        """
        Détruit la tile où le joueur se situe.
        Incrémente une valeur de l'inventaire si la tile minée est un minerai.
        """

        tile = self.map.get_tile(self.relative_position)
        ore = tile.destroy()

        if ore is None:
            return
        if ore not in self.inventory:
            self.inventory[ore] = 1
        else:
            self.inventory[ore] += 1

    def breakable(self) -> bool:
        """
        Retourne un booléen qui détermine si une tile est cassable selon le niveau du joueur.
        """

        tile = self.map.get_tile(self.relative_position)
        if tile.hardness > self.level:
            return False
        else:
            return True
        
    def facing(self) -> None:
        """
        Modifie l'image du joueur et de la pointe en fonction de sa direction et de son niveau.
        """

        self.image = player_textures[f"drill_{self.direction}"]
        self.tip_image = player_textures[f"drilltip_{self.direction}_{str(self.level)}"]

    def climb(self) -> None:
        """
        Affiche un échafaudage sur la tile en dessous de la position relative du joueur.
        S'il y a déjà un échafaudage, ça n'affiche rien en plus.
        """

        tile_below = self.map.get_tile(self.relative_position + (0, 1))
        if isinstance(tile_below, Scaffolding):
            return
        self.map._tiles[self.relative_position.x][self.relative_position.y + 1] = Scaffolding(tile_below.texture)

    def fall(self) -> None:
        """
        Fait tomber le joueur.
        La vitesse du joueur augmente au fur et à mesure qu'il tombe.
        La limite de vitesse du joueur est d'une tile.
        """

        self.speed += round(0.1, 1)
        self.position.y += self.speed
        self.position.y = round(self.position.y, 1)

        if self.position.y >= self.relative_position.y + 1:
            self.relative_position.y += 1
            self.position.y = self.relative_position.y
        
    def upgrade(self) -> None:
        """
        Améliore le niveau du joueur si il a les ressources nécessaires.
        Dans le cas contraire, affiche un texte pendant 1.5 seconde.
        Les ressources nécessaires pour l'amélioration sont enlevées de l'inventaire.
        """

        if self.level == 7:
            return

        for keys, values in requirements_upgrade[self.level].items():
            if not keys in self.inventory or self.inventory[keys] < values:
                text = font.render(("Vous n'avez pas assez de ressources"), True, "BLACK")
                self.display_surface.blit(text, (500, 400))
                pygame.display.flip()
                sleep(1.5)
                return

        for keys, values in requirements_upgrade[self.level].items():
            self.inventory[keys] -= values
        self.level += 1
        sleep(0.1)

    def display_inventory(self) -> None:
        """
        Affiche l'inventaire du joueur en fonction des minerais récupérés.
        """

        inv_pos = (self.display_surface.get_width() - inventory_texture.get_width()) // 2
        self.display_surface.blit(inventory_texture, (inv_pos, 0))

        element, ligne = 0, 0
        for c in self.inventory:
            if element == 5:
                element = 0
                ligne += 1

            element_gap = element * 180
            ligne_gap = ligne * 180

            self.display_surface.blit(ores_textures[c], (inv_pos + 48 + element_gap, 107 + ligne_gap))
            text = font.render(str(self.inventory[c]), True, "BLACK")
            self.display_surface.blit(text, text.get_rect(center = (inv_pos + 154 + element_gap, 214 + ligne_gap)))
            element += 1

    def display_craft_interface(self) -> None:
        """
        Affiche l'interface de craft et les minerais requis pour améliorer le niveau du joueur.
        """

        craft_interface_position = (self.display_surface.get_width() - craft_interface_texture.get_width()) // 2
        self.display_surface.blit(craft_interface_texture, (craft_interface_position, 0))

        element = 0
        for keys, values in requirements_upgrade[self.level].items():
            element_gap = element * 180
            self.display_surface.blit(ores_textures[keys], (craft_interface_position + 306 + element_gap, 170))
            text = font.render(str(values), True, "BLACK")
            self.display_surface.blit(text, text.get_rect(center = (craft_interface_position + 412 + element_gap, 274)))
            element += 1

    def update(self) -> None:
        """
        Met à jour le joueur s'il se déplace où tombe.
        Permet d'afficher les interfaces de l'inventaire ou de craft.
        """
        self.rect.topleft = self.position * 32

        # Téléporte le joueur s'il est sous la carte
        if self.position.y > 1200:
            text = font.render("Merci d'avoir joué!", True, "WHITE")
            self.display_surface.blit(text,  text.get_rect(center=(self.display_surface.get_width() // 2,
                                                                   self.display_surface.get_height() // 2 + 128)))

        if self.position.y > 1525:
            self.position.y = -128
            self.relative_position.y = -128
            return

        # Vérifie si la tile en dessous du joueur est solide.
        if self.position == self.relative_position:
            tile_below = self.map.get_tile(self.relative_position + (0, 1))
            if not tile_below.can_collide:
                if not self.falling:
                    self.falling = True
                    self.speed = 0
                    return
            else:
                if self.falling:
                    self.falling = False
                    self.speed = 0.2
        
        if not self.falling:
            
            # Permet au joueur de miner un bloc s'il est cassable.
            if self.breakable():
                self.mine()
            else:
                self.relative_position -= self.tip_position
                return
            
            # Permet au joueur de grimper sur des échafaudages s'il va vers le haut.
            if self.direction == "up":
                self.climb()

            # Incrémente la position du joueur jusqu'à être à la position relative.
            if self.position != self.relative_position:
                self.position += self.tip_position * self.speed
                self.position.x = round(self.position.x, 1)
                self.position.y = round(self.position.y, 1)
                return
            
            # Affiche l'inventaire ou l'interface de craft si le joueur appui sur E ou A.
            keys = key.get_pressed()
            if keys[pygame.K_e]:
                self.display_button = False
                self.display_inventory()
                return

            if keys[pygame.K_a]:
                self.display_button = True
                self.display_craft_interface()
                return
            else:
                self.display_button = False
            
            # Permet au joueur de se déplacer en appuyant sur les flèches ou les touches : ZQSD
            if keys[pygame.K_UP] or keys[pygame.K_z]:
                self.tip_position.x, self.tip_position.y =  0, -1
                self.direction = "up"
                self.relative_position.y -= 1
                return

            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.tip_position.x, self.tip_position.y =  0, 1
                self.direction = "down"
                self.relative_position.y += 1
                return

            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.tip_position.x, self.tip_position.y = 1, 0
                self.direction = "right"
                self.relative_position.x += 1
                return

            if keys[pygame.K_LEFT] or keys[pygame.K_q]:
                self.tip_position.x, self.tip_position.y = -1, 0
                self.direction = "left"
                self.relative_position.x -= 1
                return
        else: 
            self.fall()
        
    def __getstate__(self):
        state = self.__dict__.copy()
        state["position"] = Vector2(round(self.position.x), round(self.position.y))
        del state["image"]
        del state["display_surface"]
        del state["tip_image"]
        del state["upgrade_button"]
        del state["display_button"]
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self.image: Surface = player_textures[f"drill_{self.direction}"]
        self.tip_image: Surface = player_textures[f"drilltip_{self.direction}_{str(self.level)}"]
        self.display_surface = display.get_surface()
        self.upgrade_button: Button = Button(button_textures["up_button"].get_rect(center=(1080,383)), button_textures["up_button"], 
                                             button_textures["button_hovered"], "Upgrade", 32, self.upgrade)
        self.display_button: bool = False
