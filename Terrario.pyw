import pygame, os

class GlobalInstance:
    def __init__(self):
        self.init()
        self.load_textures()

        #TODO
        self.map = None
        self.player = None
        self.garage = None

        self.run()

    def init(self):
        """Initialise la fenêtre Pygame."""

        pygame.init()
        self.screen = pygame.display.set_mode()
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
            #TODO

            self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

if __name__ == "__main__":
    GlobalInstance()