import pygame, opensimplex

class Map:
    def __init__(self, global_instance):
        self.global_instance = global_instance
        self.map = {0: {0: "diamond"}}

        self.cave_size = 0
        self.scale = 0.1

    def generate_tile(self, x, y):
        if not x in self.map:
            self.map[x] = {}
        
        if y in self.map[x]:
            return

        if opensimplex.noise2(x * self.scale, y * self.scale) > self.cave_size:
            self.map[x][y] = "stone"
        else:
            self.map[x][y] = "cave"

    def render(self):
        screensize = self.global_instance.screen.get_size()
        player_position = self.global_instance.player.position
        camera_offset = self.global_instance.player.get_camera_offset()
        tile_size = self.global_instance.tile_size

        for x in range(int(player_position.x - (screensize[0] // tile_size)),  int(player_position.x + (screensize[0] // tile_size))):
            for y in range(int(player_position.y - (screensize[1] // tile_size)),  int(player_position.y + (screensize[1] // tile_size))):
                self.generate_tile(x, y)

                offset = camera_offset // self.global_instance.tile_size - player_position
                tile_position = pygame.Vector2(x, y) + offset

                self.global_instance.screen.blit(self.global_instance.textures[self.map[x][y]], tile_position * tile_size)
