import pygame, os

textures = {}
for file in os.listdir("{}\Images\Tiles".format(os.getcwd())):
    if file.endswith(".png"):
        file_name = file.replace(".png", "").lower()
        
        path = "{}\Images\Tiles\{}".format(os.getcwd(), file)
        image = pygame.transform.scale(pygame.image.load(path), (32, 32))
        
        textures[file_name] = image

class Tile:
    def __init__(self, type, texture, can_collide=True, drops = None):
        self.type = type
        self.texture = textures[texture] if isinstance(texture, str) else texture
        self.can_collide = can_collide

        if drops is None:
            drops = []

class Scaffolding(Tile):
    """Classe Scaffolding qui permet d'éviter d'avoir une texture différente pour chaque block ou l'échafaudage est placé."""
    def __init__(self, type, texture):
        surface = pygame.surface.Surface((32, 32))
        surface.fill(pygame.Color(77, 165, 217))
        surface.blit(textures[texture], (0, 0))
        surface.blit(textures["scaffolding"], (0, 0))

        super().__init__(type, surface)