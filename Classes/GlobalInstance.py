import pygame, os
from Classes.Player import Player

class GlobalInstance:
    def __init__(self):
        self.init()
        self.load_textures()

        #TODO
        self.map = None
        self.player = Player(self)
        self.garage = None

        self.run()

    def init(self):
        """Initialise la fenêtre Pygame."""

        pygame.init()
        self.screen = pygame.display.set_mode((512, 512))
        pygame.display.set_caption("Terrario")
    
    def load_textures(self):
        """Charge les textures du dossier "\Images" et les stocks sous forme d'images Pygame, dans un dictionnaire "self.textures"."""

        self.textures = {}
        for file in os.listdir("Images"):
            if file.endswith(".png"):
                file_name = file[:-4].lower()
                path = f"Images\{file}"
                texture = pygame.image.load(path)

                self.textures[file_name] = texture

    def run(self):
        """Commence la boucle d'execution."""

        self.clock = pygame.time.Clock()
        self.running = True
        while self.running:
            self.clock.tick(60)
            self.screen.fill(pygame.Color(0, 0, 0))
            self.player.tick()

            pygame.display.flip()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False