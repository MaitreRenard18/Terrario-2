import pygame, sys


class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(flags=flags)
        self.clock = pygame.time.Clock()

        from Classes.map import Map
        self.map = Map()

        self.run()

    def run(self):
        """Commence la boucle d'execution."""
        
        self.map.render()
        self.map.player.update()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.map.player.update()
            self.map.render()
            pygame.display.update()
            self.clock.tick(60)