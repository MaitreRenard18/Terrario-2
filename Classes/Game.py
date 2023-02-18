import pygame, sys
from Classes.Map import Map

class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        self.screen = pygame.display.set_mode()
        self.clock = pygame.time.Clock()

        self.map = Map()

        self.run()

    def run(self):
        """Commence la boucle d'execution."""

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.map.render()
            self.map.player.update()
            pygame.display.update()
            self.clock.tick(30)
