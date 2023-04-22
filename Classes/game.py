import sys

import pygame

from .menu import Menu
from .map import Map
from .saving import save


class Game:
    def __init__(self):
        """Initialise la fenêtre Pygame et les différentes instances nécessaires au jeu."""

        pygame.init()
        pygame.event.set_allowed([pygame.QUIT, pygame.KEYDOWN, pygame.KEYUP])

        flags = pygame.FULLSCREEN | pygame.DOUBLEBUF
        self.screen = pygame.display.set_mode(flags=flags)
        self.clock = pygame.time.Clock()

        self.map = Map()
        self.menu = Menu(self.map)

        self.run()

    def run(self):
        """Commence la boucle d'execution."""

        show_stats = False
        max_fps = 30

        while True:

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_F1:
                    show_stats = not show_stats

                if event.type == pygame.KEYDOWN and event.key == pygame.K_F2:
                    max_fps = 120 if max_fps == 60 else 60 if max_fps == 30 else 30

                if event.type == pygame.QUIT:
                    if not self.menu.displayed:
                        save(self.save_name, self.map)
                    pygame.quit()
                    sys.exit()
               
            if self.menu.displayed:
                self.menu.update()

                if self.menu.main:
                    self.menu.play_button.check_event(event)
                else:
                    for c in self.menu.saves_buttons:
                        self.menu.saves_buttons[c].check_event(event)
                        if self.menu.delete:
                            self.menu.delete = False
                            break
                    for k in self.menu.world_buttons:
                        self.menu.world_buttons[k].check_event(event)

            else:
                self.map.update()
            
                if self.map.player.display_button:
                    self.map.player.upgrade_button.check_event(event)
            
            self.menu.quit_button.check_event(event)
            self.map = self.menu.map

            if show_stats:
                font = pygame.font.Font("prstart.ttf", 32)

                fps = font.render(f"FPS: {round(self.clock.get_fps())}", True, pygame.Color(255, 255, 255))
                pygame.display.get_surface().blit(fps, (2, 0))

                y = font.render(f"Position: {int(self.map.player.position.x)}, {int(self.map.player.position.y)}",
                                True, pygame.Color(255, 255, 255))
                pygame.display.get_surface().blit(y, (2, 32))

            pygame.display.update()
            self.clock.tick(max_fps)
